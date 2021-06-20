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
        "private_key_id": "a9f6d1c43277bf6fa570961c9a4d7578e70a71fa",
        # get_value_from_dotenv('private_key').replace('\\n', '\n'),
        "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCdoMlV/p+KF4vH\\nWlYr6AKYbKPpsZ2yZGlLG2M8Kn711qxHGH48u0hHyVT+gw/XL83iKWRHrgmQ5Dj3\\nX01VyPNhpiIjll2YDolCAkpvo5cAy+ITGr8HFaTCEpmE8XZgzBryLDPj6AkMLTyx\\na/myvw13YM7yOXboBlQCM5RaCoUqjuIQn0+jatQn45WWKkb4hU226GbJd53/738a\\nKhu+FygWWybKq+14NWZxFP2s876f7VOEcuRuO/fuLoGi0EAhpfaLxBgF4HyV9wR7\\nLwSgZ1rYpoc4l1pwYvVBgwVKpiZZdQ/OeRwlS63h1DuLS/ytALOqfllf9FnljhKc\\nW+/ZNOTLAgMBAAECggEARPfsAA9nuOEyjKhPGejq8cxfL8pCSKK8m1tBYTrq0B/8\\nwyLJYUNEjfxejvnDfZDyEWmw8dgJYXcqIbp2OPmy29/4AgAxtW1uyw37ibtXP8b1\\nhQxn1u62ZyACQfPwqsvDYoDKt4Z4JvbIHo0y9O25M6mNAtj32O+j5E6zM25087he\\npDQ3/wquewKGfH12QSo8/H+66lE9xl4ZWPhQaunFKRWyLo3iS/3YltxQdXWI6/b4\\nHjMgdOqy/hD8hcYR1KTg43LlIY/WfZuDzuGS4kbuqUMNr+XtmOOevSWL43WK0IHy\\n94sdcB4NXQCxeJb4ub5WJfwHyxWxWERFqW6qex+OiQKBgQDXZEIOx+DgenP2XWX3\\n5VtVhlpU+uPT3leMcYxxIfzezoRTA2Y9DUoQUMjpfu8bRnbFELH+JBTFB83U6znE\\nHTGFfc/qqSs2yOwYL5eXpQujCptD0/8F/Bn8QIGn4JWdjigLfd0aTThO5Km65wyY\\nfUxHiIImobDd/sThsofqblIg1QKBgQC7WJs+vUk2gOw6v/6E9Nvwyn8qZvPr6rm0\\nsPmk+XLJBwjkHR6q8jUZrgPuhmbbRtK7y0u1pH/Z4Ce/Ln+o9jDqyfHsGNcpWDcu\\nuzFHHLasXegP4YOT4LfbdJ2duFRPfwHi9PLYtBM3CYoKtsJ0hsaFCbonTk6DxGHY\\napauHbS/HwKBgHXW/Sj3A7nsZKsh2Bqy2bBFy//4L1MHruBAczSmAqGnXM/J6VJ3\\nhdC9Ud4lOw2yFGKmSqse9FoDdgIKG1WHH0PIXEsm+GSFsl1dFFO70U0HDYEjZ7/P\\neCwA4q6E+XX0g0YeOywbmTXYdl+x7rsyudvc/E/EYG5j5zUPprqEVtxtAoGBALWs\\nsjeAFXxOP0aloqrKTHLP28uBtO7FW7rWl/CcmexJ7xxPBMtfP5Ech+GJ4jqoDnlg\\nJpYJ5JWi4shpzhBKVZuJpBmA6T3FtxWRH7NHK/owwnaMCS2hEIo3JxWoh9HjZy/w\\nu4Lb9Xo8vOmw2xdnDyI6EZRGQqtTCFN24ZINapafAoGAFAhtw46tsu7CPiLI3Dan\\nj+U1jCmx9fIZCDbH69FWJEsKW2gcDcw+uVhEmQurxNB8bjgb219c5RocAHnUdKh1\\nwzzOurXYx41ajle4j1QkL0Tg303QgKlXdORhnvHSZZixOjDCpxYAYPtJvFGAOz9W\\npy+Qkjsk8LfMSyi6r6LGAkQ=\\n-----END PRIVATE KEY-----\\n".replace('\\n', '\n'),
        # get_value_from_dotenv('private_key_id'),
        # replacement due to the way python gets
        # strings from environment
        "client_email": "pybothelp@pybot-to-track-studying.iam.gserviceaccount.com",
        "client_id": '101688956838801253271',  # get_value_from_dotenv('client_id'),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/pybothelp%40pybot-to-track-studying.iam.gserviceaccount.com"
    }
    return creds
