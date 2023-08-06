from __future__ import print_function

import sys
import time
from pprint import pprint

from dkube.sdk.internal import dkube_api
from dkube.sdk.internal.dkube_api.models.custom_container_model import \
    CustomContainerModel
from dkube.sdk.internal.dkube_api.models.custom_container_model_image import \
    CustomContainerModelImage
from dkube.sdk.internal.dkube_api.models.inference_job_model import \
    InferenceJobModel
from dkube.sdk.internal.dkube_api.models.job_model import JobModel
from dkube.sdk.internal.dkube_api.models.job_model_parameters import \
    JobModelParameters
from dkube.sdk.internal.dkube_api.models.job_model_parameters_run import \
    JobModelParametersRun
from dkube.sdk.internal.dkube_api.rest import ApiException

from .util import *


class DkubeServing(object):

    def __init__(self, user, name=generate('serving'), description='', tags=[]):
        self.predictor_container = CustomContainerModelImage(
            path='', username=None, password=None, runas=None)
        self.predictor = CustomContainerModel(image=None)
        self.transformer_container = CustomContainerModelImage(
            path='', username=None, password=None, runas=None)
        self.transformer = CustomContainerModel(image=None)

        self.serving_def = InferenceJobModel(model=None, version=None, owner=None, device=None, deploy=None,
                                             serving_image=self.predictor, transformer=False,
                                             transformer_image=self.transformer, transformer_project=None,
                                             transformer_commit_id=None, transformer_code=None)
        self.run_def = JobModelParametersRun(template=None, group='default')
        self.job_parameters = JobModelParameters(
            _class='inference', inference=self.serving_def, run=self.run_def)
        self.job = JobModel(name=None, parameters=self.job_parameters)

        self.update_basic(user, name, description, tags)

    def update_basic(self, user, name, description, tags):
        tags = list_of_strs(tags)

        self.user = user
        self.name = name
        self.description = description

        self.job.name = name
        self.job.description = description
        self.serving_def.tags = tags
        self.serving_def.device = "cpu"
        self.serving_def.transformer = False

    def set_transformer(self, transformer: bool=False, script=None):
        self.serving_def.transformer = transformer
        self.serving_def.transformer_code = script

    def update_transformer_code(self, code=None, commitid=None):
        self.serving_def.transformer_project = self.user + ':' + code
        self.serving_def.transformer_commit_id = commitid

    def update_transformer_image(self, image_url=None, login_uname=None, login_pswd=None):
        self.transformer_container.path = image_url
        self.transformer_container.username = login_uname
        self.transformer_container.password = login_pswd
        self.transformer.image = self.transformer_container

    def update_serving_model(self, model, version=None):
        self.serving_def.model = model
        self.serving_def.version = version
        self.serving_def.owner = self.user

    def update_serving_image(self, deploy=None, image_url=None, login_uname=None, login_pswd=None):
        self.predictor_container.path = image_url
        self.predictor_container.username = login_uname
        self.predictor_container.password = login_pswd
        self.serving_def.deploy = deploy
        self.predictor.image = self.predictor_container
