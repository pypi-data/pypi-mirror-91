from dkube.sdk.internal.dkube_api import ArtifactVolume

from .util import generate


class DkubeResourcePVC(object):
    """This class represent kubernetes PVC for DKube resources.

        *Arguments*

            type
                type of dkube resource (program/dataset/model/featureset)
            kind
                Kind of volume to be exported  (input/output/intermediate)
            name
                name of the resource
            version
                version of the resource (in v1,v2 format). default is 'latest' (Optional)
    """

    def __init__ (self, type, kind, name, version='latest'):
        claimname = "{{workflow.uid}}-" + generate(type)
        self.volume = ArtifactVolume(name = claimname, artifact_type=type, artifact_name=name, artifact_version=version)
        self.claimname = claimname
        self.kind = kind

