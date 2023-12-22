
import pandas as pd
from core.miscellaneous import get_parameter_value

def get_connection_configuration():
    return [
        {
            "name": "path"
        }
    ]

def get_data(test_case_definition):
    path = get_parameter_value(test_case_definition, "path", "03x003")
    df = pd.read_csv(path)
    return df
