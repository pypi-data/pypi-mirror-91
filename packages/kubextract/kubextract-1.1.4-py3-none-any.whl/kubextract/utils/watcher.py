import os
import re
import json
import kfp
import time
import subprocess
import requests
from kubernetes import client, config
from datetime import datetime
from urllib.parse import quote_plus


class RunPipe:
    """This is end-to-end kubeflow process.

    Generate kubeflow pipeline configuration.
    Run kubeflow experiment.
    Monitoring kubeflow experiment job.
    Send notification for job status.

    Attributes:
        params (dict): parameters that will be used on pipeline.

    """

    def __init__(self, params=None):
        """Construct for storing class attributes.

        Args:
            params_path (str): location of component params.

        """
        self.params = params
        config.load_incluster_config()

    def get_pipeline_list(self):
        """Get all pipelines that created on kubeflow platform.

        Returns:
            dict: list of pipelines info.

        """
        kfp_client = kfp.Client()
        pipeline_data = {}
        page_token = None

        while True:
            pipeline_list = kfp_client.list_pipelines(
                page_token=page_token, page_size=5
            )

            for pipe in pipeline_list.pipelines:
                pipeline_data[pipe.name] = pipe.id

            page_token = pipeline_list.next_page_token
            if page_token is None:
                break

        return pipeline_data

    def get_pipeline_version_list(self, pipeline_id):
        """Get all pipeline versions that created on kubeflow platform.

        Args:
            pipeline_id (str): pipeline ID that used for checking versions.

        Returns:
            dict: list of pipeline versions info.

        """
        kfp_client = kfp.Client()
        pipe_versions = {}
        page_token = None

        while True:
            version_list = kfp_client.pipelines.list_pipeline_versions(
                resource_key_id=pipeline_id, page_token=page_token, page_size=5
            )
            version_list = version_list.to_dict()

            for version in version_list["versions"]:
                pipe_versions[version["name"]] = version["id"]

            page_token = version_list["next_page_token"]
            if page_token is None:
                break

        return pipe_versions

    def check_any_pipeline(self, local_path, pipeline_data):
        """Checking if any pipeline.

        Prevent create duplicate pipeline and pipeline version.
        If they do not exist, than create new pipeline

        Args:
            local_path (str): location of pipeline config file.
            pipeline_data (dict): list of pipelines info.

        Returns:
            :rtype: (str, str): pipeline or version id and category id.

        """
        pipe_name = self.params["PIPE_NAME"]
        pipe_ver_name = "{pipe_name}-{version}".format(
            pipe_name=self.params["PIPE_NAME"],
            version=os.getenv("CI_COMMIT_SHA")
        )

        try:
            pipeline_id = pipeline_data[pipe_name]
            pipe_versions = self.get_pipeline_version_list(pipeline_id)
            kfp_client = kfp.Client()

            try:
                return (pipe_versions[pipe_ver_name], "ver_id")
            except KeyError:
                res_ver = kfp_client.pipeline_uploads.upload_pipeline_version(
                    local_path, pipelineid=pipeline_id, name=pipe_ver_name
                )

                return (res_ver.id, "ver_id")
        except KeyError:
            print("there's no pipeline selected, try to create new...")
            kfp_client = kfp.Client()
            res_pipe = kfp_client.upload_pipeline(local_path, pipe_name)

            return (res_pipe.id, "pipe_id")

    def check_any_experiment(self):
        """Checking if any experiment.

        Prevent create duplicate experiment.
        If the experiment doesn't exist, than create new one.

        Returns:
            str: experiment id.

        """
        exp_name = self.params["EXP_NAME"]
        exp_desc = self.params["EXP_DESC"]

        try:
            kfp_client = kfp.Client()
            res_exp = kfp_client.get_experiment(experiment_name=exp_name)
            exp_id = res_exp.id
        except Exception:
            kfp_client = kfp.Client()
            res_exp = kfp_client.create_experiment(
                exp_name, description=exp_desc
            )
            exp_id = res_exp.id

        return exp_id

    def run_logging(self, pod_names, prev_time, cur_time):
        """Print logging from stackdriver.

        Args:
            pod_names (list): List of pod names.
            prev_time (str): Start time of logging.
            cur_time (str): End time of logging.

        """
        pod_name_filter = ""
        for i, pod_name in enumerate(pod_names):
            if i == 0:
                pod_name_filter += pod_name
            else:
                pod_name_filter += " OR {pod_name}".format(
                    pod_name=pod_name
                )

        cmd_str = """gcloud logging read \
            'timestamp>=\"{prev_time}\" AND timestamp<=\"{cur_time}\"
            AND resource.type=k8s_container
            AND resource.labels.cluster_name=kubeflow-research
            AND resource.labels.pod_name=({pod_name})' \
            --order=asc --format=json | python3 -c \
            'import sys, json; [print(data[\"textPayload\"]) \
            for data in json.load(sys.stdin)]'""".format(
            prev_time=prev_time,
            cur_time=cur_time,
            pod_name=pod_name_filter,
        )

        os.system(cmd_str)

    def send_notification(self, nodes, comps, status, job_name, log_url):
        """Get notification into workchat channels.

        Get notification of logging stackdriver url and job status.

        Args:
            nodes (dict): List of component job description.
            comps (list): List of pod names.
            status (str): Component job status.
            job_name (str): Experiment job name.
            log_url (str): Stackdriver logging url.

        Returns:
            type: Description of returned object.

        """
        base_url = "https://api.warungpintar.co/warbot/v1/send?recipient="
        url = (
            "{base_url}{workchat_id}&type=\
            {workchat_type}&gitlab_token={token}".format(
                base_url=base_url,
                workchat_id=self.params["WORKCHAT_ID"],
                workchat_type=self.params["WORKCHAT_TYPE"],
                token=self.params["GITLAB_PERS_TOKEN"],
            )
        )
        headers = {"content-type": "application/json"}

        comp_status = ""

        for i, comp in enumerate(comps):
            sel_node = nodes[comp]
            sel_comp_stat = """<COMPONENT-{n_comp}>
            COMP_NAME: {dis_name}
            STATUS: {phase}
            FINISH_DATE: {finish_time}\n\n""".format(
                n_comp=str(i + 1),
                dis_name=sel_node["displayName"],
                phase=sel_node["phase"],
                finish_time=sel_node["finishedAt"],
            )
            comp_status += sel_comp_stat

        msg = """<<<{job_name}>>>\n
        JOB_STATUS: {status}
        LOGGING URL: {log_url}\n
        {comp_status}""".format(
            job_name=job_name, status=status,
            log_url=log_url, comp_status=comp_status
        )
        data = {"message": msg}
        json_data = json.dumps(data)

        requests.post(url, headers=headers, data=json_data)

    def get_namespace_and_pods(self, pipe_run_id):
        """Get namespace and pod names that run on kubeflow.

        Args:
            pipe_run_id (str): Pipeline job id.

        Returns:
            list: List of pod names.

        """
        while True:
            namespaces = []

            v1 = client.CoreV1Api()
            ret = v1.list_pod_for_all_namespaces(watch=False)
            for i in ret.items:
                namespaces.append((i.metadata.namespace, i.metadata.name))

            kfp_client = kfp.Client()
            response = kfp_client.get_run(run_id=pipe_run_id)
            manifest = json.loads(response.pipeline_runtime.workflow_manifest)
            pattern = manifest["metadata"]["name"]

            pods = [ns[1] for ns in namespaces if re.match(pattern, ns[1])]

            if len(pods) > 0:
                break
            else:
                print("pods not found, trying to search pods...")
                time.sleep(1)

        return pods

    def check_job(self, pipe_run_id):
        """Check pipeline job whether is success or fail.

        Args:
            pipe_run_id (str): Pipeline job id.

        Returns:
            dict: Description of pipeline job.

        """
        job_details = {"nodes": None, "job_status": None, "job_name": None}

        try:
            kfp_client = kfp.Client()
            response = kfp_client.wait_for_run_completion(
                run_id=pipe_run_id, timeout=5
            )

            manifest = json.loads(response.pipeline_runtime.workflow_manifest)

            job_details["nodes"] = manifest["status"]["nodes"]
            job_details["job_status"] = manifest["status"]["phase"]
            job_details["job_name"] = response.run.name

            return job_details
        except Exception:
            return job_details

    def wait_job_until_finish(self, pipe_run_id, comps, log_url):
        """Checking job when pipeline job success or failed.

        Args:
            pipe_run_id (str): Pipeline job id.
            comps (type): List of pod names.
            log_url (type): Stackdriver logging url.

        """
        prev_time = datetime.now().isoformat(timespec="seconds") + "Z"
        job_details = self.check_job(pipe_run_id)
        is_finished = False

        while True:
            if job_details["job_status"] == "Succeeded":
                is_finished = True

            if (
                job_details["job_status"] == "Succeeded"
                or job_details["job_status"] == "Failed"
            ):
                self.send_notification(
                    job_details["nodes"],
                    comps,
                    job_details["job_status"],
                    job_details["job_name"],
                    log_url,
                )
                break

            time.sleep(1)
            cur_time = datetime.now().isoformat(timespec="seconds") + "Z"
            self.run_logging(comps, prev_time, cur_time)

            job_details = self.check_job(pipe_run_id)
            prev_time = cur_time

        if not is_finished:
            raise Exception("Job is failed, please check your logs...")

    def generate_log_url(self, pod_names):
        """Modify stackdriver url with selected pod names.

        Args:
            pod_names (list): List of pod names.

        Returns:
            str: final stackdriver url after modified.

        """
        pod_name_filter = ""
        for i, pod_name in enumerate(pod_names):
            if i == 0:
                pod_name_filter += '"{pod_name}"'.format(
                    pod_name=pod_name
                )
            else:
                pod_name_filter += ' OR "{pod_name}"'.format(
                    pod_name=pod_name
                )

        base_url = "https://console.cloud.google.com/logs/viewer?"
        filter_url = "project=warung-support&interval=NO_LIMIT&advancedFilter="
        query_str = 'resource.type="k8s_container" \n\
            AND resource.labels.cluster_name="kubeflow-research" \n\
            AND resource.labels.pod_name={pod_name}'.format(
            pod_name=pod_name_filter
        )

        query = quote_plus(query_str, safe="()")
        final_url = base_url + filter_url + query

        return final_url

    def run_pipe(self):
        """All process when running job on kubeflow."""
        pipeline_data = self.get_pipeline_list()

        # check if any existing pipeline
        pipe_id, id_type = self.check_any_pipeline(
            self.params["PIPE_PATH"], pipeline_data
        )

        # check if any existing experiment
        exp_id = self.check_any_experiment()
        kfp_client = kfp.Client()
        job_name = "{exp_name} experiment {commit_sha}".format(
            exp_name=self.params["EXP_NAME"],
            commit_sha=os.getenv("CI_COMMIT_SHA")
        )

        if id_type == "pipe_id":
            pipe_run = kfp_client.run_pipeline(
                exp_id, job_name, pipeline_id=pipe_id
            )
        elif id_type == "ver_id":
            pipe_run = kfp_client.run_pipeline(
                exp_id, job_name, version_id=pipe_id
            )

        pod_names = self.get_namespace_and_pods(pipe_run.id)
        # generate stackdriver logging url
        log_url = self.generate_log_url(pod_names)

        self.wait_job_until_finish(pipe_run.id, pod_names, log_url)

    def check_node_pool_label(self):
        """Checking node pool whether exist or not.

        Returns:
            bool: Node pool status.

        """
        all_labels = []
        sel_labels = []

        cmd_str = "gcloud container node-pools list \
        --cluster=kubeflow-research --zone=asia-east1-a \
        --format=json"

        process = subprocess.Popen(
            [cmd_str], shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, err = process.communicate()
        out = out.decode("UTF8")
        nodes = json.loads(out)

        for node in nodes:
            labels = node["config"]["labels"]
            all_labels.append(labels)

        for c_comp in self.params["COMPONENTS"]:
            node_key = c_comp["NODE_KEY"]
            node_val = c_comp["NODE_VAL"]

            sel_label = list(
                (
                    item
                    for item in all_labels
                    if node_key in item.keys() and node_val in item.values()
                )
            )
            sel_labels += sel_label

        if len(sel_labels) == len(self.params["COMPONENTS"]):
            print(
                "node label {node_key}: {node_val} is existed".format(
                    node_key=node_key, node_val=node_val
                )
            )
            return True
        else:
            print(
                "node label {node_key}: {node_val} is not existed".format(
                    node_key=node_key, node_val=node_val
                )
            )
            return False

    def check_image_tag(self):
        """Check image tag whether exist or not.

        Returns:
            bool: image tag status.

        """
        status = True

        for c_comp in self.params["COMPONENTS"]:
            cmd_str = 'gcloud container images list \
            --repository={img_registry} \
            --filter="name:{img_name}"'.format(
                img_registry=self.params["IMAGE_REGISTRY"],
                img_name=c_comp["IMG_NAME"]
            )

            process = subprocess.Popen(
                [cmd_str], shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            out, err = process.communicate()
            out = out.decode("UTF8").split("\n")

            if len(out) == 1:
                status = False
                print(
                    "image tag {img_name} is not existed".format(
                        img_name=c_comp["IMG_NAME"]
                    )
                )
                break
            else:
                print(
                    "image tag {img_name} is existed".format(
                        img_name=c_comp["IMG_NAME"]
                    )
                )
                continue

        return status

    def main(self):
        """All process run on kubeflow."""
        if not self.check_image_tag():
            raise Exception("Image tag not found...")

        if not self.check_node_pool_label():
            raise Exception("node pool label not found...")

        self.run_pipe()
