from kubextract.utils.generate import GenerateFrame
import ruamel.yaml as yaml
import re
import os


class CheckKubeFiles:
    """Testing Scenario for kubextract.

    Args:
        params_path (str): location of component params.

    Attributes:
        params (dict): List of component params.
        trgt_base (str): base target path for generate framework.
        params_path

    """

    def __init__(self, params_path=None):
        """Construct for storing class attributes.

        Args:
            params_path (str): location of component params.

        """
        self.params = self.load_params(params_path)
        self.params_path = params_path
        self.trgt_base = self.params["LOCAL_SRC"]

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

    def read_file(self, path):
        """Read content file.

        Args:
            path (str): Location of file.

        Returns:
            list: List of content file.

        """
        with open(path, "r") as stream:
            data = stream.read()
            split_data = data.split("\n")

        return split_data

    def check_params_on_file(
            self, filename=None,
            comp_path=None, contents=None):
        """Check every params value of each config file.

        Args:
            filename (str): name of config file.
            comp_path (str): location of component path.
            contents (list): List of content that will be checked.

        """
        if comp_path is not None:
            trgt_file = "{trgt_base}/{comp_path}/{filename}".format(
                trgt_base=self.trgt_base, comp_path=comp_path,
                filename=filename
            )
        else:
            trgt_file = "{trgt_base}/{filename}".format(
                trgt_base=self.trgt_base, filename=filename
            )

        trgt_data = self.read_file(trgt_file)

        for cont in contents:
            status = []

            for value in trgt_data:
                print((cont, value))
                fltrs = re.findall(cont, value)

                if len(fltrs) > 0:
                    status.append(True)

            assert len(status) > 0

    def main(self):
        """List all content will be checked and check each files."""
        gen = GenerateFrame(params_path=self.params_path)
        gen.main()

        for comp in self.params["COMPONENTS"]:
            dock_content = []
            cb_content = []
            ci_content = [
                "build_{stage_name}".format(
                    stage_name=comp["STAGE_NAME"]
                ),
                "{local_src}/{comp_path}/cloudbuild.yaml".format(
                    local_src=self.params["LOCAL_SRC"],
                    comp_path=comp["COMP_PATH"]
                ),
                "_LOCAL_SRC={local_src}".format(
                    local_src=self.params["LOCAL_SRC"]
                ),
                "{local_src}/{comp_path}/Dockerfile".format(
                    local_src=self.params["LOCAL_SRC"],
                    comp_path=comp["COMP_PATH"]
                ),
                "{img_registry}/{img_name}".format(
                    img_registry=self.params["IMAGE_REGISTRY"],
                    img_name=comp["IMG_NAME"]
                ),
                "kubepipe_{pipe_name}".format(
                    pipe_name=self.params["PIPE_NAME"]
                ),
                "PARAMS_PATH={params_path}".format(
                    params_path=self.params_path
                )
            ]

            self.check_params_on_file(
                filename=".gitlab-ci.yml", contents=ci_content
            )

            try:
                for env_var in comp["CI_ENV"]:
                    cb_content.append(
                        "{env_var}=${{_{env_var}}}".format(
                            env_var=env_var
                        )
                    )
                    cb_content.append(
                        "_{env_var}: {env_var}".format(
                            env_var=env_var
                        )
                    )

                    self.check_params_on_file(
                        filename="cloudbuild.yaml",
                        comp_path=comp["COMP_PATH"],
                        contents=cb_content,
                    )

                    dock_content.append(
                        "ARG {env_var}".format(
                            env_var=env_var
                        )
                    )
                    dock_content.append(
                        "ENV {env_var}=${{{env_var}}}".format(
                            env_var=env_var
                        )
                    )
            except Exception:
                print("There's no CI_ENV")

            dock_content.append(
                "WORKDIR {doc_workdir}".format(
                    doc_workdir=comp["DOCKER_WORKDIR"]
                )
            )
            dock_content.append(
                "ADD {comp_path} {doc_workdir}".format(
                    comp_path=comp["COMP_PATH"],
                    doc_workdir=comp["DOCKER_WORKDIR"]
                )
            )
            dock_content.append(
                "ADD params.yml {doc_workdir}/params.yml".format(
                    doc_workdir=comp["DOCKER_WORKDIR"]
                )
            )

            self.check_params_on_file(
                filename="Dockerfile",
                comp_path=comp["COMP_PATH"],
                contents=dock_content,
            )


class TestAllScenario:
    """All scenario pytest."""

    def test_mnist_comp(self):
        """Check mnist component generation."""
        dir_name = os.path.dirname(os.path.abspath(__file__))
        dir_name = dir_name.replace("utils-test", "params")
        mnist_path = os.path.join(dir_name, "mnist.yml")

        check_files = CheckKubeFiles(params_path=mnist_path)
        check_files.main()

    def test_markdown_comp(self):
        """Check markdown component generation."""
        dir_name = os.path.dirname(os.path.abspath(__file__))
        dir_name = dir_name.replace("utils-test", "params")
        markdown_path = os.path.join(dir_name, "markdown.yml")

        check_files = CheckKubeFiles(params_path=markdown_path)
        check_files.main()
