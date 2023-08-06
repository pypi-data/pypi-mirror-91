# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains configurations that specifies how outputs for a job should be uploaded and promoted to a dataset.

For more information, see the article [how to specify
outputs](https://docs.microsoft.com/azure/machine-learning/how-to-create-register-datasets).
"""
from copy import deepcopy
from uuid import uuid4

from azureml._base_sdk_common._docstring_wrapper import experimental
from azureml.data._loggerfactory import _LoggerFactory, track
from azureml.data.constants import UPLOAD_MODE, MOUNT_MODE, DIRECT_MODE, _PUBLIC_API
from azureml.data._dataprep_helper import dataprep
from azureml.data._partition_format import handle_partition_format
from azureml.data.dataset_factory import _set_column_types
from azureml.data.dataset_type_definitions import PromoteHeadersBehavior


_logger = None


def _get_logger():
    global _logger
    if _logger is None:
        _logger = _LoggerFactory.get_logger(__name__)
    return _logger


@experimental
class OutputDatasetConfig:
    """Represent how to copy the output of a job to a remote storage location and be promoted to a Dataset.

    This is the base class used to represent how to copy the output of a job to a remote storage location, whether
    to register it as a named and versioned Dataset, and whether to apply any additional transformations to
    the Dataset that was created.

    You should not be creating instances of this class directly but instead should use the appropriate subclass.
    """

    @track(_get_logger, activity_type=_PUBLIC_API)
    def __init__(self, mode, name=None, **kwargs):
        """Initialize a OutputDatasetConfig.

        :param mode: The mode in which to copy the output to the remote storage.
        :type mode: str
        :param name: The name of the output specific to the run it will be produced in.
        :type name: str
        """
        self.name = name or OutputDatasetConfig._generate_random_name('output')
        self.mode = mode
        self._additional_transformations = kwargs.get('additional_transformations')
        self._registration = kwargs.get('registration')
        self._origin = _Origin()

    @track(_get_logger, activity_type=_PUBLIC_API)
    def register_on_complete(self, name, description=None, tags=None):
        """Register the output as a new version of a named Dataset after the run has ran.

        If the named Dataset does not exists, it will be created and a new version will be created for the newly
        created named Dataset.

        :param name: The Dataset name to register the output under.
        :type name: str
        :param description: The description for the Dataset.
        :type description: str
        :param tags: A list of tags to be assigned to the Dataset.
        :type tags: dict[str, str]
        :return: A new :class:`azureml.data.output_dataset_config.OutputDatasetConfig` instance with the registration
            information.
        :rtype: azureml.data.output_dataset_config.OutputDatasetConfig
        """
        if not name:
            raise ValueError('The registration name of the dataset must not be empty.')
        copy = deepcopy(self)
        copy._registration = RegistrationConfiguration(name, description, tags)
        return copy

    def as_input(self, name=None):
        """Specify how to consume the output as an input in subsequent pipeline steps.

        :param name: The name of the input specific to the run.
        :type name: str
        :return: A :class:`azureml.data.dataset_consumption_config.DatasetConsumptionConfig` instance describing
            how to deliver the input data.
        :rtype: azureml.data.dataset_consumption_config.DatasetConsumptionConfig
        """
        raise NotImplementedError()

    @staticmethod
    def _generate_random_name(prefix):
        return '{}_{}'.format(prefix, str(uuid4()).split('-')[0])

    def _to_output_data(self):
        from azureml.core.runconfig import OutputData, RegistrationOptions, OutputOptions, DatasetRegistrationOptions

        def to_registration(registration):
            dataflow_json = self._additional_transformations.to_json() if self._additional_transformations else None
            dataset_registration_options = DatasetRegistrationOptions(dataflow_json)
            if not registration:
                return RegistrationOptions(dataset_registration_options=dataset_registration_options)
            return RegistrationOptions(registration.name, registration.description, registration.tags,
                                       dataset_registration_options=dataset_registration_options)

        registration = to_registration(self._registration)
        output_options = OutputOptions(registration_options=registration)
        return OutputData(mechanism=self.mode, additional_options=output_options)

    def _set_producer(self, step):
        """Pipeline specific method."""
        self._origin.producer_step = step

    @property
    def _producer(self):
        """Pipeline specific property."""
        return self._origin.producer_step


@experimental
class OutputFileDatasetConfig(OutputDatasetConfig):
    """Represent how to copy the output of a run and be promoted as a FileDataset."""

    @track(_get_logger, custom_dimensions={'app_name': 'OutputFileDatasetConfig'}, activity_type=_PUBLIC_API)
    def __init__(self, name=None, destination=None, source=None):
        """Initialize a OutputFileDatasetConfig.

        .. remarks::
            You can pass the OutputFileDatasetConfig as an argument to your run, and it will be automatically
            translated into local path on the compute. The source argument will be used if one is specified,
            otherwise we will automatically generate a directory in the OS's temp folder. The files and folders inside
            the source directory will then be copied to the destination based on the output configuration.

            By default the mode by which the output will be copied to the destination storage will be set to mount.
            For more information about mount mode, please see the documentation for as_mount.

        :param name: The name of the output specific to this run. This is generally used for lineage purposes. If set
            to None, we will automatically generate a name.
        :type name: str
        :param destination: The destination to copy the output to. If set to None, we will copy the output to the
            workspaceblobstore datastore, under the path /dataset/{run-id}/{output-name}, where `run-id` is the Run's
            ID and the `output-name` is the output name from the `name` parameter above. The destination is a tuple
            where the first item is the datastore and the second item is the path within the datastore to copy the
            data to.

            The path within the datastore can be a template path. A template path is just a regular path but with
            placeholders inside. Those placeholders will then be resolved at the appropriate time. The syntax for
            placeholders is {placeholder}, for example, /path/with/{placeholder}. Currently only two placeholders
            are supported, {run-id} and {output-name}.
        :type destination: tuple
        :param source: The path with in the compute target to copy the data to the destination. If set to None, we
            will set this to a directory we create inside the compute target's OS temporary directory.
        :type source: str
        """
        super(OutputFileDatasetConfig, self).__init__(MOUNT_MODE, name)
        self.destination = destination
        self.source = source
        self._upload_options = None

    @track(_get_logger, custom_dimensions={'app_name': 'OutputFileDatasetConfig'}, activity_type=_PUBLIC_API)
    def as_mount(self):
        """Set the mode of the output to mount.

        For mount mode, the output directory will be a FUSE mounted directory. Files written to the mounted directory
        will be uploaded when the file is closed.

        :return: A :class:`azureml.data.OutputFileDatasetConfig` instance with mode set to mount.
        :rtype: azureml.data.OutputFileDatasetConfig
        """
        copy = deepcopy(self)
        copy.mode = MOUNT_MODE
        copy._upload_options = None
        return copy

    @track(_get_logger, custom_dimensions={'app_name': 'OutputFileDatasetConfig'}, activity_type=_PUBLIC_API)
    def as_upload(self, overwrite=False, source_globs=None):
        """Set the mode of the output to upload.

        For upload mode, files written to the output directory will be uploaded at the end of the job. If the job
        fails or gets canceled, then the output directory will not be uploaded.

        :param overwrite: Whether to overwrite files that already exists in the destination.
        :type overwrite: bool
        :param source_globs: Glob patterns used to filter files that will be uploaded.
        :type source_globs: builtin.list[str]
        :return: A :class:`azureml.data.OutputFileDatasetConfig` instance with mode set to upload.
        :rtype: azureml.data.OutputFileDatasetConfig
        """
        copy = deepcopy(self)
        copy.mode = UPLOAD_MODE
        copy._upload_options = UploadOptions(overwrite, source_globs)
        return copy

    @track(_get_logger, custom_dimensions={'app_name': 'OutputFileDatasetConfig'}, activity_type=_PUBLIC_API)
    def as_input(self, name=None):
        """Specify how to consume the output as an input in subsequent pipeline steps.

        :param name: The name of the input specific to the run.
        :type name: str
        :return: A :class:`azureml.data.dataset_consumption_config.DatasetConsumptionConfig` instance describing
            how to deliver the input data.
        :rtype: azureml.data.dataset_consumption_config.DatasetConsumptionConfig
        """
        from azureml.data.dataset_consumption_config import DatasetConsumptionConfig

        name = name or self.__class__._generate_random_name('input')
        return DatasetConsumptionConfig(name, self, 'mount')

    @track(_get_logger, custom_dimensions={'app_name': 'OutputFileDatasetConfig'}, activity_type=_PUBLIC_API)
    def read_delimited_files(
            self, include_path=False, separator=',', header=PromoteHeadersBehavior.ALL_FILES_HAVE_SAME_HEADERS,
            partition_format=None, path_glob=None, set_column_types=None
    ):
        """Transform the output dataset to a tabular dataset by reading all the output as delimited files.

        :param include_path: Boolean to keep path information as column in the dataset. Defaults to False.
            This is useful when reading multiple files, and want to know which file a particular record
            originated from, or to keep useful information in file path.
        :type include_path: bool
        :param separator: The separator used to split columns.
        :type separator: str
        :param header: Controls how column headers are promoted when reading from files. Defaults to assume
            that all files have the same header.
        :type header: azureml.data.dataset_type_definitions.PromoteHeadersBehavior
        :param partition_format: Specify the partition format of path. Defaults to None.
            The partition information of each path will be extracted into columns based on the specified format.
            Format part '{column_name}' creates string column, and '{column_name:yyyy/MM/dd/HH/mm/ss}' creates
            datetime column, where 'yyyy', 'MM', 'dd', 'HH', 'mm' and 'ss' are used to extract year, month, day,
            hour, minute and second for the datetime type. The format should start from the position of first
            partition key until the end of file path.
            For example, given the path '../Accounts/2019/01/01/data.parquet' where the partition is by
            department name and time, partition_format='/{Department}/{PartitionDate:yyyy/MM/dd}/data.parquet'
            creates a string column 'Department' with the value 'Accounts' and a datetime column 'PartitionDate'
            with the value '2019-01-01'.
        :type partition_format: str
        :param path_glob: A glob pattern to filter files that will be read as delimited files. If set to None, then
            all files will be read as delimited files.
        :type path_glob: str
        :param set_column_types: A dictionary to set column data type, where key is column name and value is
            :class:`azureml.data.DataType`. Columns not in the dictionary will remain of type string. Passing None
            will result in no conversions. Entries for columns not found in the source data will not cause an error
            and will be ignored.
        :type set_column_types: dict[str, azureml.data.DataType]
        :return: A :class:`azureml.data.output_dataset_config.OutputTabularDatasetConfig` instance with instruction of
            how to convert the output into a TabularDataset.
        :rtype: azureml.data.output_dataset_config.OutputTabularDatasetConfig
        """
        dprep = dataprep()
        dataflow = dprep.Dataflow(self._engine_api)
        dataflow = OutputFileDatasetConfig._filter_path(dprep, dataflow, path_glob)
        dataflow = dataflow.parse_delimited(
            separator=separator, headers_mode=header, encoding=dprep.FileEncoding.UTF8, quoting=False,
            skip_rows=0, skip_mode=dprep.SkipMode.NONE, comment=None
        )
        if partition_format:
            dataflow = handle_partition_format(dataflow, partition_format)
        dataflow = OutputFileDatasetConfig._handle_path(dataflow, include_path)
        dataflow = _set_column_types(dataflow, set_column_types)
        return _create_tabular_dataset_with_dataflow(self, dataflow)

    @track(_get_logger, custom_dimensions={'app_name': 'OutputFileDatasetConfig'}, activity_type=_PUBLIC_API)
    def read_parquet_files(self, include_path=False, partition_format=None, path_glob=None,
                           set_column_types=None):
        """Transform the output dataset to a tabular dataset by reading all the output as delimited files.

        The tabular dataset is created by parsing the parquet file(s) pointed to by the intermediate output.

        :param include_path: Boolean to keep path information as column in the dataset. Defaults to False.
            This is useful when reading multiple files, and want to know which file a particular record
            originated from, or to keep useful information in file path.
        :type include_path: bool
        :param partition_format: Specify the partition format of path. Defaults to None.
            The partition information of each path will be extracted into columns based on the specified format.
            Format part '{column_name}' creates string column, and '{column_name:yyyy/MM/dd/HH/mm/ss}' creates
            datetime column, where 'yyyy', 'MM', 'dd', 'HH', 'mm' and 'ss' are used to extract year, month, day,
            hour, minute and second for the datetime type. The format should start from the position of first
            partition key until the end of file path.
            For example, given the path '../Accounts/2019/01/01/data.parquet' where the partition is by
            department name and time, partition_format='/{Department}/{PartitionDate:yyyy/MM/dd}/data.parquet'
            creates a string column 'Department' with the value 'Accounts' and a datetime column 'PartitionDate'
            with the value '2019-01-01'.
        :type partition_format: str
        :param path_glob: A glob pattern to filter files that will be read as parquet files. If set to None, then
            all files will be read as parquet files.
        :type path_glob: str
        :param set_column_types: A dictionary to set column data type, where key is column name and value is
            :class:`azureml.data.DataType`. Columns not in the dictionary will remain of type loaded from the parquet
            file. Passing None will result in no conversions. Entries for columns not found in the source data will
            not cause an error and will be ignored.
        :type set_column_types: dict[str, azureml.data.DataType]
        :return: A :class:`azureml.data.output_dataset_config.OutputTabularDatasetConfig` instance with instruction of
            how to convert the output into a TabularDataset.
        :rtype: azureml.data.output_dataset_config.OutputTabularDatasetConfig
        """
        dprep = dataprep()
        dataflow = dprep.Dataflow(self._engine_api)
        dataflow = OutputFileDatasetConfig._filter_path(dprep, dataflow, path_glob)
        dataflow = dataflow.read_parquet_file()
        if partition_format:
            dataflow = handle_partition_format(dataflow, partition_format)
        dataflow = OutputFileDatasetConfig._handle_path(dataflow, include_path)
        dataflow = _set_column_types(dataflow, set_column_types)
        return _create_tabular_dataset_with_dataflow(self, dataflow)

    @property
    def _engine_api(self):
        return dataprep().api.engineapi.api.get_engine_api()

    def _to_output_data(self):
        from azureml.core.runconfig import DataLocation, DataPath, UploadOptions as RunConfigUploadOptions,\
            GlobsOptions

        def to_data_location(destination):
            if not destination:
                return None
            try:
                datastore_name = destination[0].name
            except AttributeError:
                datastore_name = destination[0]
            return DataLocation(data_path=DataPath(datastore_name, *destination[1:]))

        def to_upload_options(mode, upload_options):
            if mode != UPLOAD_MODE:
                if upload_options:
                    raise ValueError('Mode is not set to upload but an UploadOption is provided. Please make sure the '
                                     'mode is set to upload by calling as_upload.')
                return None
            if upload_options:
                globs = to_globs(upload_options.source_globs)
                return RunConfigUploadOptions(upload_options.overwrite, globs)
            return RunConfigUploadOptions(False, None)

        def to_globs(globs):
            if not globs:
                return None
            if not isinstance(globs, list):
                globs = [globs]
            return GlobsOptions(globs)

        output_data = super(OutputFileDatasetConfig, self)._to_output_data()
        output_data.output_location = to_data_location(self.destination)
        upload_options = to_upload_options(self.mode, self._upload_options)
        output_data.additional_options.upload_options = upload_options
        output_data.additional_options.path_on_compute = self.source
        return output_data

    @staticmethod
    def _filter_path(dprep, dataflow, path_glob):
        if not path_glob:
            return dataflow

        return dataflow.filter(
            dprep.Regex(path_glob).is_match(dprep.api.functions.get_stream_name(dataflow['Path']))
        )

    @staticmethod
    def _handle_path(dataflow, include_path):
        if not include_path:
            return dataflow.drop_columns('Path')
        return dataflow


@experimental
class OutputTabularDatasetConfig(OutputDatasetConfig):
    """Represent how to copy the output of a run and be promoted as a TabularDataset."""

    @track(_get_logger, custom_dimensions={'app_name': 'OutputTabularDatasetConfig'}, activity_type=_PUBLIC_API)
    def __init__(self, **kwargs):
        """Initialize a OutputTabularDatasetConfig.

        .. remarks::
            You should not call this constructor directly, but instead should create a FileOutputDatasetConfig and then
            calling the corresponding read_* methods to convert it into a OutputTabularDatasetConfig.

            The way the output will be copied to the destination for a OutputTabularDatasetConfig is the same as a
            OutputFileDatasetConfig. The difference between them is that the Dataset that is created will be a
            TabularDataset containing all the specified transformations.

        """
        output_file_dataset_config = kwargs.get('output_file_dataset_config')

        if not output_file_dataset_config:
            raise ValueError('The constructor of this class is not supposed to be called directly. Please create '
                             'an OutputFileDatasetConfig and add additional transforms to get a '
                             'OutputTabularDatasetConfig.')

        super(OutputTabularDatasetConfig, self).__init__(
            output_file_dataset_config.mode,
            output_file_dataset_config.name,
            additional_transformations=output_file_dataset_config._additional_transformations
        )
        self._output_file_dataset_config = output_file_dataset_config
        self._origin = output_file_dataset_config._origin

    @track(_get_logger, custom_dimensions={'app_name': 'OutputTabularDatasetConfig'}, activity_type=_PUBLIC_API)
    def keep_columns(self, columns):
        """Keep the specified columns and drops all others from the Dataset.

        :param columns: The name or a list of names for the columns to keep.
        :type columns: str or buildin.list[str]
        :return: A :class:`azureml.data.output_dataset_config.OutputTabularDatasetConfig` instance with which columns
            to keep.
        :rtype: azureml.pipeline.core.pipeline_output_dataset.PipelineOutputTabularDataset
        """
        dataflow = self._additional_transformations.keep_columns(columns)
        return _create_tabular_dataset_with_dataflow(self._output_file_dataset_config, dataflow)

    @track(_get_logger, custom_dimensions={'app_name': 'OutputTabularDatasetConfig'}, activity_type=_PUBLIC_API)
    def drop_columns(self, columns):
        """Drop the specified columns from the Dataset.

        :param columns: The name or a list of names for the columns to drop.
        :type columns: str or builtin.list[str]
        :return: A :class:`azureml.data.output_dataset_config.OutputTabularDatasetConfig` instance with which columns
            to drop.
        :rtype: azureml.pipeline.core.pipeline_output_dataset.PipelineOutputTabularDataset
        """
        dataflow = self._additional_transformations.drop_columns(columns)
        return _create_tabular_dataset_with_dataflow(self._output_file_dataset_config, dataflow)

    @track(_get_logger, custom_dimensions={'app_name': 'OutputTabularDatasetConfig'}, activity_type=_PUBLIC_API)
    def random_split(self, percentage, seed=None):
        """Split records in the dataset into two parts randomly and approximately by the percentage specified.

        The resultant output configs will have their names changed, the first one will have _1 appended to the name
        and the second one will have _2 appended to the name. If it will cause a name collision or you would like to
        specify a custom name, please manually set their names.

        :param percentage: The approximate percentage to split the dataset by. This must be a number between
            0.0 and 1.0.
        :type percentage: float
        :param seed: Optional seed to use for the random generator.
        :type seed: int
        :return: Returns a tuple of two OutputTabularDatasetConfig objects representing the two Datasets after the
            split.
        :rtype: (azureml.data.output_dataset_config.OutputTabularDatasetConfig,
            azureml.data.output_dataset_config.OutputTabularDatasetConfig)
        """
        dataflow1, dataflow2 = self._additional_transformations.random_split(percentage, seed)
        first = _create_tabular_dataset_with_dataflow(self._output_file_dataset_config, dataflow1)
        second = _create_tabular_dataset_with_dataflow(self._output_file_dataset_config, dataflow2)
        first.name += '_1'
        second.name += '_2'
        return first, second

    @track(_get_logger, custom_dimensions={'app_name': 'OutputTabularDatasetConfig'}, activity_type=_PUBLIC_API)
    def as_mount(self):
        """Set the mode of the output to mount.

        For mount mode, the output directory will be a FUSE mounted directory. Files written to the mounted directory
        will be uploaded when the file is closed.

        :return: A :class:`azureml.data.output_dataset_config.OutputTabularDatasetConfig` instance with mode set to
            mount.
        :rtype: azureml.data.output_dataset_config.OutputTabularDatasetConfig
        """
        copy = deepcopy(self)
        copy.mode = MOUNT_MODE
        copy._output_file_dataset_config.mode = MOUNT_MODE
        copy._output_file_dataset_config._upload_options = None
        return copy

    @track(_get_logger, custom_dimensions={'app_name': 'OutputTabularDatasetConfig'}, activity_type=_PUBLIC_API)
    def as_upload(self, overwrite=False, source_globs=None):
        """Set the mode of the output to upload.

        For upload mode, files written to the output directory will be uploaded at the end of the job. If the job
        fails or gets canceled, then the output directory will not be uploaded.

        :param overwrite: Whether to overwrite files that already exists in the destination.
        :type overwrite: bool
        :param source_globs: Glob patterns used to filter files that will be uploaded.
        :type source_globs: builtin.list[str]
        :return: A :class:`azureml.data.output_dataset_config.OutputTabularDatasetConfig` instance with mode set to
            upload.
        :rtype: azureml.data.output_dataset_config.OutputTabularDatasetConfig
        """
        copy = deepcopy(self)
        copy.mode = UPLOAD_MODE
        copy._output_file_dataset_config.mode = UPLOAD_MODE
        copy._output_file_dataset_config._upload_options = UploadOptions(overwrite, source_globs)
        return copy

    @track(_get_logger, custom_dimensions={'app_name': 'OutputTabularDatasetConfig'}, activity_type=_PUBLIC_API)
    def as_input(self, name=None):
        """Specify how to consume the output as an input in subsequent pipeline steps.

        :param name: The name of the input specific to the run.
        :type name: str
        :return: A :class:`azureml.data.dataset_consumption_config.DatasetConsumptionConfig` instance describing
            how to deliver the input data.
        :rtype: azureml.data.dataset_consumption_config.DatasetConsumptionConfig
        """
        from azureml.data.dataset_consumption_config import DatasetConsumptionConfig

        name = name or self.__class__._generate_random_name('input')
        return DatasetConsumptionConfig(name, self, DIRECT_MODE)

    def _to_output_data(self):
        return self._output_file_dataset_config._to_output_data()


@experimental
class UploadOptions:
    """Options that are specific to output which will be uploaded."""

    def __init__(self, overwrite=False, source_globs=None):
        """Initialize a UploadOptions.

        :param overwrite: Whether to overwrite files that already exists in the destination.
        :type overwrite: bool
        :param source_globs: Glob patterns used to filter files that will be uploaded.
        :type source_globs: builtin.list[str]
        """
        if source_globs is not None and not isinstance(source_globs, list):
            source_globs = [source_globs]
        self.overwrite = overwrite
        self.source_globs = source_globs


@experimental
class RegistrationConfiguration:
    """Configuration that specifies how to register the output as a Dataset."""

    def __init__(self, name, description, tags):
        """Initialize a RegistrationConfiguration.

        :param name: The Dataset name to register the output under.
        :type name: str
        :param description: The description for the Dataset.
        :type description: str
        :param tags: A list of tags to be assigned to the Dataset.
        :type tags: dict[str, str]
        """
        self.name = name
        self.description = description
        self.tags = tags


class _Origin:
    """A special class that will not be copied/deepcopied.

    The purpose of this class is to have the ability to track things that will not be copied/deepcopied when
    copy and deepcopy is called. OutputDatasetConfig follows dataflow's pattern of creating a new copy of itself
    whenever any methods are called, this is desirable in most cases but for building pipeline, pipeline by default
    captures closures, this means you don't need to explicitly specify the order of steps and the pipeline SDK
    is able to figure this out on its own. To do so, when an output is passed to a step, it sets it producer_step in
    the output to that step, and later when it constructs the graph, the input instance of this output needs to figure
    out which output the input came from, it does this by querying its producer_step property. This won't work
    if we deep copy everything, which is why we have this class which overrides the behavior of copy and deepcopy
    so these things are not copied and shared between all the copied instances.
    """

    def __init__(self):
        self.producer_step = None

    def __copy__(self):
        return self

    def __deepcopy__(self, memodict={}):
        return self


def _create_tabular_dataset_with_dataflow(output_file_dataset, dataflow):
    copy = deepcopy(output_file_dataset)
    copy._additional_transformations = dataflow
    return OutputTabularDatasetConfig(output_file_dataset_config=copy)
