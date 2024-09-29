"""Module to manage the configuration of the framework"""
import copy
import pathlib
import yaml
from pyjeb import control_and_setup
from pyjeb.exception import InvalidParameterException
from case import Case, ConnectionDescription
from parameters import Parameters


class Configuration:
    """Manage configuration"""
    parameters = None
    connectors = None
    exporter = None
    connections = {}

    # Definition of the structure of a test case
    case_definition = [
        {"name": "disabled", "type": "boolean", "default": False},
        {"name": "options", "type": "dict", "default": {}},
        {"name": "options.ignore", "type": "list", "default": None},
        {"name": "options.sort", "type": "list", "default": None},
        {"name": "options.cast", "type": "list", "default": []},
        {"name": "options.cast.name", "type": "string"},
        {
            "name": "options.cast.type",
            "type": "string",
            "validset": ["float", "int", "datetime", "string"],
        },
        {"name": "options.pass_rate", "type": "decimal", "default": 1},
        {"name": "options.allow_no_rows", "type": "boolean", "default": True},
        {"name": "options.trim", "type": "boolean", "default": False},
        {"name": "source", "type": "dict"},
        {"name": "source.type"},
        {"name": "source.connection", "default": None},
        {"name": "expected", "type": "dict"},
        {"name": "expected.connection", "default": None},
        {"name": "expected.connection", "default": None},
    ]

    def __init__(self, parameters: Parameters, connectors: dict, exporters: dict):
        """Initialize Configuration with parameters, connectors, and exporters"""
        self.parameters = parameters
        self.connectors = connectors

        # Initialize connections and set the exporter
        self.init_connections()
        self.set_exporter(exporters)

    def get_module_type(self, obj: dict):
        """Get type of module from user configuration"""
        if "type" not in obj.keys():
            raise InvalidParameterException("Property 'type' is not defined")

        module_type = str(obj["type"]).upper()
        if module_type not in self.connectors.keys():
            raise InvalidParameterException(
                f"Property 'type' ({module_type}) is not a valid connector"
            )

        return module_type

    def get_connection(self, name):
        """Get connection of module from user configuration"""
        if name is None:
            return None

        if name not in self.connections.keys():
            raise InvalidParameterException(f"Connection {name} do not exists")

        return self.connections[name]

    def init_connections(self):
        """Load connections and apply control and variable setup"""
        if self.parameters.path_connection is None:
            self.connections = {}
        else:
            # Load connections from the specified path
            with open(self.parameters.path_connection, encoding="UTF-8") as file:
                content = file.read()
                self.connections = yaml.safe_load(content)

        # Copy connections and initialize each one
        connections = copy.copy(self.connections)
        for connection_name in connections:
            connection = connections[connection_name]
            module_type = self.get_module_type(connection)

            connection_definition = self.connectors[module_type].connection_definition

            # Apply control and setup to the connection
            self.connections[module_type] = control_and_setup(
                connection, connection_definition, self.parameters.variables, None
            )

    def get_cases(self):
        """Get cases from user configuration and apply control and variable setup"""
        cases = {}
        # Get list of case files based on the specified filter
        files_list = list(
            pathlib.Path(self.parameters.path_cases).rglob(
                self.parameters.path_cases_filter
            )
        )

        for file_path in files_list:
            with open(file_path, encoding="UTF-8") as file:
                configurations = yaml.load(file, Loader=yaml.loader.SafeLoader)
                for case_name in configurations.keys():
                    configuration = configurations[case_name]

                    # Apply control and setup to the case configuration
                    case = control_and_setup(
                        configuration,
                        self.case_definition,
                        self.parameters.variables,
                        None,
                    )

                    # Get and setup source configuration
                    source_module_type = self.get_module_type(configuration["source"])
                    source_connector = self.connectors[source_module_type]
                    source_configuration_definition = (
                        source_connector.configuration_definition
                    )

                    case["source"] = control_and_setup(
                        case["source"],
                        source_configuration_definition,
                        self.parameters.variables,
                        None,
                    )
                    source_definition = ConnectionDescription(
                        source_connector, self.get_connection(case["source"]["connection"])
                    )

                    # Get and setup expected configuration
                    expected_module_type = self.get_module_type(configuration["expected"])
                    expected_connector = self.connectors[expected_module_type]
                    expected_configuration_definition = (
                        expected_connector.configuration_definition
                    )

                    case["expected"] = control_and_setup(
                        case["expected"],
                        expected_configuration_definition,
                        self.parameters.variables,
                        None,
                    )
                    expected_definition = ConnectionDescription(
                        expected_connector,
                        self.get_connection(case["expected"]["connection"]),
                    )

                    # Ensure both source and expected connectors are either Spark or non-Spark
                    if source_connector.is_spark != expected_connector.is_spark:
                        raise InvalidParameterException(
                            f"'{case_name}': Source and expected must be both Spark or not Spark connectors"
                        )

                    # Add the case to the cases dictionary
                    cases[case_name] = Case(
                        configuration,
                        source_definition,
                        expected_definition,
                        case["options"],
                        case["disabled"],
                    )

        return cases

    def set_exporter(self, exporters):
        """Set exporter from args"""
        if self.parameters.export not in exporters.keys():
            raise InvalidParameterException(
                f"Parameter 'export' ({self.parameters.export}) is not a valid exporter"
            )

        # Set the exporter and its output path
        self.exporter = exporters[self.parameters.export]
        self.exporter.output_path = self.parameters.path_output
