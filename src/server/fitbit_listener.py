import fitbit
import os
import json
from settings import Settings
from src.db import DB
import datetime
import logging
import gather_keys_oauth2 as Oauth2
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

#
# CLIENT_ID = '23QXH9'
# CLIENT_SECRET = '679db39e6fc859f28225f4815cb71348'
#
#
# server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
# server.browser_authorize()
# ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
# REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
# auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)


class FitbitTracker:

    def __init__(self):
        if os.path.exists(os.path.join(Settings.proj_root,'fitbit_token.json')):


            with open(os.path.join(Settings.proj_root,'fitbit_token.json')) as f:

                connection_data = json.load(f)
                logging.log(logging.ERROR, "Fitbit token expired. Refreshing token")
                server = Oauth2.OAuth2Server(connection_data['clientid'], connection_data['client_secret'])
                server.browser_authorize()
                ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
                REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
                self.auth2_client = fitbit.Fitbit(connection_data['clientid'], connection_data['client_secret'], oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)
                f.close()
                with open(os.path.join(Settings.proj_root,'fitbit_token.json'), 'w') as f:
                    json.dump({'clientid': connection_data['clientid'], 'client_secret': connection_data['client_secret'], 'access_token': ACCESS_TOKEN, 'refresh_token': REFRESH_TOKEN}, f)
                    f.close()

        else:
            raise Exception("Fitbit service not initialized")

    def get_steps(self, date: datetime.date) -> dict:
        """
        date is at date interval. eg datetime.date.today()
        :param date:
        :return:
        """
        data = self.auth2_client.intraday_time_series('activities/steps', base_date=date, detail_level=Settings.fitbit_interval)
        return_dict = {
            'steps': data['activities-steps'][0]['value'],
            'date': data['activities-steps'][0]['dateTime'],
            'interval': Settings.fitbit_interval,
            'dataset': data['activities-steps-intraday']['dataset']
        }
        return return_dict

    def get_sleep(self, date: datetime.date) -> list:
        """
        date is at date interval. eg datetime.date.today()
        :param date:
        :return:
        """
        data = self.auth2_client.get_sleep(date)
        return_list = []
        for sleep_data in data['sleep']:
            return_list.append(sleep_data)
        return return_list

    def get_heart_rate(self, date: datetime.date) -> dict:
        """
        date is at date interval. eg datetime.date.today()
        :param date:
        :return:
        """
        data = self.auth2_client.intraday_time_series('activities/heart', base_date=date, detail_level=Settings.fitbit_interval)
        return_dict = {
            'heartzones': data['activities-heart'][0]['value']['heartRateZones'],
            'date': data['activities-heart'][0]['dateTime'],
            'interval': Settings.fitbit_interval,
            'dataset': data['activities-heart-intraday']['dataset']
        }
        return return_dict

    def get_calories(self, date: datetime.date) -> dict:
        """
        date is at date interval. eg datetime.date.today()
        :param date:
        :return:
        """
        data = self.auth2_client.intraday_time_series('activities/calories', base_date=date, detail_level=Settings.fitbit_interval)
        return_dict = {
            'calories': data['activities-calories'][0]['value'],
            'date': data['activities-calories'][0]['dateTime'],
            'interval': Settings.fitbit_interval,
            'dataset': data['activities-calories-intraday']['dataset']
        }
        return return_dict

def runner():
    fb = FitbitTracker()
    db = DB()
    step_data = fb.get_steps(datetime.date.today()-datetime.timedelta(days = 1))
    sleep_data = fb.get_sleep(datetime.date.today()-datetime.timedelta(days = 1))
    heart_data = fb.get_heart_rate(datetime.date.today()-datetime.timedelta(days = 1))
    calorie_data = fb.get_calories(datetime.date.today()-datetime.timedelta(days = 1))
    db.insert('stepdata', step_data)
    for itm in sleep_data:
        db.insert('sleepdata', itm)
    db.insert('heartdata', heart_data)
    db.insert('caloriesdata', calorie_data)
    db.close()

if __name__ == "__main__":

    runner()

