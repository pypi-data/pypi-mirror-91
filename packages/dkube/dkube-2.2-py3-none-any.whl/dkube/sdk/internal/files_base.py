"""

.. module:: DKubeAPIs for file upload and download
   :synopsis: Helper class which provides high level methods for user to integrate at workflow level.

.. moduleauthor:: Subrahmanyam Ongole <github.com/songole>


"""

from __future__ import print_function

import json
import os
from pprint import pprint
import tempfile
import yaml

import requests
from dkube.sdk.internal.dkube_api.models.api_response import ApiResponse
from dkube.sdk.internal.dkube_api.rest import ApiException
from url_normalize import url_normalize


class FilesBase(object):

    def __init__(self, url=None, token=None):

        protocol = url.split(':')
        url = url.rstrip('/')
        if protocol[0] == "https":
            self.url = "{}/dkube/v2/ext".format(url)
        else:
            assert protocol[0] == "http", "Invalid host"
            self.url = "{}/dkube/v2".format(url)
        
        self.token = token
        self.request_headers = {}
        self.request_headers['Authorization'] = 'Bearer {}'.format(self.token)


    def _upload_file(self, urlpath=None, filepath=None):

        try:
            fp = open(filepath)
        except BaseException:
            print("Specified filepath {} is not valid".format(filepath))
            return response()
        
        urlpath = os.path.normpath(urlpath)
        ep = '{}{}'.format(self.url, urlpath)
        
        response = requests.post(
            ep,
            headers=self.request_headers,
            files={'upfile': fp},
            verify=False,
        )
        return response

    def featureset_upload_featurespec(self, featureset=None, filepath=None, metadata=None) :
        """
        Method to upload features specification file on DKube.
        Raises Exception in case of errors.

        """
        url = "/featuresets/" + featureset + "/featurespec/upload"
        resp = None
        
        if filepath:
            assert (
                os.path.isfile(filepath) == True
            ), "Specified file path {} is invalid".format(filepath)
            resp = self._upload_file(url, filepath)
        else:
            with tempfile.NamedTemporaryFile() as temp:
                spec = yaml.safe_dump(metadata)
                temp.write(spec.encode('ascii'))
                temp.flush()
                resp = self._upload_file(url, temp.name)
        
        resp_dict = json.loads(resp.text)
        return resp_dict

    def featureset_download_specfile(self, featureset=None):
        """
        Method to upload features specification file on DKube.
        Raises Exception in case of errors.

        *Inputs*

            featureset
                FeatureSet name.

            filepath
                The full pathname of features specification file on your workstation

        """
        url = "/featuresets/" + featureset + "/featurespec/download"
        assert (
            os.path.isfile(filepath) == True
        ), "Specified file path {} is invalid".format(filepath)
        resp = self._upload_file(url, filepath)
        resp_dict = json.loads(resp.text)
        return resp_dict



