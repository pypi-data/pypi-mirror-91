# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""AutoML object in charge of orchestrating various AutoML runs for predicting models."""
import json
import logging
import os
import os.path
import shutil
import sys
import warnings
from pathlib import Path
from types import ModuleType
from typing import Any, cast, List, Optional, Dict, Union

from azureml._common._error_definition import AzureMLError
from azureml._common._error_definition.user_error import NotFound
from azureml._common.exceptions import AzureMLException
from azureml._restclient.constants import RunStatus, SNAPSHOT_MAX_FILES, ONE_MB,\
    SNAPSHOT_MAX_SIZE_BYTES
from azureml._restclient.experiment_client import ExperimentClient
from azureml._restclient.jasmine_client import JasmineClient
from azureml._restclient.models.create_parent_run import CreateParentRun
from azureml._restclient.models import LocalRunGetNextTaskBatchInput, LocalRunGetNextTaskInput, \
    MiroProxyInput
from azureml._restclient.models.run_dto import RunDto
from azureml._tracing._tracer_factory import get_tracer
from azureml.automl.core import dataprep_utilities, dataset_utilities, package_utilities
from azureml.automl.core._run import run_lifecycle_utilities
from azureml.automl.core.console_writer import ConsoleWriter
from azureml.automl.core.constants import RunHistoryEnvironmentVariableNames
from azureml.automl.core.shared import import_utilities, logging_utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    AutoMLInternal,
    ExecutionFailure,
    InvalidArgumentType,
    InvalidArgumentWithSupportedValues,
    RuntimeModuleDependencyMissing,
    SnapshotLimitExceeded)
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.constants import TelemetryConstants
from azureml.automl.core.shared.exceptions import (
    AutoMLException, ClientException, ConfigException, ValidationException)
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.systemusage_telemetry import SystemResourceUsageTelemetryFactory
from azureml.core import Experiment, Run
from azureml.core._serialization_utils import _serialize_to_dict
from azureml.core.compute_target import AbstractComputeTarget
from azureml.core.runconfig import RunConfiguration
from azureml.exceptions import ServiceException as AzureMLServiceException, SnapshotException
from . import constants, _logging
from ._automl_feature_config_manager import AutoMLFeatureConfigManager
from ._azureautomlsettings import AzureAutoMLSettings
from ._environment_utilities import modify_run_configuration
from ._local_managed_utils import local_managed
from .constants import Framework
from ._remote_console_interface import RemoteConsoleInterface
from .exceptions import FetchNextIterationException
from .run import AutoMLRun
from .utilities import _InternalComputeTypes
from msrest.exceptions import ClientRequestError

logger = logging.getLogger(__name__)
tracer = get_tracer(__name__)


class AzureAutoMLClient:
    """Client to run AutoML experiments on Azure Machine Learning platform."""

    # constants for run properties
    DISPLAY_TASK_TYPE_PROPERTY = 'display_task_type'
    SDK_DEPENDENCIES_PROPERTY = 'dependencies_versions'

    def __init__(self, experiment: Experiment, settings: AzureAutoMLSettings):
        """
        Create an AzureAutoMLClient.

        :param settings: the AutoML settings to use
        """
        self.automl_settings = settings
        self.experiment = experiment

        self._status = constants.Status.NotStarted
        self._loop = None
        self._score_best = None
        self._console_writer = ConsoleWriter()

        self.parent_run_id = None   # type: Optional[str]
        self.current_iter = None
        self.input_data = None      # type: Optional[Dict[str, Union[Any, Any]]]
        self._adb_thread = None
        self.onnx_cvt = None        # runtime_type: Optional[OnnxConverter]

        self._check_create_folders(self.automl_settings.path)

        self._usage_telemetry = SystemResourceUsageTelemetryFactory.get_system_usage_telemetry()

        self.experiment_start_time = None

        if not self.automl_settings.show_warnings:
            # sklearn forces warnings, so we disable them here
            warnings.simplefilter('ignore', DeprecationWarning)
            warnings.simplefilter('ignore', RuntimeWarning)
            warnings.simplefilter('ignore', UserWarning)
            warnings.simplefilter('ignore', FutureWarning)

        # Setup the user script.
        self._setup_data_script()

        # Set up clients to communicate with AML services
        self._jasmine_client = JasmineClient(service_context=self.experiment.workspace.service_context,
                                             experiment_name=self.experiment.name,
                                             experiment_id=self.experiment.id,
                                             host=self.automl_settings.service_url)
        self.feature_config_manager = AutoMLFeatureConfigManager(self._jasmine_client)
        self.experiment_client = ExperimentClient(service_context=self.experiment.workspace.service_context,
                                                  experiment_name=self.experiment.name,
                                                  experiment_id=self.experiment.id,
                                                  host=self.automl_settings.service_url)

        self.current_run = None     # type: Optional[AutoMLRun]

    @property
    def logger(self):
        return logger

    def cancel(self):
        """
        Cancel the ongoing local run.

        :return: None
        """
        self._status = constants.Status.Terminated

    def _setup_data_script(self) -> None:
        module_path = self.automl_settings.data_script
        if self.automl_settings.data_script is not None:
            # Show warnings to user when use the data_script.
            warnings.warn('Please make sure in the data script the data script '
                          'uses the paths of data files on the remote machine.'
                          'The data script is not recommended anymore, '
                          'please take a look at the latest documentation to use the dprep interface.')

            is_data_script_in_proj_dir = True
            if not os.path.exists(self.automl_settings.data_script):
                # Check if the data_script is a relative sub path from the project path (automl_settings.path)
                script_path = os.path.join(self.automl_settings.path,
                                           self.automl_settings.data_script)
                if os.path.exists(script_path):
                    module_path = script_path
                else:
                    raise ConfigException._with_error(
                        AzureMLError.create(NotFound, target="data_script", resource_name=script_path)
                    )
            else:
                # Check if the data_script path is under the project path or it's sub folders.
                try:
                    path_script = Path(self.automl_settings.data_script)
                    path_project = Path(self.automl_settings.path)
                    if path_project not in path_script.parents:
                        is_data_script_in_proj_dir = False
                except Exception:
                    is_data_script_in_proj_dir = False
                module_path = self.automl_settings.data_script

            # Check if the data_script path is actually a file path.
            if not os.path.isfile(module_path):
                raise ConfigException._with_error(
                    AzureMLError.create(
                        InvalidArgumentType, target="data_script",
                        argument=str(module_path), actual_type="Directory",
                        expected_types="File")
                )

            # Make sure the script_path (the data script path) has the script file named as DATA_SCRIPT_FILE_NAME.
            module_file_name = os.path.basename(module_path)
            if module_file_name != constants.DATA_SCRIPT_FILE_NAME:
                raise ConfigException._with_error(
                    AzureMLError.create(
                        InvalidArgumentWithSupportedValues, target="data_script",
                        arguments=module_file_name, supported_values=constants.DATA_SCRIPT_FILE_NAME
                    )
                )

            # If data_script is not in project folder, copy the data_script file into the project folder.
            # We'll take the snapshot of the project folder.
            if not is_data_script_in_proj_dir:
                # Need to copy the data script file.
                des_module_path = os.path.join(self.automl_settings.path,
                                               constants.DATA_SCRIPT_FILE_NAME)
                if os.path.abspath(module_path) != os.path.abspath(des_module_path):
                    shutil.copy(os.path.abspath(module_path), des_module_path)
                module_path = des_module_path

            try:
                import azureml.train.automl.runtime
                from azureml.train.automl.runtime import utilities as utils
                from azureml.automl.runtime import training_utilities
                from azureml.automl.runtime.shared import utilities as runtime_utilities
                self.user_script = utils._load_user_script(module_path)  # type: Optional[ModuleType]
                self.input_data = training_utilities._extract_user_data(self.user_script)
                training_utilities.auto_block_models(self.input_data, self.automl_settings)
                if self.automl_settings.exclude_nan_labels:
                    self.input_data = runtime_utilities._y_nan_check(self.input_data)
            except AzureMLException:
                raise
            except ImportError as e:
                raise ConfigException._with_error(
                    AzureMLError.create(RuntimeModuleDependencyMissing, target="data_script", module_name=e.name),
                    inner_exception=e
                ) from e
            except Exception as e:
                logging_utilities.log_traceback(e, logger)
                logger.error('Failed to load the data from user provided get_data script.')
                raise ClientException._with_error(
                    AzureMLError.create(AutoMLInternal, error_details=str(e), target="data_script",
                                        reference_code=ReferenceCodes._DATA_SCRIPT_INTERNAL_ERROR),
                    inner_exception=e
                ) from e
        else:
            self.user_script = None

    def fit(self,
            run_configuration: Optional[RunConfiguration] = None,
            compute_target: Optional[Union[AbstractComputeTarget, str]] = None,
            X: Optional[Any] = None,
            y: Optional[Any] = None,
            sample_weight: Optional[Any] = None,
            X_valid: Optional[Any] = None,
            y_valid: Optional[Any] = None,
            sample_weight_valid: Optional[Any] = None,
            cv_splits_indices: Optional[List[Any]] = None,
            show_output: bool = False,
            existing_run: bool = False,
            training_data: Optional[Any] = None,
            validation_data: Optional[Any] = None,
            test_data: Optional[Any] = None,
            _script_run: Optional[Run] = None,
            parent_run_id: Optional[Any] = None,
            is_managed: bool = False,
            kwargs: Optional[Dict[str, Any]] = None) -> AutoMLRun:
        """
        Start a new AutoML execution on the specified compute target.

        :param run_configuration: The run confiuguration used by AutoML, should contain a compute target for remote
        :type run_configuration: Azureml.core RunConfiguration
        :param compute_target: The AzureML compute node to run this experiment on
        :type compute_target: azureml.core.compute.AbstractComputeTarget
        :param X: Training features
        :type X: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow or
                 azureml.core.Dataset, azureml.data.dataset_definition.DatasetDefinition
                 or azureml.data.TabularDataset
        :param y: Training labels
        :type y: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow or
                 azureml.core.Dataset, azureml.data.dataset_definition.DatasetDefinition
                 or azureml.data.TabularDataset
        :param sample_weight:
        :type sample_weight: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
                or azureml.data.TabularDataset
        :param X_valid: validation features
        :type X_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow or
                   azureml.core.Dataset, azureml.data.dataset_definition.DatasetDefinition
                   or azureml.data.TabularDataset
        :param y_valid: validation labels
        :type y_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow or
                   azureml.core.Dataset, azureml.data.dataset_definition.DatasetDefinition
                   or azureml.data.TabularDataset
        :param sample_weight_valid: validation set sample weights
        :type sample_weight_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
                or azureml.data.TabularDataset
        :param cv_splits_indices: Indices where to split training data for cross validation
        :type cv_splits_indices: list(int), or list(Dataflow) in which each Dataflow represent a train-valid set
                                 where 1 indicates record for training and 0 indicates record for validation
        :param show_output: Flag whether to print output to console
        :type show_output: bool
        :param existing_run: Flag whether this is a continuation of a previously completed experiment
        :type existing_run: bool
        :param _script_run: Run to associate with parent run id
        :type _script_run: azureml.core.Run
        :return: AutoML parent run
        :rtype: azureml.train.automl.AutoMLRun
        """
        self._status = constants.Status.Started

        # Save these params for local managed
        data_params = {
            'training_data': training_data,
            'validation_data': validation_data,
            'X': X,
            'y': y,
            'sample_weight': sample_weight,
            'X_valid': X_valid,
            'y_valid': y_valid,
            'sample_weight_valid': sample_weight_valid,
            'cv_splits_indices': cv_splits_indices}

        if show_output:
            self._console_writer = ConsoleWriter(sys.stdout)

        if run_configuration is None:
            run_configuration = RunConfiguration()
            if compute_target is not None:
                run_configuration.target = compute_target  # this will handle str or compute_target
                self._console_writer.println('No run_configuration provided, running on {0} with default configuration'
                                             .format(run_configuration.target))
            else:
                self._console_writer.println(
                    'No run_configuration provided, running locally with default configuration')
            if run_configuration.target != 'local':
                run_configuration.environment.docker.enabled = True
        if run_configuration.framework.lower() not in list(Framework.FULL_SET):
            raise ConfigException._with_error(
                AzureMLError.create(
                    InvalidArgumentWithSupportedValues, target="run_configuration",
                    arguments=run_configuration.framework,
                    supported_values=list(Framework.FULL_SET)
                )
            )

        self.automl_settings.compute_target = run_configuration.target

        self.automl_settings.azure_service = _InternalComputeTypes.identify_compute_type(
            compute_target=self.automl_settings.compute_target,
            azure_service=self.automl_settings.azure_service)

        # Save the Dataset to Workspace so that its saved id will be logged for telemetry and lineage
        dataset_utilities.ensure_saved(
            self.experiment.workspace, X=X, y=y, sample_weight=sample_weight, X_valid=X_valid, y_valid=y_valid,
            sample_weight_valid=sample_weight_valid, training_data=training_data, validation_data=validation_data,
            test_data=test_data
        )

        dataset_utilities.collect_usage_telemetry(
            compute=run_configuration.target, spark_context=self.automl_settings.spark_context,
            X=X, y=y, sample_weight=sample_weight, X_valid=X_valid, y_valid=y_valid,
            sample_weight_valid=sample_weight_valid, training_data=training_data,
            validation_data=validation_data, test_data=test_data
        )

        X, y, sample_weight, X_valid, y_valid, sample_weight_valid = dataset_utilities.convert_inputs(
            X, y, sample_weight, X_valid,
            y_valid, sample_weight_valid
        )

        training_data, validation_data, test_data = dataset_utilities.convert_inputs_dataset(
            training_data,
            validation_data,
            test_data
        )

        try:
            if self.automl_settings.spark_context:
                try:
                    from azureml.train.automl.runtime import _runtime_client
                    runtime_client = _runtime_client.RuntimeClient(self)
                    runtime_client._init_adb_driver_run(run_configuration=run_configuration,
                                                        X=X,
                                                        y=y,
                                                        sample_weight=sample_weight,
                                                        X_valid=X_valid,
                                                        y_valid=y_valid,
                                                        sample_weight_valid=sample_weight_valid,
                                                        cv_splits_indices=cv_splits_indices,
                                                        training_data=training_data,
                                                        validation_data=validation_data,
                                                        show_output=show_output)
                except Exception:
                    raise
            elif is_managed:
                self.current_run = local_managed(
                    self.experiment,
                    run_configuration,
                    self.automl_settings,
                    data_params,
                    show_output)
            elif run_configuration.target == 'local':
                name = run_configuration._name if run_configuration._name else "local"
                run_configuration.save(self.automl_settings.path, name)
                self._console_writer.println('Running on local machine')
                if not show_output:
                    logging.warning('Running on local machine. Note that local runs always run synchronously '
                                    'even if you use the parameter \'show_output=False\'')

                if not self.automl_settings._ignore_package_version_incompatibilities:
                    self._check_package_compatibilities(is_managed_run=_script_run is not None)
                try:
                    from azureml.train.automl.runtime import _runtime_client
                except ImportError as e:
                    raise ConfigException._with_error(
                        AzureMLError.create(
                            RuntimeModuleDependencyMissing, target="compute_target", module_name=e.name),
                        inner_exception=e
                    ) from e

                runtime_client = _runtime_client.RuntimeClient(self)

                runtime_client._fit_local(
                    X=X, y=y, sample_weight=sample_weight, X_valid=X_valid, y_valid=y_valid,
                    cv_splits_indices=cv_splits_indices,
                    existing_run=existing_run, sample_weight_valid=sample_weight_valid,
                    training_data=training_data, validation_data=validation_data, _script_run=_script_run,
                    parent_run_id=parent_run_id)
            else:
                self._console_writer.println('Running on remote compute: ' + str(run_configuration.target))
                self.automl_settings.debug_log = "azureml_automl.log"
                self._fit_remote(run_configuration, X=X, y=y, sample_weight=sample_weight,
                                 X_valid=X_valid, y_valid=y_valid, sample_weight_valid=sample_weight_valid,
                                 cv_splits_indices=cv_splits_indices, show_output=show_output,
                                 training_data=training_data, validation_data=validation_data,
                                 test_data=test_data)
        except Exception as e:
            self._fail_parent_run(error_details=e, is_aml_compute=run_configuration.target != 'local')
            raise
        assert self.current_run is not None
        return self.current_run

    def _fit_remote(self, run_configuration, X=None, y=None, sample_weight=None, X_valid=None, y_valid=None,
                    sample_weight_valid=None, cv_splits_indices=None, show_output=False,
                    training_data=None, validation_data=None, test_data=None):

        self._fit_remote_core(run_configuration, X=X, y=y, sample_weight=sample_weight, X_valid=X_valid,
                              y_valid=y_valid, sample_weight_valid=sample_weight_valid,
                              cv_splits_indices=cv_splits_indices, training_data=training_data,
                              validation_data=validation_data, test_data=test_data)

        if show_output:
            RemoteConsoleInterface._show_output(cast(AutoMLRun, self.current_run),
                                                self._console_writer,
                                                logger,
                                                self.automl_settings.primary_metric)

    def _take_snapshot(self):
        """
        Take a snapshot of the user's folder and upload it for remote run consumption. This is necessary if the user
        has any files that need to be included (e.g. the data script).
        """
        snapshot_id = None
        try:
            snapshot_id = cast(AutoMLRun, self.current_run).take_snapshot(self.automl_settings.path)
            logger.info("Snapshot_id: {0}".format(snapshot_id))
            return snapshot_id
        except SnapshotException as se:
            # Snapshot Size was either greater than 300MB or exceeded max files allowed
            if ((str(SNAPSHOT_MAX_SIZE_BYTES / ONE_MB) in se.message) or (str(SNAPSHOT_MAX_FILES) in se.message)):
                logging_utilities.log_traceback(se, logger)
                raise SnapshotException._with_error(
                    AzureMLError.create(
                        SnapshotLimitExceeded, target="automl_config.path",
                        size=str(SNAPSHOT_MAX_SIZE_BYTES / ONE_MB), files=str(SNAPSHOT_MAX_FILES)
                    )
                )
            else:
                raise
        except (AzureMLException, AzureMLServiceException):
            raise
        except Exception as e:
            logging_utilities.log_traceback(e, logger)
            return snapshot_id

    def _fit_remote_core(self, run_configuration, X=None, y=None, sample_weight=None,
                         X_valid=None, y_valid=None, sample_weight_valid=None, cv_splits_indices=None,
                         training_data=None, validation_data=None, test_data=None):
        """
        Create the parent run and submit the snapshot to JOS.

        :param run_configuration: Run configuration for this run, either user provided or system-generated.
        :param X: X input data. Not compatible with training_data.
        :param y: y input data. Not compatible with training_data.
        :param sample_weight: Sample weights for the data.
        :param X_valid: X validation data.
        :param y_valid: y validation data.
        :param sample_weight_valid: Sample weights for the validation data.
        :param cv_splits_indices: Indices of all the cross folds.
        :param training_data: Training data. Not compatible with X and y.
        :param validation_data: Validation data. Not compatible with X and y.
        :param test_data: Test data. Not compatible with X and y.
        :return:
        """
        run_config_object = run_configuration
        if isinstance(run_configuration, str):
            run_config_object = RunConfiguration.load(
                self.automl_settings.path, run_configuration)

        self._create_parent_run_for_remote(
            run_config_object, X=X, y=y, sample_weight=sample_weight, X_valid=X_valid, y_valid=y_valid,
            sample_weight_valid=sample_weight_valid, cv_splits_indices=cv_splits_indices,
            training_data=training_data, validation_data=validation_data, test_data=test_data)

        try:
            snapshot_id = None
            if self.user_script is not None:
                # A snapshot is only needed if the user is using a custom data script
                snapshot_id = self._take_snapshot()
                Contract.assert_non_empty(snapshot_id, "snapshot_id", reference_code="_fit_remote_core", log_safe=True)

            definition = {
                "Configuration": _serialize_to_dict(run_config_object)
            }

            definition["Configuration"]["environment"]["python"]["condaDependencies"] = \
                json.loads(json.dumps(run_config_object.environment.python.conda_dependencies._conda_dependencies))

            logger.info("Starting a snapshot run (snapshot_id : {0})".format(snapshot_id))
            self._jasmine_client.post_remote_jasmine_snapshot_run(
                self.parent_run_id, definition, snapshot_id)
        except (AzureMLException, AzureMLServiceException) as e:
            logging_utilities.log_traceback(e, logger)
            raise
        except Exception as e:
            logging_utilities.log_traceback(e, logger)
            raise ClientException.from_exception(e, target="AzureAutoMLClientfitremotecore").with_generic_msg(
                "Error occurred trying to run snapshot run.")

    def _create_parent_run_for_remote(self, run_config_object, X=None, y=None, sample_weight=None,
                                      X_valid=None, y_valid=None, sample_weight_valid=None, cv_splits_indices=None,
                                      training_data=None, validation_data=None, test_data=None):

        run_configuration = run_config_object.target
        run_config_object = modify_run_configuration(self.automl_settings, run_config_object, logger)

        # Uncomment to fall back to curated envs for changing environment behavior
        # run_config_object = modify_run_configuration_curated(self.automl_settings,
        #                                                      run_config_object,
        #                                                      self.experiment.workspace,
        #                                                      logger)

        parent_run_dto = self._create_and_validate_parent_run_dto(
            target=run_configuration,
            training_data=training_data,
            validation_data=validation_data,
            X=X,
            y=y,
            sample_weight=sample_weight,
            X_valid=X_valid,
            y_valid=y_valid,
            sample_weight_valid=sample_weight_valid,
            cv_splits_indices=cv_splits_indices,
            test_data=test_data
        )

        try:
            logger.info("Start creating parent run.")
            self.parent_run_id = self._jasmine_client.post_parent_run(
                parent_run_dto)
            # Populating the logging custom dimensions with the parent run id,
            # so that AppInsights querying gets easier.
            _logging.set_run_custom_dimensions(
                automl_settings=self.automl_settings,
                parent_run_id=self.parent_run_id,
                child_run_id=None)
        except (AzureMLException, AzureMLServiceException):
            raise
        except Exception as e:
            raise ClientException.from_exception(e, target="_create_parent_run_for_remote").with_generic_msg(
                "Error occurred when trying to create new parent run in AutoML service.")

        if self.user_script:
            logger.info(
                "[ParentRunID:{}] Remote run using user script.".format(self.parent_run_id))
        else:
            logger.info(
                "[ParentRunID:{}] Remote run using input X and y.".format(self.parent_run_id))

        if self.current_run is None:
            self.current_run = AutoMLRun(self.experiment, self.parent_run_id, host=self.automl_settings.service_url)

        # For back compatibility, check if the properties were added already as part of create parent run dto.
        # If not, add it here. Note that this should be removed once JOS changes are stably deployed
        if (self.DISPLAY_TASK_TYPE_PROPERTY not in self.current_run.properties or
                self.SDK_DEPENDENCIES_PROPERTY not in self.current_run.properties):
            properties_to_update = self._get_current_run_properties_to_update()
            self.current_run.add_properties(properties_to_update)

        self._console_writer.println("Parent Run ID: " + cast(str, self.parent_run_id))
        logger.info("Parent Run ID: " + cast(str, self.parent_run_id))

    def _create_and_validate_parent_run_dto(
        self,
        target,
        training_data,
        validation_data,
        X,
        y,
        sample_weight,
        X_valid,
        y_valid,
        sample_weight_valid,
        cv_splits_indices,
        parent_run_id=None,
        test_data=None
    ):
        """Create the parent DTO and validate it by invoking validation service in JOS."""
        if training_data is not None:
            if dataprep_utilities.is_dataflow(training_data):
                dataprep_json = dataprep_utilities.\
                    get_dataprep_json_dataset(training_data=training_data,
                                              validation_data=validation_data,
                                              test_data=test_data)
            else:
                dataprep_json = dataset_utilities.\
                    get_datasets_json(training_data=training_data,
                                      validation_data=validation_data,
                                      test_data=test_data)
        else:
            dataprep_json = dataprep_utilities.get_dataprep_json(X=X, y=y,
                                                                 sample_weight=sample_weight,
                                                                 X_valid=X_valid,
                                                                 y_valid=y_valid,
                                                                 sample_weight_valid=sample_weight_valid,
                                                                 cv_splits_indices=cv_splits_indices)
        if dataprep_json is not None:
            # escape quotations in json_str before sending to jasmine
            dataprep_json = dataprep_json.replace('\\', '\\\\').replace('"', '\\"')

        parent_run_dto = self._create_parent_run_dto(target, dataprep_json, parent_run_id)

        self._validate_input(parent_run_dto)

        return parent_run_dto

    def _create_parent_run_for_local_managed(
            self, data_params: Dict[str, Any], parent_run_id: Optional[Any] = None) -> AutoMLRun:
        """
        Create parent run in Run History containing AutoML experiment information for a local docker or conda run.
        Local managed runs will go through typical _create_parent_run_for_local workflow which will do the validation
        steps.

        :return: AutoML parent run
        :rtype: azureml.train.automl.AutoMLRun
        """
        parent_run_dto = self._create_and_validate_parent_run_dto(
            target=constants.ComputeTargets.LOCAL,
            parent_run_id=parent_run_id,
            **data_params
        )

        try:
            logger.info("Start creating parent run")
            self.parent_run_id = self._jasmine_client.post_parent_run(parent_run_dto)

            Contract.assert_value(self.parent_run_id, "parent_run_id")

            logger.info("Successfully created a parent run with ID: {}".format(self.parent_run_id))

            _logging.set_run_custom_dimensions(automl_settings=self.automl_settings,
                                               parent_run_id=self.parent_run_id,
                                               child_run_id=None)
        except (AutoMLException, AzureMLException, AzureMLServiceException):
            raise
        except Exception as e:
            logging_utilities.log_traceback(e, self.logger)
            raise ClientException.from_exception(e, target="_create_parent_run_for_local_managed").with_generic_msg(
                "Error when trying to create parent run in automl service.")

        logger.info("Setting Run {} status to: {}".format(str(self.parent_run_id), constants.RunState.PREPARE_RUN))
        self._jasmine_client.set_parent_run_status(
            self.parent_run_id, constants.RunState.PREPARE_RUN)

        self.current_run = AutoMLRun(self.experiment, self.parent_run_id)

        return self.current_run

    def _validate_input(self, parent_run_dto: CreateParentRun) -> None:
        logger.info("Start data validation.")
        validation_results = None
        with tracer.start_as_current_span(
                TelemetryConstants.SPAN_FORMATTING.format(
                    TelemetryConstants.COMPONENT_NAME, TelemetryConstants.DATA_VALIDATION
                ),
                user_facing_name=TelemetryConstants.DATA_VALIDATION_USER_FACING
        ):
            try:
                validation_results = self._jasmine_client.post_validate_service(parent_run_dto)
                # We get an empty response (HTTP 204) when the validation succeeds,
                # a HTTP 200 with an error response is raised otherwise
                if validation_results is None:
                    logger.info("Validation service found the data has no errors.")
            except Exception as e:
                logging_utilities.log_traceback(e, logger)
                # Any other validation related exception won't fail the experiment.
                logger.warning("Validation service meet exceptions, continue training now.")

        if validation_results is not None and len(validation_results.error.details) > 0 \
                and any([d.code != "UpstreamSystem" for d in validation_results.error.details]):
            # If validation service meets error thrown by the upstream service, the run will continue.
            self._console_writer.println("The validation results are as follows:")
            errors = []
            for result in validation_results.error.details:
                if result.code != "UpstreamSystem":
                    self._console_writer.println(result.message)
                    errors.append(result.message)
            msg = "Validation error(s): {}".format(validation_results.error.details)
            raise ValidationException._with_error(AzureMLError.create(
                ExecutionFailure, operation_name="data/settings validation", error_details=msg)
            )

    def _create_parent_run_dto(self,
                               target: Optional[Union[RunConfiguration, str]],
                               dataprep_json: Optional[str] = None,
                               parent_run_id: Optional[Any] = None) -> CreateParentRun:
        """
        Create CreateParentRun.

        :param target: run configuration
        :type target: RunConfiguration or str
        :param dataprep_json: dataprep json string
        :type dataprep_json: str
        :param parent_run_id: Parent run id.
        :return: CreateParentRun to be sent to Jasmine
        :rtype: CreateParentRun
        """

        # Remove path when creating the DTO
        settings_dict = self.automl_settings.as_serializable_dict()
        settings_dict['path'] = None

        parent_run_dto = CreateParentRun(target=target,
                                         run_type="automl",
                                         num_iterations=self.automl_settings.iterations,
                                         training_type=None,  # use self.training_type when jasmine supports it
                                         acquisition_function=None,
                                         metrics=['accuracy'],
                                         primary_metric=self.automl_settings.primary_metric,
                                         train_split=self.automl_settings.validation_size,
                                         acquisition_parameter=0.0,
                                         num_cross_validation=self.automl_settings.n_cross_validations,
                                         aml_settings_json_string=json.dumps(settings_dict),
                                         data_prep_json_string=dataprep_json,
                                         enable_subsampling=self.automl_settings.enable_subsampling,
                                         properties=self._get_current_run_properties_to_update(),
                                         scenario=self.automl_settings.scenario,
                                         environment_label=self.automl_settings.environment_label,
                                         parent_run_id=parent_run_id)
        return parent_run_dto

    def _get_task(self, previous_fit_outputs, is_sparse=None, start_child_run=False):
        """
        Query Jasmine for the next task.

        :param previous_fit_outputs: Outputs of the previous tasks that executed
        :type previous_fit_outputs: List[FitOutput]
        :param is_sparse: Whether the data is sparse
        :type is_sparse: bool
        :param start_child_run: whether to start child runs
        :type start_child_run: bool
        :return: dto containing task details
        """
        return self._get_tasks(previous_fit_outputs, 1, is_sparse, start_child_run)[0]

    def _get_tasks(self, previous_fit_outputs, max_batch_size, is_sparse, start_child_runs=False):
        """
        Query Jasmine for the next batch of tasks.

        :param previous_fit_outputs: Outputs of the previous tasks that executed
        :type previous_fit_outputs: List[FitOutput]
        :param max_batch_size: Max number of next tasks to retrieve
        :type max_batch_size: int
        :param is_sparse: Whether the data is sparse
        :type is_sparse: bool
        :param start_child_runs: whether to start child runs
        :type start_child_runs: bool
        :return: Next batch of tasks to run
        """
        with logging_utilities.log_activity(logger=logger, activity_name=TelemetryConstants.GET_PIPELINE_NAME):
            try:
                logger.info("Querying Jasmine for a max of next {} tasks.".format(max_batch_size))
                parent_run_dto = None  # type: Optional[RunDto]
                previous_pipeline_results = None  # type: Optional[MiroProxyInput]
                if previous_fit_outputs is not None:
                    # TODO: VSO-562043 - Add training_percents as well
                    previous_pipeline_results = MiroProxyInput(
                        pipeline_ids=[p.pipeline_id for p in previous_fit_outputs],
                        scores=[p.score for p in previous_fit_outputs],
                        run_algorithms=[p.run_algorithm for p in previous_fit_outputs],
                        run_preprocessors=[p.run_preprocessor for p in previous_fit_outputs],
                        iteration_numbers=list(range(len(previous_fit_outputs))),
                        predicted_times=[p.predicted_time for p in previous_fit_outputs],
                        actual_times=[p.actual_time for p in previous_fit_outputs],
                        training_percents=[p.training_percent for p in previous_fit_outputs],
                        is_sparse_data=is_sparse)
                if isinstance(self.current_run, Run):
                    parent_run_dto = self.current_run._client.run_dto
                if max_batch_size == 1:
                    local_run_get_next_task_input = LocalRunGetNextTaskInput(
                        input_df=previous_pipeline_results, parent_run_dto=parent_run_dto)
                    return [self._jasmine_client.get_next_task(self.parent_run_id,
                                                               local_run_get_next_task_input,
                                                               start_child_runs)]
                local_run_get_next_task_batch_input = LocalRunGetNextTaskBatchInput(
                    input_df=previous_pipeline_results, parent_run_dto=parent_run_dto,
                    max_batch_size=max_batch_size)
                return self._jasmine_client.get_next_task_batch(
                    self.parent_run_id,
                    local_run_get_next_task_batch_input,
                    start_child_runs).iteration_tasks
            except (AzureMLException, AzureMLServiceException):
                raise
            except ClientRequestError as ce:
                logger.error("Failed to fetch the next pipeline recommendation due to local connection problems.")
                logging_utilities.log_traceback(ce, logger)
                raise
            except Exception as e:
                logging_utilities.log_traceback(e, logger)
                raise FetchNextIterationException.from_exception(
                    e, target="AzureAutoMLClientGetNextTask").with_generic_msg(
                        "Error occurred when trying to fetch next iteration from AutoML service.")

    def _check_create_folders(self, path):
        if path is None:
            path = os.getcwd()
        # Expand out the path because os.makedirs can't handle '..' properly
        aml_config_path = os.path.abspath(os.path.join(path, '.azureml'))
        os.makedirs(aml_config_path, exist_ok=True)

    def _get_display_task(self) -> str:
        """Get display task property."""
        # This property is to temporarily fix: 362194.
        # It should be removed promptly.
        task = self.automl_settings.task_type
        if self.automl_settings.is_timeseries:
            task = constants.Tasks.FORECASTING
        return task

    def _get_current_run_properties_to_update(self):
        """Get properties to update on the current run object."""
        # TODO: Remove with task 416022
        display_task_type_property = {self.DISPLAY_TASK_TYPE_PROPERTY: self._get_display_task()}

        # Log the AzureML packages currently installed on the local machine to the given run.
        user_sdk_dependencies_property = \
            {self.SDK_DEPENDENCIES_PROPERTY: json.dumps(package_utilities.get_sdk_dependencies())}

        # Make sure to batch all relevant properties in this single call in-order to avoid multiple network trips to RH
        result = {**display_task_type_property, **user_sdk_dependencies_property}
        return result

    def _fail_parent_run(self, error_details: BaseException, is_aml_compute: bool) -> None:
        """
        Mark the parent run as 'Failed'. Additionally, a notification is sent to JOS (which may log run terminal
        details in the service side telemetry)

        This is a No-Op if there is no parent run created yet.
        """
        logging_utilities.log_traceback(error_details, logger)

        if self.current_run is None:
            logger.info("No parent run to fail")
            return

        logger.error("Run {} failed with exception of type: {}".format(str(self.parent_run_id), type(error_details)))

        try:
            # If the run is already in a terminal state, don't update the status again
            current_run_status = self.current_run.get_status()
            if current_run_status in [RunStatus.COMPLETED, RunStatus.FAILED, RunStatus.CANCELED]:
                logger.warning('Cannot fail the current run since it is already in a terminal state of [{}].'.
                               format(current_run_status))
                return
            if self.current_run is not None:
                run_lifecycle_utilities.fail_run(self.current_run, error_details, is_aml_compute=is_aml_compute)
            if self._jasmine_client is not None and self.parent_run_id is not None:
                logger.info("Setting Run {} status to: {}".format(str(self.parent_run_id),
                                                                  constants.RunState.FAIL_RUN))
                self._jasmine_client.set_parent_run_status(self.parent_run_id, constants.RunState.FAIL_RUN)
        except (AzureMLException, AzureMLServiceException, ClientRequestError) as e:
            logger.error("Encountered an error while failing the parent run. Exception type: {}".
                         format(e.__class__.__name__))
            logging_utilities.log_traceback(error_details, logger)
            raise
        except Exception as e:
            logger.error("Encountered an error while failing the parent run. Exception type: {}".
                         format(e.__class__.__name__))
            raise ClientException.from_exception(e, has_pii=True).with_generic_msg(
                "Error occurred when trying to set parent run status.")

    def _check_package_compatibilities(self, is_managed_run: bool = False) -> None:
        """
        Check package compatibilities and raise exceptions otherwise.

        :param is_managed_run: Whether the current run is a managed run.
        :raises: `azureml.automl.core.shared.exceptions.RequiredDependencyMissingOrIncompatibleException`
        in case of un-managed runs.
        :raises: `azureml.automl.core.shared.exceptions.ClientException` in case of managed runs.
        """
        try:
            is_databricks_run = self.automl_settings.azure_service == _InternalComputeTypes.DATABRICKS
            package_utilities._get_package_incompatibilities(
                packages=package_utilities.AUTOML_PACKAGES,
                ignored_dependencies=package_utilities._PACKAGES_TO_IGNORE_VERSIONS,
                is_databricks_run=is_databricks_run
            )
        except ValidationException as ex:
            if is_managed_run:
                raise ClientException._with_error(
                    AzureMLError.create(
                        AutoMLInternal,
                        target=ex._target,
                        error_details="Package mismatch in local environment.",
                        reference_code=ReferenceCodes._MANAGED_ENVIRONMENT_CORRUPTED
                    ),
                    inner_exception=ex
                )
            raise

    @staticmethod
    def _set_environment_variables_for_reconstructing_run(run):
        os.environ[RunHistoryEnvironmentVariableNames.AZUREML_ARM_SUBSCRIPTION] = \
            run.experiment.workspace.subscription_id
        os.environ[RunHistoryEnvironmentVariableNames.AZUREML_RUN_ID] = run.id
        os.environ[RunHistoryEnvironmentVariableNames.AZUREML_ARM_RESOURCEGROUP] = \
            run.experiment.workspace.resource_group
        os.environ[RunHistoryEnvironmentVariableNames.AZUREML_ARM_WORKSPACE_NAME] = run.experiment.workspace.name
        os.environ[RunHistoryEnvironmentVariableNames.AZUREML_ARM_PROJECT_NAME] = run.experiment.name
        os.environ[RunHistoryEnvironmentVariableNames.AZUREML_EXPERIMENT_ID] = run.experiment.id
        os.environ[RunHistoryEnvironmentVariableNames.AZUREML_RUN_TOKEN] = run._client.run.get_token().token
        os.environ[RunHistoryEnvironmentVariableNames.AZUREML_SERVICE_ENDPOINT] = run._client.run.get_cluster_url()
        os.environ[RunHistoryEnvironmentVariableNames.AZUREML_DISCOVERY_SERVICE_ENDPOINT] = \
            run.experiment.workspace.discovery_url

    @staticmethod
    def _is_tensorflow_module_present():
        try:
            from azureml.automl.runtime.shared import pipeline_spec
            return pipeline_spec.tf_wrappers.tf_found
        except Exception:
            return False

    @staticmethod
    def _is_xgboost_module_present():
        try:
            from azureml.automl.runtime.shared import model_wrappers
            return model_wrappers.xgboost_present
        except Exception:
            return False

    @staticmethod
    def _is_fbprophet_module_present():
        fbprophet = import_utilities.import_fbprophet(raise_on_fail=False)
        return fbprophet is not None
