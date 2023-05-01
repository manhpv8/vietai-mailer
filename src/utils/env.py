import dotenv
import os
import pprint
from typing import Dict, Any


def load_and_set_env_vars(env: str) -> Dict[str, Any]:
    """
    Utility function to use in Databricks notebooks to load .env files and set them via os
    Return a dict of set environment variables
    Parameters
    ----------
    env : str
        Name of deployment environment. One of
    Returns
    -------
    Dictionary of set environment variables
    """
    env_vars_path = os.path.join(os.getcwd(), 'conf', env, f'.env')
    pprint.pprint(f"Load & set env from env_vars_path = '{env_vars_path}'")
    dotenv.load_dotenv(env_vars_path)

    base_data_vars_vars_path = os.path.join(os.getcwd(), 'conf', '.base_data_params.env')
    pprint.pprint(f"Load & set env from base_data_vars_vars_path = '{base_data_vars_vars_path}'")
    dotenv.load_dotenv(base_data_vars_vars_path)

    os_dict = dict(os.environ)
    pprint.pprint(os_dict)

    return os_dict
