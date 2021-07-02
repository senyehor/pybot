from datetime import datetime, timedelta, date
from collections import namedtuple
from dotenv import load_dotenv
from config import DEBUG
import os
import httplib2
import googleapiclient.discovery as discovery
from oauth2client.service_account import ServiceAccountCredentials
from abc import ABC, abstractmethod

if DEBUG:
    load_dotenv('.env')


class Activity:
    pass


class CustomGoogleFunctions(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def __get_hhtp_auth(apis_path: list[str] = None, credentials: dict[str, str] = None):
        """Before calling this func make sure you set up environmental variables"""
        if not apis_path:
            apis_paths = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive',
            ]
        if not credentials:
            credentials = {
                "type": "service_account",
                "project_id": "pybot-to-track-studying",
                "private_key_id": os.getenv('private_key_id'),
                "private_key": os.getenv('private_key').replace('\\n', '\n'),
                # replacement due to way python reads env vars
                "client_email": "pog-198@pybot-to-track-studying.iam.gserviceaccount.com",
                "client_id": os.getenv('client_id'),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/pog-198%40pybot-to-track-studying.iam.gserviceaccount.com"
            }
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials, apis_paths)  # noqa
        http_auth = credentials.authorize(httplib2.Http())
        return http_auth

    @classmethod
    def _get_service(cls, service_name: str, service_version: str):
        service = discovery.build(service_name, service_version, http=cls.__get_hhtp_auth())
        return service


class Spreadsheet(CustomGoogleFunctions):

    def __init__(self, spreadsheet_id: str):  # noqa
        self.__spreadsheet_id = spreadsheet_id
        self.__sheets_service = self._get_service('sheets', 'v4').spreadsheets()

    def add_sheet(self, sheet_name: str, row_count: int = 10, column_count: int = 33) -> dict:
        response = self.__sheets_service.batchUpdate(spreadsheetId=self.__spreadsheet_id,
                                                     body={'requests': [{
                                                         'addSheet': {
                                                             'properties': {
                                                                 'title': sheet_name,
                                                                 'gridProperties': {
                                                                     'rowCount': row_count,
                                                                     'columnCount': column_count
                                                                 }
                                                             }
                                                         }
                                                     }
                                                     ]}).execute()
        return response

    # todo delete sheet
    def update(self, cells_range: str, values, value_input_option: str = 'USER_ENTERED') -> str:
        """Returns updated cells range, second value input option is 'RAW'"""
        if not isinstance(values, list):
            values = [values]
        response = self.__sheets_service.values().update(spreadsheetId=self.__spreadsheet_id,
                                                         range=cells_range,
                                                         valueInputOption=value_input_option,
                                                         body={
                                                             'values': [
                                                                 values
                                                             ]
                                                         }).execute()
        return response.get('updatedRange')

    def get(self, cells_range: str = '', major_dimension: str = 'COLUMNS'):
        """Values are [[values from range1], [values from range2], ...]"""
        if major_dimension not in ('COLUMNS', 'ROWS'):
            raise AttributeError('major_dimension must be "COLUMNS" or "ROWS"')
        response: dict = self.__sheets_service.values().get(
            spreadsheetId=self.__spreadsheet_id,
            range=cells_range,
            majorDimension=major_dimension
        ).execute()
        values = response.get('values', None)
        return values

    def get_activity(self, user_sheet_name: str, activity_name: str):
        return Activity(self, user_sheet_name, activity_name)

    def clear(self, cells_range: str):
        self.__sheets_service.values().clear(
            spreadsheetId=self.__spreadsheet_id,
            range=cells_range,
            body={}
        )

    def get_sheets_list(self) -> list[str]:
        response = self.__sheets_service.get(spreadsheetId=self.__spreadsheet_id).execute()
        sheets_list = []
        sheets = response.get('sheets')
        for sheet in sheets:
            sheets_list.append(sheet['properties']['title'])
        return sheets_list


def _str_to_datetime(time: str):
    converter = lambda x: map(int, x.split('-'))
    year, month, day = converter(time)
    date = datetime(year, month, day)
    return date


class Timings(namedtuple('Timings', ['days_planned', 'intervals_list'])):
    __slots__ = ()
    # variables to comfortably convert from string to Timings
    __timings_planned_days, __intervals_list = range(2)

    @classmethod
    def to_timings_converter(cls, timings: str):
        split = timings.split('|')
        days_planned = int(split[cls.__timings_planned_days])
        intervals_list = split[cls.__intervals_list].split(';')
        return cls(days_planned, intervals_list)

    def __str__(self):
        return str(self.days_planned) + '|' + ';'.join(self.intervals_list)


class Statistic(namedtuple('Statistic', [
    'done_days_of_planned',
    'percentage_of_planned_productivity',
    'activity_start_date',
    'this_week_start_date'
]
                           )):
    __slots__ = ()
    # variables to comfortably convert from string to Statistic
    __done_days_of_planned, __percentage_of_planned_productivity, \
    __activity_start_date, __this_week_beginning_date = range(4)  # noqa

    @classmethod
    def to_statistic_converter(cls, statistic: str):
        split = statistic.split(';')
        done_days_of_planned = split[cls.__done_days_of_planned]
        percentage_of_planned_productivity = split[cls.__percentage_of_planned_productivity]
        activity_start_date = _str_to_datetime(split[cls.__activity_start_date]).date()
        this_week_start_date = _str_to_datetime(split[cls.__this_week_beginning_date]).date()
        return cls(done_days_of_planned, percentage_of_planned_productivity, activity_start_date,
                   this_week_start_date)

    def __str__(self):
        return self.done_days_of_planned + ';' \
               + self.percentage_of_planned_productivity + ';' \
               + str(self.activity_start_date) + ';' \
               + str(self.this_week_start_date)

    def update_percentage_of_planned_productivity_and_add_day(self, done_percent: float):
        new_statistic = self.update_percentage_of_planned_productivity(done_percent)
        new_statistic = Statistic.add_day(new_statistic)
        return new_statistic

    def update_percentage_of_planned_productivity(self, done_percent: float):
        new_productivity = str((float(self.percentage_of_planned_productivity) + done_percent) / 2)
        return Statistic(self.done_days_of_planned, new_productivity, self.activity_start_date,
                         self.this_week_start_date)

    def add_day(self):
        split = self.done_days_of_planned.split('/')
        new_done_days_of_planned = str(int(split[0]) + 1) + '/' + split[1]
        return Statistic(new_done_days_of_planned, self.percentage_of_planned_productivity, self.activity_start_date,
                         self.this_week_start_date)

    def get_done_days_and_planned_days(self) -> (int, int):
        split = self.done_days_of_planned.split('/')
        return int(split[0]), int(split[1])

    def update_week_start_and_set_done_days_to_zero(self):
        _, planned_days = self.get_done_days_and_planned_days()
        new_done_days_of_planned = f'0/{planned_days}'
        new_week_start = self.this_week_start_date + timedelta(weeks=1)
        return Statistic(new_done_days_of_planned, self.percentage_of_planned_productivity, self.activity_start_date,
                         new_week_start)


class DoneActivityRecord(namedtuple('DoneActivityRecord', ['done_percent_of_planned_time', 'date'])):
    __slots__ = ()
    # variables to comfortably convert from str to DoneActivityRecord
    __done_percent_of_planned_time, __date = range(2)

    @classmethod
    def to_done_activity_record_converter(cls, activity_record: str):
        split = activity_record.split(';')
        done_percent_of_planned_time = split[cls.__done_percent_of_planned_time]
        date = _str_to_datetime(split[cls.__date]).date()
        return cls(done_percent_of_planned_time, date)

    def __str__(self):
        return self.done_percent_of_planned_time + ';' + self.date

    @classmethod
    def get_today_record(cls, done_percent_of_planned_time: float):
        return cls(str(done_percent_of_planned_time), str(datetime.utcnow().date()))


class Activity:

    def __init__(self, spreadsheet: Spreadsheet, user_sheet_name: str, activity_name: str, timings: Timings = None,
                 statistic: Statistic = None, existing_activity: bool = False):
        self.__spreadsheet = spreadsheet
        self.__user_sheet_name = user_sheet_name
        self.__activity_name = activity_name
        self.__line_number = self.__get_activity_line_number()
        self.__timings_cell = f'{self.user_sheet_name}!B{self.__line_number}'
        self.__statistic_cell = f'{self.user_sheet_name}!C{self.__line_number}'
        self.__records_cells = f'{user_sheet_name}!D{self.__line_number}:AG{self.__line_number}'
        if existing_activity:
            sheets_list = spreadsheet.get_sheets_list()
            if user_sheet_name not in sheets_list:
                raise AttributeError(f'There is no list with name "{user_sheet_name}"')
            self.__timings = self.__get_timings()
            self.__statistic = self.__get_statistic()
        else:
            self.__timings = timings
            self.__statistic = statistic

    @property
    def activity_name(self):
        return self.__activity_name

    @property
    def user_sheet_name(self):
        return self.__user_sheet_name

    @property
    def timings(self):
        return self.__timings

    @property
    def statistic(self):
        return self.__statistic

    def _get_activities_column_values(self):
        cells_for_activities_names = f'{self.user_sheet_name}!A1:A10'
        values = self.__spreadsheet.get(cells_for_activities_names, 'COLUMNS')
        if not values:
            return None
        # returns values [0] because values are [[values]]
        return values[0]

    def __get_activity_line_number(self):
        column_values = self._get_activities_column_values()
        activity_line_number = column_values.index(self.__activity_name) + 1
        return activity_line_number

    def _get_first_empty_row_number(self):
        column_values = self._get_activities_column_values()
        if column_values:
            if '' in column_values:
                return column_values.index('') + 1
            return len(column_values) + 1
        return 1

    def __get_interval_between_week_start_and_last_time_done_activity_in_days(self,
                                                                              last_record: DoneActivityRecord) -> int:
        activity_statistic = Statistic.to_statistic_converter(self.__spreadsheet.get(self.__statistic_cell)[0][0])
        week_beginning_date = activity_statistic.this_week_start_date
        return (_str_to_datetime(last_record.date).date() - week_beginning_date).days

    def __update_statistic_cell(self, statistic_cell: Statistic):
        self.__spreadsheet.update(self.__statistic_cell, str(statistic_cell))

    def __update_activity_statistic(self, last_record: DoneActivityRecord):
        days_delta = self.__get_interval_between_week_start_and_last_time_done_activity_in_days(last_record)
        statistic_cell = Statistic.to_statistic_converter(self.__spreadsheet.get(self.__statistic_cell)[0][0])
        if days_delta < 8:
            statistic_cell = statistic_cell.update_percentage_of_planned_productivity_and_add_day(
                float(last_record.done_percent_of_planned_time))
        else:
            done_days, planned_days = statistic_cell.get_done_days_and_planned_days()
            if done_days != planned_days:
                days_user_should_exercise_but_didnt = done_days - planned_days
                for _ in range(days_user_should_exercise_but_didnt):
                    statistic_cell = statistic_cell.update_percentage_of_planned_productivity(0)
                statistic_cell = statistic_cell.update_week_start_and_set_done_days_to_zero()
        self.__update_statistic_cell(statistic_cell)

    def __clear_activity_cells(self):
        self.__spreadsheet.clear(self.__records_cells)

    def __get_first_free_cell_of_activity_row(self):
        values = self.__spreadsheet.get(self.__records_cells, major_dimension='ROWS')
        if not values:
            free_cell_number = 1
        else:
            free_cell_number = len(values) + 1
        if free_cell_number < 24:
            return chr(free_cell_number + 67) + str(self.__line_number)
        return 'A' + chr(free_cell_number + 41) + str(self.__line_number)

    def __get_timings(self):
        if hasattr(self, '__timings'):
            return self.__timings
        timings = self.__spreadsheet.get(self.__timings_cell)
        if not timings:
            raise Exception(f'At {self.user_sheet_name} "{self.__activity_name}" activity timings cell is empty :(')
        return Timings.to_timings_converter(timings[0][0])

    def __get_statistic(self):
        if hasattr(self, '__statistic'):
            return self.__statistic
        statistic = self.__spreadsheet.get(self.__statistic_cell)
        if not statistic:
            raise Exception(f'At {self.user_sheet_name} "{self.__activity_name}" activity statistic cell is empty :(')
        return Statistic.to_statistic_converter(statistic[0][0])

    def _add_activity_record(self, record: DoneActivityRecord):
        first_free_cell = f'{self.user_sheet_name}!' + self.__get_first_free_cell_of_activity_row()
        if first_free_cell.startswith('AH'):
            self.__clear_activity_cells()
            first_free_cell = self.__get_first_free_cell_of_activity_row()
        self.__spreadsheet.update(first_free_cell, str(record))
        self.__update_activity_statistic(record)

    def _delete(self):
        self.__spreadsheet.clear(f'{self.user_sheet_name}!A{self.__line_number}:AG{self.__line_number}')


class ActivitiesManager:
    def __init__(self, spreadsheet: Spreadsheet, user_sheet_name: str):
        """If activity name is not specified creates manager to create, delete and edit activities"""
        if user_sheet_name not in spreadsheet.get_sheets_list():
            spreadsheet.add_sheet(user_sheet_name)
        self.__spreadsheet = spreadsheet
        self.__user_sheet_name = user_sheet_name

    def add_activity(self, activity: Activity):
        free_line_number = activity._get_first_empty_row_number()
        name_timing_statistic_cells = f'{activity.user_sheet_name}!A{free_line_number}:C{free_line_number}'
        self.__spreadsheet.update(name_timing_statistic_cells,
                                  [activity.activity_name, str(activity.timings), str(activity.statistic)])

    def get_activity(self, activity_name: str):
        return Activity(self.__spreadsheet, self.__user_sheet_name, activity_name, existing_activity=True)

    @staticmethod
    def add_record(activity: Activity, record: DoneActivityRecord):
        activity._add_activity_record(record)

    @staticmethod
    def delete_activity(activity: Activity):
        activity._delete()

    @staticmethod
    def get_current_statistic(activity: Activity):
        today = datetime.utcnow().date()
        days_practiced = (today - activity.statistic.activity_start_date).days
        percentage_of_planned_productivity = float(activity.statistic.percentage_of_planned_productivity) * 100
        return f'Your current productivity is {percentage_of_planned_productivity:g}% and ' \
               f'you have been practising for ' \
               f'{days_practiced} days'


spreadsheet = Spreadsheet(os.getenv('workbook_id'))
pog = ActivitiesManager(spreadsheet, 'test_sheet')
print(pog.get_current_statistic(pog.get_activity('python')))
