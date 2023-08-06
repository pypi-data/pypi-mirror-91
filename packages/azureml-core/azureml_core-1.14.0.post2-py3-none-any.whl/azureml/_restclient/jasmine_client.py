# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Access jasmineclient"""
from .experiment_client import ExperimentClient


class JasmineClient(ExperimentClient):
    """
    Jasmine APIs

    :param host: The base path for the server to call.
    :type host: str
    :param auth: Client authentication
    :type auth: azureml.core.authentication.AbstractAuthentication
    :param subscription_id:
    :type subscription_id: str
    :param resource_group_name:
    :type resource_group_name: str
    :param workspace_name:
    :type workspace_name: str
    :param project_name:
    :type project_name: str
    """

    def __init__(self,
                 service_context,
                 experiment_name,
                 experiment_id=None,
                 **kwargs):
        """
        Constructor of the class.
        """
        try:
            from azureml.train.automl import __version__ as azureml_train_automl
        except Exception:
            azureml_train_automl = None
        try:
            from azureml.train.automl.runtime import __version__ as azureml_train_automl_runtime
        except Exception:
            azureml_train_automl_runtime = None

        self.automl_user_agent = "azureml.train.automl/{} azureml.train.automl.runtime/{}"\
            .format(azureml_train_automl, azureml_train_automl_runtime)

        super(JasmineClient, self).__init__(
            service_context, experiment_name, experiment_id, **kwargs)

    def get_rest_client(self, user_agent=None):
        """get service rest client"""
        if user_agent is None or not user_agent.__contains__("automl"):
            user_agent = "{} {}".format(user_agent, self.automl_user_agent)
        return self._service_context._get_jasmine_restclient(user_agent=user_agent)

    def post_validate_service(self, create_parent_run_dto):
        return self._execute_with_experiment_arguments(
            self._client.jasmine.validate_run_input, create_parent_run_dto)

    def post_on_demand_model_explain_run(self, run_id, model_explain_dto):
        return self._execute_with_experiment_arguments(
            self._client.jasmine.on_demand_model_explain, run_id, model_explain_dto)

    def post_parent_run(self, create_parent_run_dto=None):
        """
        Post a new parent run to Jasmine
        :param create_parent_run_dto:
        :return:
        """
        return self._execute_with_experiment_arguments(
            self._client.jasmine.create_parent_run, create_parent_run_dto)

    def post_remote_jasmine_run(self, parent_run_id, jsondefinition, zipfile):
        """
        Post a new experiment to Jasmine
        :param parent_run_id: str
        :param jsondefinition: json str containing run configuration information
        :param zipfile: file pointer to a zipfile containing AzureML project
        :return:
        """
        return self._execute_with_experiment_arguments(
            self._client.jasmine.post_remote_run, parent_run_id, jsondefinition, zipfile)

    def post_remote_jasmine_snapshot_run(self, parent_run_id, jsondefinition, snapshotId):
        """
        Post a new experiment to Jasmine
        :param parent_run_id:
        :type parent_run_id: str
        :param jsondefinition: json str containing run configuration information
        :type jsondefinition: str
        :param snapshotId: Id of the snapshot containing the project files
        :return:
        """
        return self._execute_with_experiment_arguments(
            self._client.jasmine.post_remote_snapshot_run, parent_run_id, jsondefinition, snapshotId)

    def get_next_task(self, parent_run_id, local_history_payload):
        """
        Get task for next iteration to run from Jasmine
        :param parent_run_id:
        :type parent_run_id: str
        :param local_history_payload:
        :type local_history_payload: ~_restclient.models.LocalHistoryPayload
        :return:
        """
        dto = self._execute_with_experiment_arguments(self._client.jasmine.local_run_get_next_task, parent_run_id,
                                                      local_history_payload)
        return dto if dto.__dict__ is not None else None

    def get_next_pipeline(self, parent_run_id, worker_id):
        """
        Get next set of pipelines to run from Jasmine
        :param parent_run_id:
        :type parent_run_id: str
        :param worker_id:
        :type worker_id: str
        :return:
        """
        dto = self._execute_with_experiment_arguments(
            self._client.jasmine.get_pipeline, parent_run_id, worker_id)
        return dto if dto.__dict__ is not None else None

    def set_parent_run_status(self, parent_run_id, target_status):
        """
        Post a new experiment to Jasmine
        :param parent_run_id:
        :type parent_run_id: str
        :param target_status:
        :type target_status: str
        :return:
        """
        return self._execute_with_experiment_arguments(
            self._client.jasmine.parent_run_status,
            parent_run_id, target_status)

    def cancel_child_run(self, child_run_id):
        """
        Post a new experiment to Jasmine
        :param child_run_id:
        :type child_run_id: str
        :return:
        """
        return self._execute_with_experiment_arguments(
            self._client.jasmine.cancel_child_run,
            child_run_id)

    def continue_remote_run(self, run_id, iterations=None, exit_time_sec=None, exit_score=None):
        """
        Post a new experiment to Jasmine
        :param child_run_id:
        :type child_run_id: str
        :return:
        """
        return self._execute_with_experiment_arguments(
            self._client.jasmine.continue_run,
            run_id, iterations, exit_time_sec, exit_score)

    def get_feature_profiles(self, run_id, feature_input_dto):
        """
        get feature profiles from Jasmine
        :param run_id:
        :type run_id: str
        :param feature_profile_input_dto:
        :type feature_profile_input_dto:
         ~_restclient.models.FeatureProfileInputDto
        :return:
        """
        return self._execute_with_experiment_arguments(
            self._client.jasmine.get_feature_profiles,
            run_id,
            feature_input_dto)

    def get_log_config(self, log_config_input):
        """
        Get log configuration for sdk.
        :param log_config_input: Input dto for getting log config dto from service side.
        :return: LogConfigOutputDto
        """
        return self._execute_with_experimentid_arguments(
            self._client.jasmine.get_log_config,
            log_config_input)
