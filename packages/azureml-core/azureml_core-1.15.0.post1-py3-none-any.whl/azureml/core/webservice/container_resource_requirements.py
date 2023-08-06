# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module for describing Container Resource Requirements in Azure Machine Learning."""


import logging
from azureml.exceptions import WebserviceException
module_logger = logging.getLogger(__name__)


class ContainerResourceRequirements(object):
    """Defines the resource requirements for a container used by the Webservice.

    To specify autoscaling configuration, you will typically use the ``deploy_configuration``
    method of the :class:`azureml.core.webservice.aks.AksWebservice` class or the
    :class:`azureml.core.webservice.aci.AciWebservice` class.

    :param cpu: The number of CPU cores to allocate for this Webservice. Can be a decimal.
    :type cpu: float
    :param memory_in_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal.
    :type memory_in_gb: float
    :param gpu: The number of GPU cores to allocate for this Webservice.
    :type gpu: int
    """

    _expected_payload_keys = ['cpu', 'memoryInGB', 'gpu']

    def __init__(self, cpu, memory_in_gb, gpu=None):
        """Initialize the container resource requirements.

        :param cpu: The number of CPU cores to allocate for this Webservice. Can be a decimal.
        :type cpu: float
        :param memory_in_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal.
        :type memory_in_gb: float
        :param gpu: The number of GPU cores to allocate for this Webservice.
        :type gpu: int
        """
        self.cpu = cpu
        self.memory_in_gb = memory_in_gb
        self.gpu = gpu

    def serialize(self):
        """Convert this ContainerResourceRequirements object into a JSON serialized dictionary.

        :return: The JSON representation of this ContainerResourceRequirements.
        :rtype: dict
        """
        return {'cpu': self.cpu, 'memoryInGB': self.memory_in_gb, 'gpu': self.gpu}

    @staticmethod
    def deserialize(payload_obj):
        """Convert a JSON object into a ContainerResourceRequirements object.

        :param payload_obj: A JSON object to convert to a ContainerResourceRequirements object.
        :type payload_obj: dict
        :return: The ContainerResourceRequirements representation of the provided JSON object.
        :rtype: azureml.core.webservice.webservice.ContainerResourceRequirements
        """
        for payload_key in ContainerResourceRequirements._expected_payload_keys:
            if payload_key not in payload_obj:
                raise WebserviceException('Invalid webservice payload, missing {} for ContainerResourceRequirements:\n'
                                          '{}'.format(payload_key, payload_obj), logger=module_logger)

        return ContainerResourceRequirements(payload_obj['cpu'], payload_obj['memoryInGB'], payload_obj['gpu'])
