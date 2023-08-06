import os
import kfp.dsl as dsl
import ruamel.yaml as yaml
from kfp.compiler import Compiler
from kubextract.utils.watcher import RunPipe

with open(os.getenv("PARAMS_PATH"), "r") as stream:
    PARAMS = yaml.safe_load(stream)


def create_comp(c_params):
    """Create configuration of component on kubeflow pipeline.

    Args:
        c_params (dict): Attributes of component.

    Returns:
        obj: Container object.

    """
    try:
        pipe_out = c_params["PIPE_OUTPUT"]
    except KeyError:
        pipe_out = {}

    return dsl.ContainerOp(
        name=c_params["COMP_NAME"],
        image="{img_reg}/{img_name}:{tag}".format(
            img_reg=PARAMS["IMAGE_REGISTRY"],
            img_name=c_params["IMG_NAME"],
            tag=os.getenv("CI_COMMIT_REF_NAME"),
        ),
        file_outputs=pipe_out,
    )


@dsl.pipeline(name=PARAMS["PIPE_NAME"], description=PARAMS["PIPE_DESC"])
def cluster_pipeline():
    """Create component flow on kubeflow pipeline."""
    for c_params in PARAMS["COMPONENTS"]:
        if c_params["USE_GPU"]:
            prep_op = create_comp(c_params).set_gpu_limit(1)
        else:
            prep_op = create_comp(c_params)

        prep_op.add_node_selector_constraint(
            c_params["NODE_KEY"], c_params["NODE_VAL"]
        )
        prep_op.set_image_pull_policy("Always")


def main():
    """Entrypoint of pipeline."""
    Compiler().compile(cluster_pipeline, PARAMS["PIPE_PATH"])

    gen_pipe = RunPipe(params=PARAMS)
    gen_pipe.main()


if __name__ == "__main__":
    main()
