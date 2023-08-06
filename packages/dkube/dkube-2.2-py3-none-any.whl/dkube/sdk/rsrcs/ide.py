from __future__ import print_function
import time
import sys

from dkube.sdk.internal import dkube_api
from dkube.sdk.internal.dkube_api.rest import ApiException
from dkube.sdk.internal.dkube_api.models.job_model import JobModel
from dkube.sdk.internal.dkube_api.models.job_model_parameters import JobModelParameters
from dkube.sdk.internal.dkube_api.models.ds_job_model import DSJobModel
from dkube.sdk.internal.dkube_api.models.ds_job_model_executor import DSJobModelExecutor
from dkube.sdk.internal.dkube_api.models.dkube_container_model import DkubeContainerModel
from dkube.sdk.internal.dkube_api.models.dkube_container_model_framework import DkubeContainerModelFramework
from dkube.sdk.internal.dkube_api.models.dkube_container_model_framework_details import DkubeContainerModelFrameworkDetails
from dkube.sdk.internal.dkube_api.models.job_datum_model import JobDatumModel
from dkube.sdk.internal.dkube_api.models.job_datum_model_workspace import JobDatumModelWorkspace
from dkube.sdk.internal.dkube_api.models.job_input_datum_model import JobInputDatumModel
from dkube.sdk.internal.dkube_api.models.job_model_parameters_run import JobModelParametersRun
from dkube.sdk.internal.dkube_api.models.ds_job_model_hyperparams import DSJobModelHyperparams
from dkube.sdk.internal.dkube_api.models.custom_kv_model import CustomKVModel
from dkube.sdk.internal.dkube_api.models.config_file_model import ConfigFileModel
from dkube.sdk.internal.dkube_api.models.custom_container_model import CustomContainerModel
from dkube.sdk.internal.dkube_api.models.custom_container_model_image import CustomContainerModelImage
from dkube.sdk.internal.dkube_api.models.ds_job_model_hptuning import DSJobModelHptuning
from pprint import pprint

from .util import *


class DkubeIDE(object):

    FRAMEWORK_OPTS = ["custom", "tensorflow_1.14", "tensorflow_2.0",
                      "pytorch_2.6", "scikit_0.2.2"]

    def __init__(self, user, name=generate('notebook'), description='', tags=[]):
        self.repo = JobInputDatumModel  # class assignment, caller creates objects

        self.dkube_framework_details = DkubeContainerModelFrameworkDetails(
            version='v1.14')
        self.executor_dkube_framework = DkubeContainerModelFramework(
            choice='tensorflow', details=self.dkube_framework_details)
        self.executor_dkube = DkubeContainerModel(
            framework=self.executor_dkube_framework)
        self.custom_container = CustomContainerModelImage(
            path='', username=None, password=None, runas=None)
        self.executor_custom = CustomContainerModel(
            image=self.custom_container)
        self.executor_def = DSJobModelExecutor(
            choice='dkube', dkube=self.executor_dkube, custom=self.executor_custom)
        self.input_project_data = JobInputDatumModel(
            name=None, version=None, mountpath=None)
        self.input_project = JobDatumModelWorkspace(
            data=self.input_project_data, script=None)
        self.output_models = []
        self.input_datasets = []
        self.input_datums = JobDatumModel(
            workspace=self.input_project, datasets=self.input_datasets, outputs=self.output_models)
        self.customkv = CustomKVModel()
        self.configfile = ConfigFileModel()
        self.customenv = []
        self.hyperparameters = DSJobModelHyperparams(
            file=self.configfile, custom=self.customenv)
        self.hptuning = DSJobModelHptuning()
        self.notebook_def = DSJobModel(executor=self.executor_def, datums=self.input_datums,
                                       rdma=False, hyperparams=self.hyperparameters, hptuning=self.hptuning)
        self.run_def = JobModelParametersRun(template=None, group='default')
        self.job_parameters = JobModelParameters(
            _class='notebook', notebook=self.notebook_def, run=self.run_def)
        self.job = JobModel(name=None, parameters=self.job_parameters)

        self.update_basic(user, name, description, tags)

    def update_basic(self, user, name, description, tags):
        tags = list_of_strs(tags)

        self.user = user
        self.name = name

        self.job.name = name
        self.job.description = description
        self.notebook_def.tags = tags

        # Defaults
        self.dkube_framework_details.version = '1.14'
        self.executor_def.custom = None
        self.input_project.script = 'python model.py'
        return self

    def update_group(self, group='default'):
        self.run_def.group = group

    def update_container(self, framework=FRAMEWORK_OPTS[0],
                         image_url="", login_uname="", login_pswd=""):

        framework = framework.lower()
        framework_opts = DkubeIDE.FRAMEWORK_OPTS
        assert framework in framework_opts, "Invalid choice for framework, select oneof(" + str(
            framework_opts) + ")"

        if framework == "custom":
            framework_str = "custom"
            version_str = ""
        else:
            framework_str = framework.split("_")[0]
            version_str = framework.split("_")[1]

        self.executor_dkube_framework.choice = framework_str
        self.dkube_framework_details.version = version_str

        self.dkube_framework_details.image = image_url
        self.dkube_framework_details.username = login_uname
        self.dkube_framework_details.password = login_pswd
        self.dkube_framework_details.private = False

        if login_uname != "":
            self.dkube_framework_details.private = True
        return self

    def update_startupscript(self, startup_script=None):
        self.input_project.script = startup_script
        return self

    def add_envvar(self, key, value):
        self.customenv.append(str(dict(key=value)))
        return self

    def add_code(self, name, commitid=None):
        name = self.user + ':' + name
        self.input_project_data.name = name
        self.input_project_data.version = commitid

    def add_input_dataset(self, name, version=None, mountpath=None):
        name = self.user + ':' + name
        repo = self.repo(name=name, version=version, mountpath=mountpath)
        self.input_datasets.append(repo)

    def add_input_model(self, name, version=None, mountpath=None):
        name = self.user + ':' + name
        repo = self.repo(name=name, version=version, mountpath=mountpath)
        self.input_models.append(repo)

    def add_output_model(self, name, version=None, mountpath=None):
        name = self.user + ':' + name
        repo = self.repo(name=name, version=version, mountpath=mountpath)
        self.output_models.append(repo)

    def update_config_file(self, name, body=None):
        self.configfile.name = name
        self.configfile.body = body

    def update_hptuning(self, name, body=None):
        self.hptuning.name = name
        self.hptuning.body = body

    def update_resources(self, cpus=None, mem=None, ngpus=0):
        self.notebook_def.ngpus = ngpus
