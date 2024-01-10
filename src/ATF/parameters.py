"""Module for parsing input parameters"""

class Parameters:
    """Parse input parameters"""
    args = {}
    path_connection = None
    path_cases = None
    path_output = None
    export = None
    failure_on_error = None
    variables = {}

    def __init__(self, argv:list):
        self.set_args(argv[1:])
        self.set_variables()
        self.path_connection = self.get_value("connections", "connections.yaml")
        self.path_cases = self.get_value("cases", "./cases")
        self.path_output = self.get_value("output", "./output")
        self.export = self.get_value("export", "JSON").upper()
        self.failure_on_error = self.get_value("failure", True)

    def set_args(self, args):
        """Set dictionary of args with cleaned name"""
        for i, name in enumerate(args):
            if not name.startswith("-"):
                continue

            value = False
            if i != len(args) - 1:
                value = args[i + 1]
                if value.startswith("-"):
                    value = True
                else:
                    value = value.replace("'", "").replace("\"", "")

            name = name.replace("-", "")
            self.args[name] = value

    def get_value(self, long_name:str, default):
        """Get value or default value from args"""
        if long_name in self.args:
            value = self.args[long_name]
            if str(value).upper() == "TRUE": return True
            if str(value).upper() == "FALSE": return False
            return value

        return default

    def set_variables(self):
        """Set variable liste from args"""
        for name, value in self.args.items():
            if not name.startswith("p_"):
                continue
            name = name.replace("p_", "")
            self.variables[name] = value
