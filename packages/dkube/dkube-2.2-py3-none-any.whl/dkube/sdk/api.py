"""

.. module:: DKubeAPI
   :synopsis: Helper class which provides high level methods for user to integrate at workflow level.

.. moduleauthor:: Ahmed Khan <github.com/mak-454>


"""

import json
import os
import time
import pandas as pd

import urllib3
from dkube.sdk.internal.api_base import *
from dkube.sdk.internal.dkube_api.models.conditions import \
    Conditions as TriggerCondition
from dkube.sdk.internal.files_base import *
from dkube.sdk.rsrcs import *
from dkube.sdk.rsrcs.featureset import DkubeFeatureSet, DKubeFeatureSetUtils
from dkube.sdk.rsrcs.project import DkubeProject

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DkubeApi(ApiBase, FilesBase):

    """

        This class encapsules all the high level dkube workflow functions.::

            from dkube.sdk import *
            dapi = DkubeApi()

        *Inputs*

            URL
                FQDN endpoint at which DKube platform is deployed::

                    http://dkube-controller-master.dkube.cluster.local:5000

                    https://dkube.ai:32222

                .. note:: If not provided then the value is picked from *DKUBE_ACCESS_URL* env variable. If not found then http://dkube-controller-master.dkube.cluster.local:5000 is used assuming the access is internal to the DKube cluster


            token
                Access token for the APIs, without which DKube will return 40x codes

                .. note:: If not provided then the value is picked from *DKUBE_ACCESS_TOKEN* env variable. ASSERTs if env is not defined.


            common_tags
                Tags which need to applied all the resources created using this API object


            req_timeout
                Timeout for all the requests which are issued using this API object


            req_retries
                Number of retries per request

    """

    def __init__(self, URL=None, token=None, common_tags=[], req_timeout=None, req_retries=None):

        self.url = URL
        if self.url == None:
            self.url = os.getenv(
                "DKUBE_ACCESS_URL", "http://dkube-controller-master.dkube.svc.cluster.local:5000")
            self.files_url = os.getenv(
                "DKUBE_ACCESS_URL", "http://dkube-downloader.dkube.svc.cluster.local:9401")
        else:
            self.files_url = self.url

        self.token = token
        if self.token == None:
            self.token = os.getenv("DKUBE_ACCESS_TOKEN", None)
            assert self.token == None, "TOKEN must be specified either by passing argument or by setting DKUBE_ACCESS_TOKEN env variable"

        ApiBase.__init__(self, self.url, self.token, common_tags)
        FilesBase.__init__(self, self.files_url, self.token)
        self.wait_interval = 10

    def set_active_project(self, project_id):
        """
        Set active project. Any resources created using this API instance will belong to the given project.

        *Inputs*

            project_id
                ID of the project. pass None to unset.
        """
        self.common_tags = [
            tag for tag in self.common_tags if not tag.startswith("project:")
        ]
        if project_id:
            self.common_tags.append("project:" + str(project_id))
            
    def validate_token(self):
        """
            Method which can be used to validate the token.
            Returns the JWT Claims. Which contains the role assigned to the user.


        """

        return super().validate_token()

    def launch_jupyter_ide(self, ide: DkubeIDE, wait_for_completion=True):
        """
            Method to launch a Jupyter IDE on DKube platform. Two kinds of IDE are supported,
            Jupyter Notebook & RStudio.
            Raises Exception in case of errors.


            *Inputs*

                ide
                    Instance of :bash:`dkube.sdk.rsrcs.DkubeIDE` class.
                    Please see the :bash:`Resources` section for details on this class.


                wait_for_completion
                    When set to :bash:`True` this method will wait for job to complete after submission.
                    IDE is declared complete if it is one of the :bash:`running/failed/error` state

        """

        assert type(
            ide) == DkubeIDE, "Invalid type for run, value must be instance of rsrcs:DkubeIDE class"
        super().launch_jupyter_ide(ide)
        while wait_for_completion:
            status = super().get_ide('notebook', ide.user, ide.name, fields='status')
            state, reason = status['state'], status['reason']
            if state.lower() in ['running', 'failed', 'error']:
                print(
                    "IDE {} - completed with state {} and reason {}".format(ide.name, state, reason))
                break
            else:
                print(
                    "IDE {} - waiting for completion, current state {}".format(ide.name, state))
                time.sleep(self.wait_interval)

    def launch_rstudio_ide(self, ide: DkubeIDE, wait_for_completion=True):
        """
            Method to launch a Rstudio IDE on DKube platform. Two kinds of IDE are supported,
            Jupyter Notebook & RStudio.
            Raises Exception in case of errors.


            *Inputs*

                ide
                    Instance of :bash:`dkube.sdk.rsrcs.DkubeIDE` class.
                    Please see the :bash:`Resources` section for details on this class.


                wait_for_completion
                    When set to :bash:`True` this method will wait for job to complete after submission.
                    IDE is declared complete if it is one of the :bash:`running/failed/error` state

        """

        assert type(
            ide) == DkubeIDE, "Invalid type for run, value must be instance of rsrcs:DkubeIDE class"
        super().launch_rstudio_ide(ide)
        while wait_for_completion:
            status = super().get_ide('notebook', ide.user, ide.name, fields='status')
            state, reason = status['state'], status['reason']
            if state.lower() in ['running', 'failed', 'error']:
                print(
                    "IDE {} - completed with state {} and reason {}".format(ide.name, state, reason))
                break
            else:
                print(
                    "IDE {} - waiting for completion, current state {}".format(ide.name, state))
                time.sleep(self.wait_interval)

    def list_ides(self, user, filters='*'):
        """
            Method to list all the IDEs of a user.
            Raises exception on any connection errors.

            *Inputs*

                user
                    User whose IDE instances must be fetched.
                    In case of if token is of different user, then the token should have permission to fetch the
                    training runs of the :bash:`user` in the input. They should be in same DKube group.

                filters
                    Only :bash:`*` is supported now.

                    User will able to filter runs based on state or duration

        """

        return super().list_ides('notebook', user)

    def delete_ide(self, user, name):
        """
            Method tio delete an IDE.
            Raises exception if token is of different user or if training run with name doesnt exist or on any connection errors.

            *Inputs*

                user
                    The token must belong to this user. As IDE instance of different user cannot be deleted.

                name
                    Name of the IDE which needs to be deleted.

        """

        super().delete_ide('notebook', user, name)

    def create_training_run(self, run: DkubeTraining, wait_for_completion=True):
        """
            Method to create a training run on DKube.
            Raises Exception in case of errors.


            *Inputs*

                run
                    Instance of :bash:`dkube.sdk.rsrcs.Training` class.
                    Please see the :bash:`Resources` section for details on this class.


                wait_for_completion
                    When set to :bash:`True` this method will wait for job to complete after submission.
                    Job is declared complete if it is one of the :bash:`complete/failed/error` state

        """

        assert type(
            run) == DkubeTraining, "Invalid type for run, value must be instance of rsrcs:DkubeTraining class"
        super().update_tags(run.training_def)
        super().create_run(run)
        while wait_for_completion:
            status = super().get_run('training', run.user, run.name, fields='status')
            state, reason = status['state'], status['reason']
            if state.lower() in ['complete', 'failed', 'error']:
                print(
                    "run {} - completed with state {} and reason {}".format(run.name, state, reason))
                break
            else:
                print(
                    "run {} - waiting for completion, current state {}".format(run.name, state))
                time.sleep(self.wait_interval)

    def get_training_run(self, user, name):
        """
            Method to fetch the training run with given name for the given user.
            Raises exception in case of run is not found or any other connection errors.

            *Inputs*

                user
                    User whose training run has to be fetched.
                    In case of if token is of different user, then the token should have permission to fetch the
                    training run of the :bash:`user` in the input. They should be in same DKube group.

                name
                    Name of the training run to be fetched

        """

        return super().get_run('training', user, name)

    def list_training_runs(self, user, filters='*'):
        """
            Method to list all the training runs of a user.
            Raises exception on any connection errors.

            *Inputs*

                user
                    User whose training runs must be fetched.
                    In case of if token is of different user, then the token should have permission to fetch the
                    training runs of the :bash:`user` in the input. They should be in same DKube group.

                filters
                    Only :bash:`*` is supported now.

                    User will able to filter runs based on state or duration

        """

        return super().list_runs('training', user)

    def delete_training_run(self, user, name):
        """
            Method to delete a run.
            Raises exception if token is of different user or if training run with name doesnt exist or on any connection errors.

            *Inputs*

                user
                    The token must belong to this user. As run of different user cannot be deleted.

                name
                    Name of the run which needs to be deleted.

        """

        super().delete_run('training', user, name)

    def create_preprocessing_run(self, run: DkubePreprocessing, wait_for_completion=True):
        """
            Method to create a preprocessing run on DKube.
            Raises Exception in case of errors.


            *Inputs*

                run
                    Instance of :bash:`dkube.sdk.rsrcs.Preprocessing` class.
                    Please see the :bash:`Resources` section for details on this class.


                wait_for_completion
                    When set to :bash:`True` this method will wait for job to complete after submission.
                    Job is declared complete if it is one of the :bash:`complete/failed/error` state

        """

        assert type(
            run) == DkubePreprocessing, "Invalid type for run, value must be instance of rsrcs:DkubePreprocessing class"
        super().update_tags(run.pp_def)
        super().create_run(run)
        while wait_for_completion:
            status = super().get_run('preprocessing', run.user, run.name, fields='status')
            state, reason = status['state'], status['reason']
            if state.lower() in ['complete', 'failed', 'error']:
                print(
                    "run {} - completed with state {} and reason {}".format(run.name, state, reason))
                break
            else:
                print(
                    "run {} - waiting for completion, current state {}".format(run.name, state))
                time.sleep(self.wait_interval)

    def get_preprocessing_run(self, user, name):
        """
            Method to fetch the preprocessing run with given name for the given user.
            Raises exception in case of run is not found or any other connection errors.

            *Inputs*

                user
                    User whose preprocessing run has to be fetched.
                    In case of if token is of different user, then the token should have permission to fetch the
                    preprocessing run of the :bash:`user` in the input. They should be in same DKube group.

                name
                    Name of the training run to be fetched

        """

        return super().get_run('preprocessing', user, name)

    def list_preprocessing_runs(self, user, filters='*'):
        """
            Method to list all the preprocessing runs of a user.
            Raises exception on any connection errors.

            *Inputs*

                user
                    User whose preprocessing runs must be fetched.
                    In case of if token is of different user, then the token should have permission to fetch the
                    preprocessing runs of the :bash:`user` in the input. They should be in same DKube group.

                filters
                    Only :bash:`*` is supported now.

                    User will able to filter runs based on state or duration

        """

        return super().list_runs('preprocessing', user)

    def delete_preprocessing_run(self, user, name):
        """
            Method to delete a run.
            Raises exception if token is of different user or if preprocessing run with name doesnt exist or on any connection errors.

            *Inputs*

                user
                    The token must belong to this user. As run of different user cannot be deleted.

                name
                    Name of the run which needs to be deleted.

        """

        super().delete_run('preprocessing', user, name)

    def create_test_inference(self, run: DkubeServing, wait_for_completion=True):
        """
            Method to create a test inference on DKube.
            Raises Exception in case of errors.


            *Inputs*

                run
                    Instance of :bash:`dkube.sdk.rsrcs.serving` class.
                    Please see the :bash:`Resources` section for details on this class.

                    If serving image is not updated in :bash:`run:DkubeServing` argument then,
                    - If training used supported standard framework, dkube will pick approp serving image
                    - If training used custom image, dkube will try to use the same image for serving

                    If transformer image is not updated in :bash:`run:DkubeServing` then,
                    - Dkube will use same image as training image

                    If transformer code is not updated in :bash:`run:DkubeServing` then,
                    - Dkube will use the code used for training


                wait_for_completion
                    When set to :bash:`True` this method will wait for job to complete after submission.
                    Job is declared complete if it is one of the :bash:`complete/failed/error` state

        """

        assert type(
            run) == DkubeServing, "Invalid type for run, value must be instance of rsrcs:DkubeServing class"

        # Fetch training run details and fill in information for serving
        if run.predictor.image == None or (
                run.serving_def.transformer == True and run.transformer.image == None) or (
                run.serving_def.transformer == True and run.serving_def.transformer_project == None):

            if run.serving_def.version == None:
                v = self.get_model_latest_version(
                    run.serving_def.owner, run.serving_def.model)
                run.serving_def.version = v['uuid']

            li = self.get_model_lineage(
                run.serving_def.owner, run.serving_def.model, run.serving_def.version)
            if run.predictor.image == None:
                si = li['run']['parameters'][
                    'generated']['serving_image']['image']
                run.update_serving_image(
                    si['path'], si['username'], si['password'])

            if run.serving_def.transformer == True and run.transformer.image == None:
                ti = li['run']['parameters']['generated'][
                    'training_image']['image']
                run.update_transformer_image(
                    ti['path'], ti['username'], ti['password'])

            if run.serving_def.transformer == True and run.serving_def.transformer_project == None:
                code = li['run']['parameters']['training'][
                    'datums']['workspace']['data']
                name = code['name'].split(':')[1]
                run.update_transformer_code(name, code['version'])

        super().create_run(run)
        while wait_for_completion:
            status = super().get_run('inference', run.user, run.name, fields='status')
            state, reason = status['state'], status['reason']
            if state.lower() in ['complete', 'failed', 'error', 'running']:
                print(
                    "run {} - completed with state {} and reason {}".format(run.name, state, reason))
                break
            else:
                print(
                    "run {} - waiting for completion, current state {}".format(run.name, state))
                time.sleep(self.wait_interval)

    def get_test_inference(self, user, name):
        """
            Method to fetch the test inference with given name for the given user.
            Raises exception in case of run is not found or any other connection errors.

            *Inputs*

                user
                    User whose test inference has to be fetched.
                    In case of if token is of different user, then the token should have permission to fetch the
                    serving run of the :bash:`user` in the input. They should be in same DKube group.

                name
                    Name of the serving run to be fetched

        """

        return super().get_run('inference', user, name)

    def list_test_inferences(self, user, filters='*'):
        """
            Method to list all the training inferences of a user.
            Raises exception on any connection errors.

            *Inputs*

                user
                    User whose test inferences must be fetched.
                    In case of if token is of different user, then the token should have permission to fetch the
                    serving runs of the :bash:`user` in the input. They should be in same DKube group.

                filters
                    Only :bash:`*` is supported now.

                    User will able to filter runs based on state or duration

        """

        return super().list_runs('inference', user)

    def delete_test_inference(self, user, name):
        """
            Method to delete a test inference.
            Raises exception if token is of different user or if serving run with name doesnt exist or on any connection errors.

            *Inputs*

                user
                    The token must belong to this user. As run of different user cannot be deleted.

                name
                    Name of the run which needs to be deleted.

        """

        super().delete_run('inference', user, name)

    def create_code(self, code: DkubeCode, wait_for_completion=True):
        """
            Method to create a code repo on DKube.
            Raises Exception in case of errors.


            *Inputs*

                code
                    Instance of :bash:`dkube.sdk.rsrcs.code` class.
                    Please see the :bash:`Resources` section for details on this class.


                wait_for_completion
                    When set to :bash:`True` this method will wait for code resource to get into one of the complete state.
                    code is declared complete if it is one of the :bash:`complete/failed/error` state

        """

        assert type(
            code) == DkubeCode, "Invalid type for run, value must be instance of rsrcs:DkubeCode class"
        super().create_repo(code)
        while wait_for_completion:
            status = super().get_repo('program', code.user, code.name, fields='status')
            state, reason = status['state'], status['reason']
            if state.lower() in ['ready', 'failed', 'error']:
                print(
                    "code {} - completed with state {} and reason {}".format(code.name, state, reason))
                break
            else:
                print(
                    "code {} - waiting for completion, current state {}".format(code.name, state))
                time.sleep(self.wait_interval)

    def get_code(self, user, name):
        """
            Method to fetch the code repo with given name for the given user.
            Raises exception in case of code is not found or any other connection errors.

            *Inputs*

                user
                    User whose code has to be fetched.
                    In case of if token is of different user, then the token should have permission to fetch the
                    code of the :bash:`user` in the input. They should be in same DKube group.

                name
                    Name of the code repo to be fetched

        """

        return super().get_repo('program', user, name)

    def list_code(self, user, filters='*'):
        """
            Method to list all the code repos of a user.
            Raises exception on any connection errors.

            *Inputs*

                user
                    User whose projects must be fetched.
                    In case of if token is of different user, then the token should have permission to fetch the
                    projects of the :bash:`user` in the input. They should be in same DKube group.

                filters
                    Only :bash:`*` is supported now.

                    User will able to filter projects based on state or the source

        """

        return super().list_repos('program', user)

    def delete_code(self, user, name):
        """
            Method to delete a code repo.
            Raises exception if token is of different user or if code with name doesnt exist or on any connection errors.

            *Inputs*

                user
                    The token must belong to this user. As code of different user cannot be deleted.

                name
                    Name of the code which needs to be deleted.

        """

        super().delete_repo('program', user, name)

################### Feature Store ############################
    def create_featureset(self, featureset: DkubeFeatureSet):
        """
            Method to create a featureset on DKube.
            Raises Exception in case of errors.


            *Inputs*

                featureset
                    Instance of :bash:`dkube.sdk.rsrcs.featureSet` class.
                    Please see the :bash:`Resources` section for details on this class.

            *Outputs*

                A Json string with response status 

        """
        assert type(
            featureset) == DkubeFeatureSet, "Invalid type for run, value must be instance of rsrcs:DkubeFeatureset class"
        response = super().create_featureset(featureset)
        if response['code'] == 200 and featureset.featurespec_path is not None:
            spec_response = super().featureset_upload_featurespec(
                featureset.featureset.name, featureset.featurespec_path)
            if spec_response['code'] != 200:
                self.delete_featureset(featureset.featureset.name)
                return spec_response
        return response

    def delete_featuresets(self, featureset_list):
        """
            Method to delete a list of featuresets on DKube.
            Raises Exception in case of errors.

            *Inputs*

                featureset_list
                    list of featureset names
                    example: ["mnist-fs", "titanic-fs"]

            *Outputs*

                A Json string with response status with the list of deleted featureset names

        """
        assert (
            featureset_list
            and isinstance(featureset_list, list)
            and all(isinstance(featureset, str) for featureset in featureset_list)
        ), "Invalid parameter, value must be a list of featureset names"
        return super().delete_featureset(featureset_list)

    def delete_featureset(self, name):
        """
        Method to delete a a featureset on DKube.
        Raises Exception in case of errors.

        *Inputs*

            name
                featureset name to be deleted. 
                example: "mnist-fs"

        *Outputs*

            A dictionary with response status and the deleted featureset name

        """
        assert(
            name
            and isinstance(name, str)
        ), "Invalid parameter, value must be a featureset name"
        return super().delete_featureset([name])


    def commit_featureset(self, **kwargs):
        """
            Method to commit sticky featuresets.

            featureset should be in ready state. It will be in created state if no featurespec is uploaded. 
            If the featureset is in created state, the following will happen.
                a) If metadata is passed, it will be uploaded as featurespec
                b) If no metadata is passed, it derives from df and uploads it.
            If the featureset is in ready state, the following will happen.
                a) metadata if passed any will be ignored
                b) featurespec will be downloaded for the specifed featureset and df is validated for conformance.

            If name is specified, it derives the path for committing the features
            If path is also specified, it doesn't derive the path. It uses the specified path. However, path should a mount path into dkube store.

            *Inputs*

                name
                    featureset name or None
                    example: name='fset'
                df
                    Dataframe with features to be written
                    type: pandas.DataFrame
                metadata
                    optional yaml object with name, description and schema fields or None
                    example:metadata=[{'name':gender, 'description:'', 'schema':int64}]
                path
                    Mount path where featureset is mounted or None
                    example: path='/opt/dkube/fset'
                   
            *Outputs*

                Dictionary with response status

        """

        name = kwargs.get('name', None)
        df = kwargs.get('df', pd.DataFrame({'A': []}))
        metadata = kwargs.get('metadata', None)
        path = kwargs.get('path', None)

        assert(isinstance(df, pd.DataFrame)
        ), "df must be a DataFrame object"
        assert(not df.empty), "df can not be empty"

        featurespec = None
        
        if name is not None:
            featurespec, valid = super().get_featurespec(name)
            assert(valid), "featureset not found"
        if ((not featurespec) and (name is not None)):
            if not metadata:
                metadata = DKubeFeatureSetUtils().compute_features_metadata(df)
            assert(metadata), "The specified featureset is invalid"
            self.upload_featurespec(featureset=name, filepath=None, metadata=metadata)
            featurespec = metadata

        if featurespec is not None:
            isdf_valid = DKubeFeatureSetUtils().validate_features(df, featurespec)
            assert(isdf_valid), "DataFrame validation failed"

        return super().commit_featureset(name, df, path)

    def read_featureset(self, **kwargs):
        """
            Method to read a featureset version.
            If name is specified, path is derived. If featureset is not mounted, a copy is made to user's homedir
            If path is specified, it should be a mounted path

            *Inputs*

                name
                    featureset to be read
                    example: name='fset' or None

                version
                    version to be read.
                    If no version specified, latest version is assumed
                    example: version='v2' or None

                path
                    path where featureset is mounted.
                    path='/opt/dkube/fset' or None 

            *Outputs*

                Dataframe object

        """
        name = kwargs.get('name', None)
        version = kwargs.get('version', None)
        path = kwargs.get('path', None)
        
        assert ((version == None) or isinstance(version,str)), "version must be a string"

        return super().read_featureset(name, version, path)


    def list_featuresets(self, query=None):
        """
            Method to list featuresets based on query string.
            Raises Exception in case of errors.

            *Inputs*

                query
                    A query string that is compatible with Bleve search format

            *Outputs*

                A Json string with response status and the list of featuresets

        """
        return super().list_featureset(query)

    def upload_featurespec(self, featureset=None, filepath=None, metadata=None):
        """
            Method to upload feature specification file.
            Raises Exception in case of errors.

            *Inputs*

                featureset
                    The name of featureset

                filepath
                    Filepath for the feature specification metadata yaml file

                metadata
                    feature specification in yaml object. 

                One of filepath or metadata should be specified.

            *Outputs*

                A Json string with response status

        """
        assert(featureset and isinstance(featureset,str)), "featureset must be string"
        assert(bool(filepath) ^ bool(metadata)), "One of filepath and metadata should be specified"
        return super().featureset_upload_featurespec(featureset, filepath, metadata)

    def get_featurespec(self, featureset=None):
        """
            Method to retrieve feature specification method.
            Raises Exception in case of errors.

            *Inputs*

                featureset

                    The name of featureset

            *Outputs*

                A Json string with response status and feature specification metadata

        """
        return super().get_featurespec(featureset)

###############################################################

    def create_dataset(self, dataset: DkubeDataset, wait_for_completion=True):
        """
            Method to create a dataset on DKube.
            Raises Exception in case of errors.


            *Inputs*

                dataset
                    Instance of :bash:`dkube.sdk.rsrcs.dataset` class.
                    Please see the :bash:`Resources` section for details on this class.


                wait_for_completion
                    When set to :bash:`True` this method will wait for dataset resource to get into one of the complete state.
                    dataset is declared complete if it is one of the :bash:`complete/failed/error` state

        """


        assert type(
            dataset) == DkubeDataset, "Invalid type for run, value must be instance of rsrcs:DkubeDataset class"
        super().create_repo(dataset)
        while wait_for_completion:
            status = super().get_repo('dataset', dataset.user, dataset.name, fields='status')
            state, reason = status['state'], status['reason']
            if state.lower() in ['ready', 'failed', 'error']:
                print(
                    "dataset {} - completed with state {} and reason {}".format(dataset.name, state, reason))
                break
            else:
                print(
                    "dataset {} - waiting for completion, current state {}".format(dataset.name, state))
                time.sleep(self.wait_interval)

    def get_dataset(self, user, name):
        """
            Method to fetch the dataset with given name for the given user.
            Raises exception in case of dataset is not found or any other connection errors.

            *Inputs*

                user
                    User whose dataset has to be fetched.
                    In case of if token is of different user, then the token should have permission to fetch the
                    dataset of the :bash:`user` in the input. They should be in same DKube group.

                name
                    Name of the dataset to be fetched

        """

        return super().get_repo('dataset', user, name)

    def list_datasets(self, user, filters='*'):
        """
            Method to list all the datasets of a user.
            Raises exception on any connection errors.

            *Inputs*

                user
                    User whose datasets must be fetched.
                    In case of if token is of different user, then the token should have permission to fetch the
                    datasets of the :bash:`user` in the input. They should be in same DKube group.

                filters
                    Only :bash:`*` is supported now.

                    User will able to filter datasets based on state or the source

        """

        return super().list_repos('dataset', user)

    def delete_dataset(self, user, name):
        """
            Method to delete a dataset.
            Raises exception if token is of different user or if dataset with name doesnt exist or on any connection errors.

            *Inputs*

                user
                    The token must belong to this user. As dataset of different user cannot be deleted.

                name
                    Name of the dataset which needs to be deleted.

        """

        super().delete_repo('dataset', user, name)

    def create_model(self, model: DkubeModel, wait_for_completion=True):
        """
            Method to create a model on DKube.
            Raises Exception in case of errors.


            *Inputs*

                model
                    Instance of :bash:`dkube.sdk.rsrcs.model` class.
                    Please see the :bash:`Resources` section for details on this class.


                wait_for_completion
                    When set to :bash:`True` this method will wait for model resource to get into one of the complete state.
                    model is declared complete if it is one of the :bash:`complete/failed/error` state

        """

        assert type(
            model) == DkubeModel, "Invalid type for run, value must be instance of rsrcs:DkubeModel class"
        super().create_repo(model)
        while wait_for_completion:
            status = super().get_repo('model', model.user, model.name, fields='status')
            state, reason = status['state'], status['reason']
            if state.lower() in ['ready', 'failed', 'error']:
                print(
                    "model {} - completed with state {} and reason {}".format(model.name, state, reason))
                break
            else:
                print(
                    "model {} - waiting for completion, current state {}".format(model.name, state))
                time.sleep(self.wait_interval)

    def get_model(self, user, name):
        """
            Method to fetch the model with given name for the given user.
            Raises exception in case of model is not found or any other connection errors.

            *Inputs*

                user
                    User whose model has to be fetched.
                    In case of if token is of different user, then the token should have permission to fetch the
                    model of the :bash:`user` in the input. They should be in same DKube group.

                name
                    Name of the model to be fetched

        """

        return super().get_repo('model', user, name)

    def list_models(self, user, filters='*'):
        """
            Method to list all the models of a user.
            Raises exception on any connection errors.

            *Inputs*

                user
                    User whose models must be fetched.
                    In case of if token is of different user, then the token should have permission to fetch the
                    models of the :bash:`user` in the input. They should be in same DKube group.

                filters
                    Only :bash:`*` is supported now.

                    User will able to filter models based on state or the source

        """

        return super().list_repos('model', user)

    def delete_model(self, user, name):
        """
            Method to delete a model.
            Raises exception if token is of different user or if model with name doesnt exist or on any connection errors.

            *Inputs*

                user
                    The token must belong to this user. As model of different user cannot be deleted.

                name
                    Name of the model which needs to be deleted.

        """

        super().delete_repo('model', user, name)

    def trigger_runs_bycode(self, code, user):
        """
            Method to trigger all the runs in dkube which uses the mentioned code.

            *Inputs*

                code
                    Name of the code.

                user
                    Owner of the code. All runs of this user will be retriggered.

        """

        condition = TriggerCondition(match='code', name=code, user=user)
        return super().trigger_runs(condition)

    def trigger_runs_bydataset(self, dataset, user):
        """
            Method to trigger all the runs in dkube which uses the mentioned dataset in input.

            *Inputs*

                dataset
                    Name of the dataset.

                user
                    Owner of the dataset. All runs of this user will be retriggered.

        """
        condition = TriggerCondition(match='dataset', name=dataset, user=user)
        return super().trigger_runs(condition)

    def trigger_runs_bymodel(self, model, user):
        """
            Method to trigger all the runs in dkube which uses the mentioned model in input.

            *Inputs*

                model
                    Name of the model.

                user
                    Owner of the model. All runs of this user will be retriggered.

        """

        condition = TriggerCondition(match='model', name=model, user=user)
        return super().trigger_runs(condition)

    def get_model_lineage(self, user, name, version):
        """
            Method to get lineage of a model version.

            *Inputs*

                name
                    Name of the model

                version
                    Version of the model

                user
                    Owner of the model.
        """

        return super().get_datum_lineage('model', user, name, version)

    def get_dataset_lineage(self, user, name, version):
        """
            Method to get lineage of a dataset version.

            *Inputs*

                name
                    Name of the dataset

                version
                    Version of the dataset

                user
                    Owner of the dataset.
        """

        return super().get_datum_lineage('dataset', user, name, version)

    def get_training_run_lineage(self, user, name):
        """
            Method to get lineage of a training run.

            *Inputs*

                name
                    Name of the run

                user
                    owner of the run

        """

        # Get the training run info
        run = self.get_training_run(user, name)
        runid = run['job']['parameters']['generated']['uuid']
        return super().get_run_lineage('training', user, runid)

    def get_preprocessing_run_lineage(self, user, name):
        """
            Method to get lineage of a preprocessing run.

            *Inputs*

                name
                    Name of the run

                user
                    owner of the run

        """

        # Get the preprocessing run info
        run = get_preprocessing_run(user, name)
        runid = run['job']['parameters']['generated']['uuid']
        return super().get_run_lineage('preprocessing', user, runid)

    def get_model_versions(self, user, name):
        """
            Method to get the versions of model.
            Versions are returned in ascending order.

            *Inputs*

                name
                    Name of the model

                user
                    owner of the model

        """

        model = self.get_model(user, name)
        return model['versions']

    def get_model_latest_version(self, user, name):
        """
            Method to get the latest version of the given model.

            *Inputs*

                name
                    Name of the model

                user
                    owner of the model

        """

        versions = self.get_model_versions(user, name)
        return versions[0]['version']

    def get_model_version(self, user, name, version):
        """
            Method to get details of a version of the given model.
            Raises `NotFoundException` if the version is not found

            *Inputs*

                name
                    Name of the model

                version
                    Version of the model

                user
                    owner of the model
        """
        versions = self.get_model_versions(user, name)
        for v in versions:
            if v['version']['uuid'] == version:
                return v['version']

        raise Exception('{}/{}/{} not found'.format(user, name, version))

    def get_dataset_versions(self, user, name):
        """
            Method to get the versions of dataset.
            Versions are returned in ascending order.

            *Inputs*

                name
                    Name of the dataset

                user
                    owner of the dataset

        """

        dataset = self.get_dataset(user, name)
        return dataset['versions']

    def get_dataset_latest_version(self, user, name):
        """
            Method to get the latest version of the given dataset.

            *Inputs*

                name
                    Name of the dataset

                user
                    owner of the dataset

        """

        versions = self.get_dataset_versions(user, name)
        return versions[0]['version']

    def get_dataset_version(self, user, name, version):
        """
            Method to get details of a version of the given dataset.
            Raises `NotFoundException` if the version is not found

            *Inputs*

                name
                    Name of the dataset

                version
                    Version of the dataset

                user
                    owner of the dataset
        """
        versions = self.get_dataset_versions(user, name)
        for v in versions:
            if v['version']['uuid'] == version:
                return v['version']

        raise Exception('{}/{}/{} not found'.format(user, name, version))

    def get_datascience_capabilities(self):
        """
            Method to get the datascience capabilities of the platform.
            Returns the supported frameworks, versions and the corresponding container image details.

        """
        return super().get_datascience_capability()

    def get_notebook_capabilities(self):
        """
            Method to get the notebook capabilities of the platform.
            Returns the supported frameworks, versions and the image details.

        """
        caps = self.get_datascience_capabilities()
        return caps['nb_ide']['frameworks']

    def get_r_capabilities(self):
        """
            Method to get the R language capabilities of the platform.
            Returns the supported frameworks, versions and the image details.

        """
        caps = self.get_datascience_capabilities()
        return caps['r_ide']['frameworks']

    def get_training_capabilities(self):
        """
            Method to get the training capabilities of the platform.
            Returns the supported frameworks, versions and the image details.

        """
        caps = self.get_datascience_capabilities()
        return caps['training']['frameworks']

    def get_serving_capabilities(self):
        """
            Method to get the serving capabilities of the platform.
            Returns the supported frameworks, versions and the image details.

        """
        caps = self.get_datascience_capabilities()
        return caps['serving']['frameworks']

    def release_model(self, user, model, version=None, wait_for_completion=True):
        """
            Method to release a model to model catalog.
            Raises Exception in case of errors.


            *Inputs*

                model
                    Name with model.

                version
                    Version of the model to be released. 
                    If not passed then latest version is released automatically.

                user
                    Owner of the model.

                wait_for_completion
                    When set to :bash:`True` this method will wait for publish to finish.
                    Publishing is complete if stage of the mode is changed to :bash:`published/failed/error`

        """

        if version == None:
            version = self.get_model_latest_version(user, model)
            version = version['uuid']

        super().release_model(user, model, version)

        while wait_for_completion:
            v = self.get_model_version(user, model, version)
            stage = v['model']['stage']
            reason = v['model']['reason']
            if stage.lower() in ['released', 'failed', 'error']:
                print(
                    "release {}/{} - completed with state {} and reason {}".format(model, version, stage, reason))
                break
            else:
                print(
                    "release {}/{} - waiting for completion, current state {}".format(model, version, stage))
                time.sleep(self.wait_interval)

    def publish_model(self, name, description, details: DkubeServing, wait_for_completion=True):
        """
            Method to publish a model to model catalog.
            Raises Exception in case of errors.


            *Inputs*

                name
                    Name with which the model must be published in the model catalog.

                description
                    Human readable text for the model being published

                details
                    Instance of :bash:`dkube.sdk.rsrcs.serving` class.
                    Please see the :bash:`Resources` section for details on this class.

                    If serving image is not updated in :bash:`run:DkubeServing` argument then,
                    - If training used supported standard framework, dkube will pick approp serving image
                    - If training used custom image, dkube will try to use the same image for serving

                    If transformer image is not updated in :bash:`run:DkubeServing` then,
                    - Dkube will use same image as training image

                    If transformer code is not updated in :bash:`run:DkubeServing` then,
                    - Dkube will use the code used for training


                wait_for_completion
                    When set to :bash:`True` this method will wait for publish to finish.
                    Publishing is complete if stage of the mode is changed to :bash:`published/failed/error`

        """

        run = details
        user, model, version = run.serving_def.owner, run.serving_def.model, run.serving_def.version
        # Fetch training run details and fill in information for serving
        if run.predictor.image == None or (
                run.serving_def.transformer == True and run.transformer.image == None) or (
                run.serving_def.transformer == True and run.serving_def.transformer_project == None):

            if run.serving_def.version == None:
                v = self.get_model_latest_version(
                    run.serving_def.owner, run.serving_def.model)
                run.serving_def.version = v['uuid']

            li = self.get_model_lineage(
                run.serving_def.owner, run.serving_def.model, run.serving_def.version)
            if run.predictor.image == None:
                si = li['run']['parameters'][
                    'generated']['serving_image']['image']
                run.update_serving_image(
                    si['path'], si['username'], si['password'])

            if run.serving_def.transformer == True and run.transformer.image == None:
                ti = li['run']['parameters']['generated'][
                    'training_image']['image']
                run.update_transformer_image(
                    ti['path'], ti['username'], ti['password'])

            if run.serving_def.transformer == True and run.serving_def.transformer_project == None:
                code = li['run']['parameters']['training'][
                    'datums']['workspace']['data']
                cname = code['name'].split(':')[1]
                run.update_transformer_code(cname, code['version'])

        data = {'name': name, 'description': description,
                'serving': run.serving_def}
        super().publish_model(user, model, version, data)

        while wait_for_completion:
            v = self.get_model_version(user, model, version)
            stage = v['model']['stage']
            reason = v['model']['reason']
            if stage.lower() in ['published', 'failed', 'error']:
                print(
                    "publish {}/{} - completed with state {} and reason {}".format(model, version, stage, reason))
                break
            else:
                print(
                    "publish {}/{} - waiting for completion, current state {}".format(model, version, stage))
                time.sleep(self.wait_interval)

    def create_model_deployment(self, user, name, model, version,
                                description=None,
                                stage_or_deploy="stage", wait_for_completion=True):
        """
            Method to create a serving deployment for a model in the model catalog.
            Raises Exception in case of errors.


            *Inputs*

                user
                    Name of the user creating the deployment

                name
                    Name of the deployment. Must be unique

                description
                    User readable description of the deployment

                model
                    Name of the model to be deployed

                version
                    Version of the model to be deployed

                                stage_or_deploy
                                        Default set to :bash: `stage` which means to stage the model deployment for testing before
                                        deploying it for production.
                                        Change to :bash: `deploy` to deploy the model in production

                wait_for_completion
                    When set to :bash:`True` this method will wait for job to complete after submission.
                    Job is declared complete if it is one of the :bash:`complete/failed/error` state

        """

        assert stage_or_deploy in [
            "stage", "deploy"], "Invalid value for stage_or_deploy parameter."

        # Fetch the model from modelcatalog
        mcitem = self.get_modelcatalog_item(user, model, version)

        run = DkubeServing(user, name=name, description=description)
        run.update_serving_model(model, version=version)
        run.update_serving_image(image_url=mcitem['serving']['images'][
                                 'serving']['image']['path'])

        if stage_or_deploy == "stage":
            super().stage_model(run)
        if stage_or_deploy == "deploy":
            super().deploy_model(run)

        while wait_for_completion:
            status = super().get_run('inference', run.user, run.name, fields='status')
            state, reason = status['state'], status['reason']
            if state.lower() in ['complete', 'failed', 'error', 'running']:
                print(
                    "run {} - completed with state {} and reason {}".format(run.name, state, reason))
                break
            else:
                print(
                    "run {} - waiting for completion, current state {}".format(run.name, state))
                time.sleep(self.wait_interval)

    def delete_model_deployment(self, user, name):
        """
            Method to delete a model deployment.
            Raises exception if token is of different user or if serving run with name doesnt exist or on any connection errors.

            *Inputs*

                user
                    The token must belong to this user. As run of different user cannot be deleted.

                name
                    Name of the run which needs to be deleted.

        """

        super().delete_run('inference', user, name)

    def list_model_deployments(self, user, filters='*'):
        """
            Method to list all the model deployments.
            Raises exception on any connection errors.

            *Inputs*

                user
                    Name of the user.

                filters
                    Only :bash:`*` is supported now.

                    User will able to filter runs based on state or duration

        """

        deps = []
        resp = super().list_runs('inference', user)
        for item in resp:
            for inf in item['jobs']:
                deploy = inf['parameters']['inference']['deploy']
                # MAK - BUG - there is no way today from backend response to separate the test-inferences
                # vs serving deployments. So appending all.
                deps.append(inf)
        return deps

    def modelcatalog(self, user):
        """
            Method to fetch the model catalog from DKube.
            Model catalog is list of models published by datascientists and are
            ready for staging or deployment on a production cluster.
            The user must have permission to fetch the model catalog.

            *Inputs*

                user
                    Name of the user.
        """
        return super().modelcatalog(user)

    def get_modelcatalog_item(self, user, model, version):
        """
            Method to get an item from modelcatalog
            Raises exception on any connection errors.

            *Inputs*

                user
                    Name of the user.

                model
                    Name of the model in the model catalog

                version
                    Version of the model

        """
        mc = self.modelcatalog(user)

        for item in mc:
            if item['name'] == model:
                for iversion in item['versions']:
                    if iversion['model']['version'] == version:
                        return iversion

        raise Exception('{}.{} not found in model catalog'.format(model, version))

    def list_projects(self):
        """Return list of DKube projects."""
        response = self._api.get_all_projects().to_dict()
        assert response['response']['code'] == 200, response['response']['message']
        return response['data']

    def create_project(self, project:DkubeProject):
        """Creates DKube Project.

        *Inputs*

            project
                instance of :bash:`dkube.sdk.rsrcs.DkubeProject` class.
        """
        assert type(project) == DkubeProject, "Invalid type for project, value must be instance of rsrcs:DkubeProject class"
        response = self._api.create_project(project).to_dict()
        assert response['response']['code'] == 200, response['response']['message']
        return response['data']

    def update_project (self, project_id, project:DkubeProject):
        """Update project details. 
        Note: details and evail_details fields are base64 encoded.
        
        *Inputs*

            project_id
                id of the project

            project
                instance of :bash:`dkube.sdk.rsrcs.DkubeProject` class.
        """
        assert type(project) == DkubeProject, "Invalid type for project, value must be instance of rsrcs:DkubeProject class"
        project.id = project_id
        response = self._api.update_one_project(project, project.id).to_dict()
        assert response['code'] == 200, response['message']

    def get_project_id (self, name):
        """"Get project id from project name.

        *Inputs*

            name
                name of the project
        """
        response = self._api.get_all_projects().to_dict()
        assert response['response']['code'] == 200, response['response']['message']
        for project in response['data']:
            if project['name'] == name:
                return project['id']
        return None

    def get_project(self, project_id):
        """Get project details.
        
        *Inputs*

            project_id
                id of the project
        """
        response = self._api.get_one_project(project_id).to_dict()
        assert response['response']['code'] == 200, response['response']['message']
        return response['data']

    def get_leaderboard(self, project_id):
        """Get project's leaderboard details.
        
        *Inputs*

            project_id
                id of the project
        """
        response = self._api.get_all_project_submissions(project_id).to_dict()
        assert response['response']['code'] == 200, response['response']['message']
        return response['data']

    def delete_project(self, project_id):
        """Delete project. This only deletes the project and not the associated resources.
        
        *Inputs*

            project_id
                id of the project
        """
        project_ids = {"project_ids": [project_id]}
        response = self._api.projects_delete_list(project_ids).to_dict()
        assert response['code'] == 200, response['message']
