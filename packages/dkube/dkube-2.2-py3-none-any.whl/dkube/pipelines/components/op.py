import os

import kfp
from kubernetes.client.models import V1EnvVar


class DkubeOp(kfp.dsl.ContainerOp):
    _DISABLE_REUSABLE_COMPONENT_WARNING = True

    def __init__(self, name, authtoken, stage, args=[]):
        VALID_STAGES = ["training", "preprocessing", "serving", "storage", "submit"]

        assert (
            stage in VALID_STAGES
        ), "stage must be one of training/preprocessing/serving/storage/submit"

        kwargs = {"name": name, "image": "ocdr/dkube_pylauncher:2.2"}
        kwargs["command"] = ["python3", "/dkubepl/main.py", name, authtoken]
        kwargs["command"].extend(["{{workflow.uid}}", "{{pod.name}}", stage])
        kwargs["arguments"] = args

        super().__init__(**kwargs)

        if stage in ["training", "preprocessing", "serving"]:
            self.add_pod_label(name="platform", value="Dkube")
        self.add_pod_label(name="dkube.garbagecollect", value="true")
        self.add_pod_label(name="dkube.garbagecollect.policy", value="all")
        self.add_pod_label(name="stage", value=stage)
        self.add_pod_label(name="runid", value="{{pod.name}}")
        self.add_pod_label(name="wfid", value="{{workflow.uid}}")
        env_var = V1EnvVar(
            name="DKUBE_OP_DEBUG", value=os.environ.get("DKUBE_OP_DEBUG", "0")
        )
        self.add_env_variable(env_var)
