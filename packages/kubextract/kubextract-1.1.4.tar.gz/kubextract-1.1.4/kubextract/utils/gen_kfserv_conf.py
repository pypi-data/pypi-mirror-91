import ruamel.yaml as yaml
import os


class GenerateMeta:
    """Create kfserving configuration for deploy inference.

    Args:
        params_path (str): location of component params.

    Attributes:
        params (dict): List of component params.

    """

    def __init__(self, params_path=None):
        """Construct for storing class attributes.

        Args:
            params_path (str): location of component params.

        """
        self.params = self.load_params(params_path)

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

    def construct_yaml_str(self):
        """Modifying kfserving content.

        Returns:
            str: Content of kfserving file.

        """
        content = """
            apiVersion: serving.kubeflow.org/v1alpha2
            kind: InferenceService
            metadata:
              namespace: kubeflow
              labels:
                controller-tools.k8s.io: "1.0"
              name: {pipe_name}
              nodeSelector:
                {node_key}: {node_val}
            spec:
              default:
                predictor:
                  custom:
                    container:
                      image: {image_registry}/{img_name}:{tag}

        """.format(
            pipe_name=self.params["PIPE_NAME"],
            node_key=self.params["NODE_KEY"],
            node_val=self.params["NODE_VAL"],
            image_registry=self.params["IMAGE_REGISTRY"],
            img_name=self.params["IMG_NAME"],
            tag=os.getenv("CI_COMMIT_REF_NAME"),
        )

        return content

    def main(self):
        """All process modifying kfserving config file."""
        with open(os.getenv("KFSERVING_CONFIG"), "w") as outfile:
            content = self.construct_yaml_str()
            yaml_cont = yaml.load(content)
            yaml.dump(yaml_cont, outfile, default_flow_style=False)


if __name__ == "__main__":
    gen_meta = GenerateMeta(params_path=os.getenv("PARAMS_PATH"))
    gen_meta.main()
