from __future__ import print_function

import sys
import time
from pprint import pprint

from dkube.sdk.internal import dkube_api
from dkube.sdk.internal.dkube_api.models.datum_model import DatumModel
from dkube.sdk.internal.dkube_api.models.datum_model_k8svolume import \
    DatumModelK8svolume
from dkube.sdk.internal.dkube_api.models.gcs_access_info import GCSAccessInfo
from dkube.sdk.internal.dkube_api.models.git_access_credentials import \
    GitAccessCredentials
from dkube.sdk.internal.dkube_api.models.git_access_info import GitAccessInfo
from dkube.sdk.internal.dkube_api.models.nfs_access_info import NFSAccessInfo
from dkube.sdk.internal.dkube_api.models.redshift_access_info import \
    RedshiftAccessInfo
from dkube.sdk.internal.dkube_api.models.repo_gcs_access_info_secret import \
    RepoGCSAccessInfoSecret
from dkube.sdk.internal.dkube_api.models.s3_access_credentials import \
    S3AccessCredentials
from dkube.sdk.internal.dkube_api.rest import ApiException

from .util import *


class DkubeModel(object):

    """

        This class defines the DKube model with helper functions to set properties of model.::

            from dkube.sdk import *
            mnist = DkubeModel("oneconv", name="mnist")

            Where first argument is the owner of this model. User should be a valid onboarded user in dkube.

    """

    MODEL_SOURCES = ["dvs", "git", "aws_s3", "s3", "gcs", "nfs", "k8svolume"]

    """
    List of valid model sources in DKube.
    Some sources are downloaded while some are remotely referenced.

    :bash:`dvs` :- To create an empty repository which can be used in future runs.

    :bash:`git` :- If data is in the git repo. All git compatible repos are supported - github, bitbucket, gitlab. :bash:`Downloaded`

    :bash:`aws_s3` :- If the data is in AWS s3 bucket. :bash:`Downloaded | Remote`

    :bash:`s3` :- Non aws s3 data source. Like MinIO deployed on internal cluster. :bash:`Downloaded | Remote`

    :bash:`gcs` :- Google cloud storage as data source. :bash:`Downloaded`

    :bash:`nfs` :- External NFS server as data source. :bash:`Remote`

    :bash:`k8svolume` :- Kubernetes volume as data source. :bash:`Remote`

    """

    GIT_ACCESS_OPTS = ["apikey", "sshkey", "password"]

    """
    List of authentication options supported for git data source.

    :bash:`apikey` :- Github APIKey based authentication. This must have permission on the repo to clone and checkout.

    :bash:`sshkey` :- Git SSH key based authentication.

    :bash:`password` :- Standard username/password based. 

    """


    def __init__(self, user, name=generate("dataset"), tags=None):
        self.k8svolume = DatumModelK8svolume(name=None)

        self.nfsaccess = NFSAccessInfo(server=None, path=None)

        self.gcssecret = RepoGCSAccessInfoSecret(name=None, content=None)
        self.gcsaccess = GCSAccessInfo(
            bucket=None, prefix=None, secret=self.gcssecret)

        self.s3access = S3AccessCredentials(
            access_key_id=None, access_key=None, bucket=None, prefix=None, endpoint=None)

        self.gitcreds = GitAccessCredentials(
            username=None, password=None, apikey=None, sshkey=None, private=True)
        self.gitaccess = GitAccessInfo(
            path=None, url=None, branch=None, credentials=self.gitcreds)

        self.datum = DatumModel(name=None, tags=None, _class='model',
                                dvs=None, source='dvs', url=None, remote=False, gitaccess=self.gitaccess,
                                s3access=self.s3access, nfsaccess=self.nfsaccess, gcsaccess=self.gcsaccess)

        self.update_basic(user, name, tags)

    def update_basic(self, user, name, tags):
        tags = list_of_strs(tags)

        self.user = user
        self.name = name

        self.datum.name = name
        self.datum.tags = tags

    def update_model_source(self, source=MODEL_SOURCES[0]):
        """
            Method to update the source for this model.
            It should be one of the choice mentioned in MODEL_SOURCES
            Default value is **git**
        """

        self.datum.source = source

    def update_git_details(self, url, branch=None, authopt=GIT_ACCESS_OPTS[0], authval=None):
        """
i            Method to update the details of git source.

            *Inputs*

                url
                    A valid Git URL. Following are considered as valid URLs.

                    - CloneURL : https://github.com/oneconvergence/dkube.git

                    - TreeURL : https://github.com/oneconvergence/dkube/tree/2.1.dev/dkube

                    - BlobURL : https://github.com/oneconvergence/dkube/blob/2.1.dev/dkube/sdk/api.py

                    - ZipURL : https://github.com/oneconvergence/dkube/archive/2.1.dev.zip

                branch
                    Valid branch of git repo. If not provided then **master** branch is used by default.

                authopt
                    One of the valid option from **GIT_ACCESS_OPTS**

                authval
                    Value corresponding to the authopt
        """

        self.datum.source = "git"
        self.datum.url = url
        self.gitaccess.url = url
        self.gitaccess.branch = branch

        self.gitcreds.username = self.user

        if authopt == 'apikey':
            self.gitcreds.apikey = authval
        elif authopt == 'password':
            self.gitcreds.password = authval
        elif authopt == 'sshkey':
            self.gitcreds.sshkey = authval

    def update_awss3_details(self, bucket, prefix, key, secret):
        """
            Method to update details of aws s3 data source.

            *Inputs*

                bucket
                    Valid bucket in aws s3

                prefix
                    Path to an object in the bucket. Dkube will fetch recursively all objects under this prefix.

                key
                    AWS s3 access key id

                secret
                    AWS s3 access key secret
        """

        self.datum.source = "aws_s3"
        self.s3access.bucket = bucket
        self.s3access.prefix = prefix
        self.s3access.access_key_id = key
        self.s3access.access_key = secret

    def update_s3_details(self, endpoint, bucket, prefix, key, secret):
        """
            Method to update details of s3 data source like minio.

            *Inputs*

                bucket
                    Valid bucket name in s3 store

                prefix
                    Path to an object in the bucket. Dkube will fetch recursively all objects under this prefix.

                key
                    S3 access key id

                secret
                    s3 access key secret
        """

        self.datum.source = "s3"
        self.s3access.endpoint = endpoint
        self.s3access.prefix = prefix
        self.s3access.bucket = bucket
        self.s3access.access_key_id = key
        self.s3access.access_key = secret

    def update_gcs_details(self, bucket, prefix, key, secret):

        """
            Method to update details of google cloud storage.

            *Inputs*

                bucket
                    Valid bucket in GCS

                prefix
                    Path to an object in bucket. Dkube will fetch recursively all objects under this prefix.

                key
                    Name of the GCS secret

                secret
                    Content of the secret
        """

        self.datum.source = "gcs"
        self.gcsaccess.bucket = bucket
        self.gcsaccess.prefix = prefix
        self.gcssecret.name = key
        self.gcssecret.content = secret

    def update_nfs_details(self, server, path="/"):

        """
            Method to update details of nfs data source.

            *Inputs*

                server
                    IP address of the nfs server.

                path
                    Path in the nfs export. This path is directly mounted for the user program.

        """

        self.datum.source = "nfs"
        self.nfsaccess.path = path
        self.nfsaccess.server = server

    def update_k8svolume_details(self, name):

        """
            Method to update details of k8s volume data source.

            *Inputs*

                name
                    Name of the kubernetes volume. Volume should not be already **Bound**.
        """

        self.datum.source = "k8svolume"
        self.k8svolume.name = name
