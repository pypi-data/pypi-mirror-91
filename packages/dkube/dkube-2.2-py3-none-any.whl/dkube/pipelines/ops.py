"""

.. module:: DKubePiplineOps
   :synopsis: Defines pipeline components for dkube ops. Pipeline writer can use these ops to write and submit jobs to DKube platform.

.. moduleauthor:: Ahmed Khan <github.com/mak-454>

"""

import json

from dkube.sdk import DkubePreprocessing, DkubeServing, DkubeTraining, generate

from .components import DkubeOp


def dkube_training_op(
    name=generate("training"), authtoken=None, training=DkubeTraining
):

    """
    DKube Op to define a training job as a stage in pipeline.
    When run this op submits a job on DKube platform and waits for it to be completed.

    *Inputs*

        name
            Name of the stage. The passed name will be set as display_name for the stage.

        authtoken
            API authentication token. User can get this find under DeveloperSettings in DKube UI.

        training
            Instance of :bash:`dkube.sdk.rsrcs.DkubeTraining` class.
            All the properties of the job can defined in this object.
    """

    assert (
        type(training) == DkubeTraining
    ), "Invalid type for training argument, must be instance of dkube.sdk.rsrcs:DkubeTraining"
    assert authtoken is not None, "Auth token is must"

    return DkubeOp(
        name, authtoken, "training", args=[json.dumps(training.job.to_dict())]
    )


def dkube_preprocessing_op(
    name=generate("data"), authtoken=None, preprocessing=DkubePreprocessing
):

    """
    DKube Op to define a preprocessing job as a stage in pipeline.
    When run this op submits a job on DKube platform and waits for it to be completed.

    *Inputs*

        name
            Name of the stage. The passed name will be set as display_name for the stage.

        authtoken
            API authentication token. User can get this find under DeveloperSettings in DKube UI.

        preprocessing
            Instance of :bash:`dkube.sdk.rsrcs.DkubePreprocessing` class.
            All the properties of the job can defined in this object.
    """

    assert (
        type(preprocessing) == DkubePreprocessing
    ), "Invalid type for preprocessing argument, must be instance of dkube.sdk.rsrcs:DkubePreprocessing"
    assert authtoken is not None, "Auth token is must"

    return DkubeOp(
        name, authtoken, "preprocessing", args=[json.dumps(preprocessing.job.to_dict())]
    )


def dkube_serving_op(name=generate("serving"), authtoken=None, serving=DkubeServing):

    """
    DKube Op to deploy a model for serving in a stage in pipeline.
    When run this op submits a job on DKube platform and waits for it to be deployed.

    *Inputs*

        name
            Name of the stage. The passed name will be set as display_name for the stage.

        authtoken
            API authentication token. User can get this find under DeveloperSettings in DKube UI.

        serving
            Instance of :bash:`dkube.sdk.rsrcs.DkubeServing` class.
            All the properties of the job can defined in this object.
    """

    assert (
        type(serving) == DkubeServing
    ), "Invalid type for serving argument, must be instance of dkube.sdk.rsrcs:DkubeServing"
    assert authtoken is not None, "Auth token is must"

    return DkubeOp(name, authtoken, "serving", args=[json.dumps(serving.job.to_dict())])


def dkube_storage_op(name=generate("storage"), authtoken=None, command=None, claims=[]):
    """
    DKube Op to export dkube resoources as a kubernetes volume claim.

    *Inputs*

        name
            Name of the stage. The passed name will be set as display_name for the stage.

        authtoken
            API authentication token. User can get this find under DeveloperSettings in DKube UI.

        command
            "export" or "reclaim". "export" would exports the given volume requests. "reclaim" would
            delete any volume claim created in this pipeline

        claims
            List of Instance of :bash:`dkube.sdk.rsrcs.DkubeResourcePVC` class.

    """
    assert command is not None, "command is required"
    assert authtoken is not None, "Auth token is must"

    claims = [
        {"volume": claim.volume.to_dict(), "kind": claim.kind} for claim in claims
    ]
    return DkubeOp(
        name, authtoken, "storage", args=[command, "kubeflow", json.dumps(claims)]
    )


def dkube_submit_op(
    name=generate("submit"), authtoken=None, project_id=None, predictions=None
):
    """
    DKube Op to submit predictions to project leaderboard.

    *Inputs*

        name
            Name of the stage. The passed name will be set as display_name for the stage.

        authtoken
            API authentication token. User can get this find under DeveloperSettings in DKube UI.

        project_id
            ID of the project to which this submission would be done

        predictions
            prediction output from previous kubeflow component

    """
    assert project_id is not None, "project_id is required"
    assert authtoken is not None, "Auth token is must"
    assert predictions is not None, "predictions is required"

    return DkubeOp(name, authtoken, "submit", args=[project_id, predictions])
