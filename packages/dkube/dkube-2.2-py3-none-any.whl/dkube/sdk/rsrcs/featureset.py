from __future__ import print_function

import os
import sys
import time
from pprint import pprint
import json
import tempfile

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from dkube.sdk.internal import dkube_api
from dkube.sdk.internal.dkube_api.models.feature_set_input_def import \
    FeatureSetInputDef
from dkube.sdk.internal.dkube_api.rest import ApiException

from .util import *


class DkubeFeatureSet(object):
    """

        This class defines the DKube featureset with helper functions to set properties of featureset.::

            from dkube.sdk import *
             mnist = DkubeFeatureSet(name="mnist-fs")

    """

    def __init__(self, name=generate("featureset"), tags=None, description=None, path=None, config_file="/opt/dkube/conf/conf.json"):
        self.featureset = FeatureSetInputDef(
            name=None, tags=None, description=None)

        self.update_basic(name, description, tags, config_file)
        self.update_featurespec_file(path)
        self.update_features_path()

    def update_basic(self, name, description, tags, config_file):
        if name is not None:
            self.featureset.name = name
        if description is not None:
            self.featureset.description = description
        if tags is not None:
            self.featureset.tags = tags
        self.CONFIG_FILE = config_file

    def update_featurespec_file(self, path=None):
        """
            Method to update the filepath for feature specification metadata

            *Inputs*

                path
                    A valid filepath. The file should be an YAML file describing a 'Name', 'Description', 'Schema' for each feature.

        """
        self.featurespec_path = path

    def upload_featurespec(self):
        pass

    def update_features_path(self, path=None):
        """
            Method to update the directory path for features data

            *Inputs*

                path
                    A valid directory path. This folder is typically where the featureset is mounted by DKube. The folder contains features saved in Apache Parquet file format. 

        """
        self.features_path = path




class DKubeFeatureSetUtils:

    def validate_features(self, dataframe=None, featurespec=None) -> bool:
        """
            Method to validate features data against features specification metadata 

            *Inputs*

                dataframe
                    Panda's dataframe object with features data. This should confirm to the feature specification metadata.
                featurespec
                    Dictionary 

        """
        if featurespec is None or dataframe is None:
            return False

        f_spec = featurespec
        # Parse featurespec.
        # - Create a list of feature names
        # - Create a map of feature name and schema
        fspec_dic = {}
        fspec_keys = []
        for each_spec in f_spec:
            fspec_dic[str(each_spec['name'])] = str(each_spec['schema'])
            fspec_keys.append(str(each_spec['name']))

        # Get the feature names and schema from the dataframe
        schema = [str(sma) for sma in dataframe.dtypes.to_list()]
        df_keys = [str(k) for k in dataframe.keys()]
        df_spec = {}
        for i in range(len(df_keys)):
            df_spec[df_keys[i]] = schema[i]

        # Validations
        # - The number of features should be the same
        # - The feature names should be the same
        # - The feature schema should be the same.

        if len(fspec_keys) != len(df_keys):
            # "No. of columns in dataframe and featurespec are not equal"
            return False
        for each_key in df_keys:
            if each_key not in fspec_keys:
                # error": "Column name {} not found in featurespec".format(each_key)
                return False
            if df_spec[each_key] != fspec_dic[each_key]:
                # Datatype not matched for column {}".format(each_key)}
                return False

        return True

    def compute_features_metadata(self, df):
        # Prepare featurespec - Name, Description, Schema for each feature
        keys = df.keys()
        schema = df.dtypes.to_list()
        featureset_metadata = []
        
        for i in range(len(keys)):
            metadata = {}
            metadata["name"] = str(keys[i])
            metadata["description"] = None
            metadata["schema"] = str(schema[i])
            featureset_metadata.append(metadata)

        return featureset_metadata
        # Convert featureset metadata (featurespec) to yaml
        #featureset_metadata = yaml.dump(featureset_metadata, default_flow_style=False)

    # return the mounted path for the featureset
    def _get_featureset_mount_path(self, name, config, type):
       
        # name - featureset name
        # config - config.json in dict format
        # type - search in 'outputs' or 'inputs'
        object = config.get(type, None)
        if object is None:
            return None
        
        for rec in object:
            fsets = rec.get('featureset', None)
            if fsets is None:
                continue
            for fset in fsets:
                if name == fset['name']:
                    return fset['location']
        return None

    # return the mounted featureset name, given the mount point
    def _get_featureset_name(self, path, config, type):
       
        # path - featureset mount path
        # config - config.json in dict format
        # type - search in 'outputs' or 'inputs'
        object = config.get(type, None)
        if object is None:
            return None
        
        for rec in object:
            fsets = rec.get('featureset', None)
            if fsets is None:
                continue
            for fset in fsets:
                if path == fset['location'] or path == fset['dkube_path']:
                    return fset['name']
            
        return None
        
    def _get_d3_full_path(self, rel_path):

        # Get full path to dkube store
        rel_path = rel_path.replace('users','home',1)                     
        base = os.getenv("DKUBE_DATA_BASE_PATH")
        fullpath = os.path.join(base, rel_path)
        return (fullpath)

    def _get_d3_rel_path(self, full_path):
        # Is this a mounted path
        relpath = self._get_d3_path_from_mountpoint(full_path)

        # This might have been created 
        if relpath is None:
            # Get relative path from dkube store       
            base = os.getenv("DKUBE_DATA_BASE_PATH")
            relpath = os.path.relpath(full_path, base)
            relpath = relpath.replace('home','users',1) 
        return (relpath)

    def _get_d3_path_from_mountpoint(self, path):
        # For the following df output, it returns featuresets/train-fs-1936/1610480719061/data
        #   10.233.59.86:/dkube/featuresets/train-fs-1936/1610480719061/data  /fset 

        src = target = None
        for l in open("/proc/mounts", "r"):
            tabs = l.split(" ")
            if( path == tabs[1] ):
                src = tabs[0]
                break
        if src is not None:
            mnt_fields = src.split(":")
            if len(mnt_fields) > 1:
                src = mnt_fields[1]
            else:
                src = mnt_fields[0]
            src = os.path.relpath(src, "/dkube")
        return src


    def get_top_version(self, versions):
        # Get the latest version
        # Shortcut for now, get the length of the list and return it
        top = len(versions)
        return ('v{}'.format(top))

    def validate_version(self, versions, version):
        # Does the version specified exists?
        index = int(version[1:])
        if index >= 1 and index <= len(versions):
            return True
        return False
    
    def get_version_status(self, versions, version):
        # Get the state of the specified version
        index = int(version[1:])
        if index < 1 and index > len(versions):
            return 'INVALID'
        versions = sorted(versions, key=lambda k: k['version'].get('index', 0), reverse=False)
        return versions[index-1]['version']['state']

    def get_featureset_name_from_mountpath(self, path, type):

        try:
            if os.path.exists("/etc/dkube/config.json"):
                with open("/etc/dkube/config.json") as fp:
                    dkube_config = json.load(fp)
                    name = self._get_featureset_name(path, dkube_config, type)
        except:
            name = None

        return name



    def features_write(self, name, dataframe, path=None) -> str:
        """
            Method to write features 

            *Inputs*

                name
                    Featureset name 

                dataframe
                    Panda's dataframe object with features data. This should confirm to the feature specification metadata.

                path
                    This is optional. If not specified it derives the path from /etc/dkube/config.json. 

            *Outputs*  
                path - where the features are written

        """
        filename = 'featureset.parquet'
        if path is None:
            assert(name)
            # Get the path
            try:
                if os.path.exists("/etc/dkube/config.json"):
                    with open("/etc/dkube/config.json") as fp:
                        dkube_config = json.load(fp)
                        path = self._get_featureset_mount_path(name, dkube_config, 'outputs')
            except:
                path = None

            if path is None:
                dkube_path = os.getenv('DKUBE_USER_STORE')
                if dkube_path is None:
                    return None
                featureset_folder = 'gen/outputs/' + name
                path = os.path.join(dkube_path, featureset_folder)
                os.makedirs(path, exist_ok=True)
                # update config.json
                #_update_featureset_path(name, dkube) 

        # Try writing 2 times
        # After commit, the parquet file becomes read-only
        for i in range(2):
            try:
                table = pa.Table.from_pandas(dataframe)
                pq.write_table(table, os.path.join(path, filename))

                # Get the path relative to DKube base
                path = self._get_d3_rel_path(path)
                return path

            except Exception as e:
                print("features_write: write failed {}".format(str(e)))
                if i == 1:
                    return None

    def features_read(self, name, path=None) -> (pd.DataFrame, bool):
        """
            Method to read features 

            *Inputs*

                name
                    featureset name
                path
                    This is optional. It points to where featureset is mounted

            *Outputs*  
                    Dataframe with features

        """
        filename='featureset.parquet'
        df_empty = pd.DataFrame({'A': []})
        is_mounted = False

        if path is None:
            # Get the path
            try:
                if os.path.exists("/etc/dkube/config.json"):
                    with open("/etc/dkube/config.json") as fp:
                        dkube_config = json.load(fp)
                        path = self._get_featureset_mount_path(name, dkube_config, 'inputs')
                        if path is not None:
                            is_mounted=True
            except:
                path = None

        if path is None:
            return df_empty,  is_mounted
        try:
            table = pq.read_table(os.path.join(path, filename))
            feature_df = table.to_pandas()
            return feature_df, is_mounted
        except Exception as e:
            return df_empty, is_mounted
