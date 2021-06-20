from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import httplib2
import googleapiclient.discovery as discovery
from oauth2client.service_account import ServiceAccountCredentials
from bot import run_bot

APIS_PATHS = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]
# TODO: add creds
# credentials = ServiceAccountCredentials.from_json_keyfile_dict(get_credentials_dict(), APIS_PATHS)
# http_auth = credentials.authorize(httplib2.Http())
# service = discovery.build('sheets', 'v4', http=http_auth)


def main():
    run_bot()


if __name__ == '__main__':
    main()
