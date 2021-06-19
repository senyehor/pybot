import json
import os
from dotenv import load_dotenv
from pprint import pprint


def get_value_from_dotenv(key: str) -> str:
    value = os.getenv(key)
    if value:
        return value
    raise Exception(f'{key} is not configured in .env file')


def get_credentials_dict() -> dict:
    load_dotenv('.env')
    # create dictionary that represents credentials.json
    creds = {
        "type": "service_account",
        "project_id": "pybot-to-track-studying",
        "private_key_id": get_value_from_dotenv('private_key_id'),
        "private_key": get_value_from_dotenv('private_key').replace('\\n', '\n'),
        # replacement due to the way python gets
        # strings from environment
        "client_email": "pybothelp@pybot-to-track-studying.iam.gserviceaccount.com",
        "client_id": get_value_from_dotenv('client_id'),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/pybothelp%40pybot-to-track-studying.iam.gserviceaccount.com"
    }
    return creds
