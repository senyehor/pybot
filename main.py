from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import httplib2
import googleapiclient.discovery as discovery
from oauth2client.service_account import ServiceAccountCredentials

APIS_PATHS = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]
creds = {
    "type": "service_account",
    "project_id": "pybot-to-track-studying",
    "private_key_id": os.getenv('private_key_id'),
    "private_key": os.getenv('private_key'),
    "client_email": "pog-198@pybot-to-track-studying.iam.gserviceaccount.com",
    "client_id": os.getenv('client_id'),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/pog-198%40pybot-to-track-studying.iam.gserviceaccount.com"
}

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, APIS_PATHS)

httpAuth = credentials.authorize(httplib2.Http())
service = discovery.build('sheets', 'v4', http=httpAuth)

spreadsheet = service.spreadsheets().create(body={
    'properties': {'title': 'Первый тестовый документ', 'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Лист номер один',
                               'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
}).execute()
spreadsheetId = spreadsheet['spreadsheetId']
print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)
