from prompt_toolkit.validation import Validator, ValidationError
from PyInquirer import prompt
import click
import ruamel.yaml as yaml
import os
import re


class StringValidator(Validator):
    """Checking input for avoiding error."""

    def validate(self, document):
        """Checking input for empty and TypeVariable.

        Args:
            document (obj): input object of CLI.

        """
        if document.text == "":
            raise ValidationError(message="Please do not input empty string")

        try:
            str(document.text)
        except Exception:
            inp_type = str(str)
            raise ValidationError(
                message="Please input {inp_type} type".format(
                    inp_type=inp_type
                )
            )


QUES = [
    {
        "type": "input",
        "name": "params_path",
        "message": "Where's your params yaml path:",
        "validate": StringValidator,
    }
]


class GenerateFrame:
    """Automatically extract kubeflow component framework.

    This extraction include all kubeflow, docker and gitlab-ci configuration.

    Args:
        params_path (str): location of component params.

    Attributes:
        params (dict): List of component params.
        build_template (str): template of build image config file.
        kubepipe_template (str): template of kubepipe deployment config file.
        kfserve_template (str): template of kfserving deployment config file.
        main_ci_template (str): template of main gitlab-ci config file.
        cloudbuild_template (str): template of cloudbuild config file.
        params_path

    """

    def __init__(self, params_path=None):
        """Construct for storing class attributes.

        Args:
            params_path (str): location of component params.

        """
        self.params = self.load_params(params_path)
        self.params_path = params_path

        dir_name = os.path.dirname(os.path.abspath(__file__))
        dir_name = dir_name.replace("utils", "templates")

        self.build_template = os.path.join(
            dir_name, "_build-gitlab-ci.yml"
        )
        self.kubepipe_template = os.path.join(
            dir_name, "_kubepipe-gitlab-ci.yml"
        )
        self.kfserve_template = os.path.join(
            dir_name, "_kfserving-gitlab-ci.yml"
        )
        self.main_ci_template = os.path.join(
            dir_name, "_gitlab-ci.yml"
        )
        self.cloudbuild_template = os.path.join(
            dir_name, "_cloudbuild.yaml"
        )

    def load_params(self, path):
        """Read params file for component params.

        Args:
            path (str): location of params file.

        Returns:
            dict: component params.

        """
        with open(path, "r") as stream:
            params = yaml.safe_load(stream)

        return params

    def add_build_ci_env(self, build_str, comp):
        """Add environment on subtitutions gcloud build flag.

        In order to add additional args when building image.

        Args:
            build_str (str): Template of gcloud build on gitlab-ci.
            comp (dict): Attributes of component.

        Returns:
            str: Template of gcloud build have been modified.

        """
        space = " " * 6

        try:
            for env_var in comp["CI_ENV"]:
                build_str += ",\\\n{space}_{key}=${value}".format(
                    key=env_var, value=env_var, space=space
                )

            build_str += "\n"
        except KeyError:
            build_str += "\n"

        return build_str

    def generate_ci_build_conf(self):
        """Modify configuration of build stage on gitlab-ci.

        Variables on the template will be changed into params values.
        Also, add new string as variables on subtitutions.

        Returns:
            str: Final configuration of build stage

        """
        final_str = ""

        for i, c_comp in enumerate(self.params["COMPONENTS"]):
            with open(self.build_template, "r") as rfile:
                build_str = rfile.read()
                build_str_len = len(build_str)

                if build_str[build_str_len - 1] == "\n":
                    build_str = build_str[: build_str_len - 1]

                build_str = build_str.format(
                    stage_name=c_comp["STAGE_NAME"],
                    local_src=self.params["LOCAL_SRC"],
                    comp_path=c_comp["COMP_PATH"],
                    image_registry=self.params["IMAGE_REGISTRY"],
                    image_tag=c_comp["IMG_NAME"],
                )

                build_str = self.add_build_ci_env(build_str, c_comp)

                if i == 0:
                    final_str += build_str
                else:
                    build_str = "\n" + build_str
                    final_str += build_str

        return final_str

    def generate_kubepipe_conf(self, path):
        """Configuration on deploy-pipe and deploy stage.

        Deploy-pipe stage use kubepipe template for training.
        Deploy stage use kfserving template for inference.
        Both templates contain variables will be changed into params values.

        Args:
            path (str): Path of kubepipe or kfserving template.

        Returns:
            str: Final configuration of kubepipe or kfserving.

        """
        with open(path, "r") as rfile:
            kpipe_str = rfile.read()
            kpipe_str_len = len(kpipe_str)
            kpipe_str = kpipe_str[: kpipe_str_len - 1]

            kpipe_str = kpipe_str.format(
                stage_name=self.params["PIPE_NAME"],
                params_path=self.params_path
            )

        return kpipe_str

    def generate_stage_conf(self):
        """Load main of gitlab-ci template.

        It contains of build_content and kubepipe_content variables.
        Both contents contain of build, deploy-pipe, and deploy stage config.

        Returns:
            str: content of gitlab-ci main template.

        """
        with open(self.main_ci_template, "r") as rfile:
            stage_str = rfile.read()

        return stage_str

    def generate_ci_conf(self, filepath):
        """All processes of modifying gitlab-ci config.

        First, load all template of part of gitlab-ci config.
        Second, modify all variables with params values.
        Third, add string as additional variables on gcloud build if any
        Last, combine all part of gitlab-ci and create gitlab-ci.yaml file

        Args:
            filepath (str): Filename of gitlab-ci config.

        """
        stage_str = self.generate_stage_conf()
        build_str = self.generate_ci_build_conf()

        if self.params["PIPE_TYPE"] == "kfpipe":
            kpipe_str = self.generate_kubepipe_conf(self.kubepipe_template)
        elif self.params["PIPE_TYPE"] == "kfserving":
            kpipe_str = self.generate_kubepipe_conf(self.kfserve_template)

        final_str = stage_str.format(
            build_content=build_str, kubepipe_content=kpipe_str
        )

        if not os.path.exists(self.params["LOCAL_SRC"]):
            os.makedirs(self.params["LOCAL_SRC"])

        target_path = "{local_src}/{filepath}".format(
            local_src=self.params["LOCAL_SRC"], filepath=filepath
        )
        with open(target_path, "w") as wfile:
            wfile.write(final_str)

        click.echo(
            "\ncreating {filepath} to {target_path}...".format(
                filepath=filepath, target_path=target_path
            )
        )

    def add_cloudbuild_ci_env(self, cloud_str, c_comp):
        """Modify cloudbuild template on substitutions and build-args.

        Before use var on docker, you have add var on cloudbuild.
        New variables additional command is added on both section.

        Args:
            cloud_str (str): Content of cloudbuild template.
            c_comp (dict): Attributes of component.

        Returns:
            str: Final modification of cloudbuild config.

        """
        split_str = cloud_str.split("\n")
        subs_keys = []
        new_args = []

        try:
            for env_var in c_comp["CI_ENV"]:
                subs_key = "{space}_{key}: {value}".format(
                    key=env_var, value=env_var, space=" " * 4
                )
                new_arg = "{space}'--build-arg', \
                '{key}=${{_{value}}}',".format(
                    key=env_var, value=env_var, space=" " * 11
                )

                subs_keys.append(subs_key)
                new_args.append(new_arg)

            split_str[9:9] = subs_keys
            split_str[3:3] = new_args
            cloud_str = "\n".join(split_str)

            return cloud_str
        except KeyError:
            return cloud_str

    def generate_cloudbuild(self, filepath):
        """All processes of modifying cloudbuild config.

        First, load cloudbuild template.
        Second, add new var additional command if any.
        Last, create all cloudbuild.yaml file on each component.

        Args:
            filepath (str): Filename of cloudbuild config.

        """
        for i, c_comp in enumerate(self.params["COMPONENTS"]):
            with open(self.cloudbuild_template, "r") as rfile:
                cloud_str = rfile.read()
                cloud_str = self.add_cloudbuild_ci_env(cloud_str, c_comp)

                target_path = "{local_src}/{comp_path}".format(
                    local_src=self.params["LOCAL_SRC"],
                    comp_path=c_comp["COMP_PATH"]
                )

                if not os.path.exists(target_path):
                    os.makedirs(target_path)

                target_file = "{target_path}/{filepath}".format(
                    target_path=target_path, filepath=filepath
                )
                with open(target_file, "w") as wfile:
                    wfile.write(cloud_str)

                click.echo(
                    "\ncreating {filepath} to {target_path}...".format(
                        filepath=filepath, target_path=target_path
                    )
                )

    def read_dockerfile(self, path):
        """Load existing dockerfile on component.

        Args:
            path (str): Location of component dockerfile.

        Returns:
            str: Content of component dockerfile.

        """
        with open(path, "r") as rfile:
            content = rfile.read()
            content = content.split("\n")

        return content

    def write_dockerfile(self, path, content):
        """Create existing dockerfile after modifying content.

        Args:
            path (str): Target location of modified dockerfile.
            content (str): Final content of dockerfile after modified.

        """
        with open(path, "w") as wfile:
            wfile.write(content)

    def add_dockerfile_env(self, dock_cont, c_comp):
        """Modify dockerfile configuration.

        Setting workdir, add source code, and env variables.

        Args:
            dock_cont (str): Description of parameter `dock_cont`.
            c_comp (dict): Attributes of component.

        Returns:
            str: Dockerfile content after modified.

        """
        envs = ["ENV PARAMS_PATH=params.yml"]
        workdirs = [
            "WORKDIR {workdir}".format(workdir=c_comp["DOCKER_WORKDIR"]),
            "ADD {comp_path} {workdir}".format(
                workdir=c_comp["DOCKER_WORKDIR"], comp_path=c_comp["COMP_PATH"]
            ),
            "ADD params.yml {workdir}/params.yml".format(
                workdir=c_comp["DOCKER_WORKDIR"]
            ),
        ]

        dock_cont = self.check_workdir_ci(dock_cont, c_comp["DOCKER_WORKDIR"])

        try:
            for env_var in c_comp["CI_ENV"]:
                dock_arg = "ARG {arg}".format(arg=env_var)
                dock_env = "ENV {key}=${{{value}}}".format(
                    key=env_var, value=env_var
                )

                envs += [dock_arg, dock_env]
        except KeyError:
            print("There are no CI environment variables...")

        for env_var in envs:
            dock_cont = self.check_dockerfile_ci_env(dock_cont, env_var)

        all_new_cont = envs + workdirs
        dock_cont[1:1] += all_new_cont

        dock_cont = self.normalize_new_line(dock_cont)
        dock_cont = "\n".join(dock_cont)
        dock_cont += "\n"

        return dock_cont

    def normalize_new_line(self, dock_cont):
        """Automatically fix space on dockerfile content.

        Args:
            dock_cont (str): dockerfile content after modified.

        Returns:
            str: dockerfile content after fix space.

        """
        new_cont = []

        for i, cont in enumerate(dock_cont):
            if i == 0:
                new_cont.append(cont)
                continue

            if cont[0] == " ":
                new_cont.append(cont)
            else:
                new_cont += ["", cont]

        return new_cont

    def check_workdir_ci(self, dock_cont, re_filter):
        """Check if any workdir config on dockerfile.

        Fix workdir component whatever exist or not.

        Args:
            dock_cont (str): content of dockerfile template.
            re_filter (str): string for regex filter.

        Returns:
            list: list of new content for dockerfile.

        """
        new_cont = []

        for cont in dock_cont:
            if cont == "":
                continue
            split_cont = cont.split(" ")

            if (
                split_cont[0] == "WORKDIR"
                or split_cont[0] == "ADD"
                or split_cont[0] == "COPY"
            ):

                r = re.compile(re_filter)
                con_filters = list(filter(r.match, split_cont))

                if len(con_filters) == 0:
                    new_cont.append(cont)
            else:
                new_cont.append(cont)

        return new_cont

    def check_dockerfile_ci_env(self, dock_cont, dock_fltr):
        """Check if any env variables config on dockerfile.

        Fix env variables component whatever exist or not.

        Args:
            dock_cont (str): content of dockerfile template.
            re_filter (str): string for regex filter.

        Returns:
            list: list of new content for dockerfile.

        """
        new_cont = []

        for cont in dock_cont:
            if cont == "":
                continue
            if cont != dock_fltr and cont != dock_fltr.strip("{}"):
                new_cont.append(cont)

        return new_cont

    def generate_dockerfile(self):
        """All processes of modifying dockerfile content."""
        try:
            for c_comp in self.params["COMPONENTS"]:
                local_docker = "{local_src}/{comp_path}/Dockerfile".format(
                    local_src=self.params["LOCAL_SRC"],
                    comp_path=c_comp["COMP_PATH"]
                )

                if not os.path.exists(local_docker):
                    dock_cont = ["FROM python:3.7"]
                else:
                    dock_cont = self.read_dockerfile(local_docker)

                dock_cont = self.add_dockerfile_env(dock_cont, c_comp)
                self.write_dockerfile(local_docker, dock_cont)

        except KeyError:
            print("this pipeline haven't any components...")

    def main(self):
        """Generate all component configuration."""
        self.generate_ci_conf(".gitlab-ci.yml")
        self.generate_cloudbuild("cloudbuild.yaml")
        self.generate_dockerfile()


@click.command()
def main():
    """Entrypoint of kubextract."""
    args = prompt(QUES)
    gen = GenerateFrame(params_path=args["params_path"])
    gen.main()


if __name__ == "__main__":
    main(prog_name="kubextract")
