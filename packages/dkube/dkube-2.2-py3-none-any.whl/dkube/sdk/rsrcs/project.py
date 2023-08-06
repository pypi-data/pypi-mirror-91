from dkube.sdk.internal.dkube_api import ProjectModel


class DkubeProject(ProjectModel):
    """This class defines the properties which can be set on the instance of DkubeProject.

        *Properties*

            name
                name of the project
            description
                description of the project (Optional)
            image
                URL for the image thumbnail for this project (Optional)
            leaderboard
                set True to enable the leaderboard (default False)
            details
                Project details. this should be base64 encoded (Optional)
            eval_repo
                Dkube code repo name of eval repository
            eval_commit_id
                commit id of eval repository (Optional)
            eval_image
                Docker image to be used for evaluation (Optional)
            eval_script
                command to run for evaluating the submission
            eval_details
                Evaluation details. This should be base64 encoded (Optional)
    """
    def __init__(self, name, **kwargs):
        super(DkubeProject, self).__init__(name, **kwargs)
