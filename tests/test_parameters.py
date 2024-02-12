from ploosh.parameters import Parameters

def test_parameters_default():
    parameters = Parameters([])

    assert parameters.export == "JSON"
    assert parameters.path_cases == "./cases"
    assert parameters.path_cases_filter == "*.yml"
    assert parameters.path_connection == "connections.yaml"
    assert parameters.path_output == "./output"
    assert parameters.failure_on_error is True


def test_parameters_args():
    parameters = Parameters([""
        , "--export", "CSV"
        , "--cases", "./tests"
        , "--filter", "*"
        , "--connections", "dev.yml"
        , "--output", "./results"
        , "--failure", "False"
    ])

    assert parameters.export == "CSV"
    assert parameters.path_cases == "./tests"
    assert parameters.path_cases_filter == "*"
    assert parameters.path_connection == "dev.yml"
    assert parameters.path_output == "./results"
    assert parameters.failure_on_error is False

def test_parameters_variables():
    parameters = Parameters([""
        , "--p_password_database", "azerty123"
        , "--p_password_snowflake", "qwerty456"
    ])

    assert parameters.variables["password_database"] == "azerty123"
    assert parameters.variables["password_snowflake"] == "qwerty456"