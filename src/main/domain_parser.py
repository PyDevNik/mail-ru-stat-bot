import requests
from datetime import datetime, timedelta
import pandas as pd

from data_saver import list_to_dataframe, write_to_excel


def get_token(refresh_token: str):
    request_data = requests.post(
        f'https://o2.mail.ru/token',
        params={
            'client_id': 'postmaster_api_client',
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token})

    if request_data.ok:
        access_token = request_data.json()['access_token']
        return access_token


def get_stats(domain: str, access_token: str) -> list:
    date_from = (datetime.now() - timedelta(days=30)).date()

    request = requests.get('https://postmaster.mail.ru/ext-api/stat-list-detailed',
                           params={'domain': domain, 'date_from': date_from},
                           headers={'Bearer': access_token})
    stats_data = {}
    if request.ok:
        stats_dict = request.json()["data"]
        if stats_dict:
            stats_data = stats_dict[0].get('data')
    return stats_data


def create_stats(refresh_token, domain):
    access_token = get_token(refresh_token)
    data_dict = get_stats(domain, access_token)
    if data_dict: 
        dataframe_rows = [
        'Дата',
        'Письма',
        'Доставлено',
        'Жалоб',
        'Репутация, %',
        'Тенденция, %',
        'Прочит.',
        'Удал. прочит.',
        'Удал. непрочит.',
        'Доставлено, %'
        ]

        excel_data = list_to_dataframe(dataframe_rows)

        for day in data_dict:
            # check that sent is not zero
            # to not get the division by zero
            if day['delivered'] != 0:
                delivered = 100 * round(day['messages_sent'] / day['delivered'])
            else:
                delivered = 100

            data_list = [day['date'],
                     day['messages_sent'],
                     day['delivered'],
                     day['complaints'],
                     round(day['reputation'], 2),
                     round(day['trend'], 2),
                     day['read'],
                     day['deleted_read'],
                     day['deleted_unread'],
                     delivered]

            dataframe = list_to_dataframe(data_list)
            excel_data = pd.concat([excel_data, dataframe], axis=1, ignore_index=True)
        return [excel_data, data_dict]
    else: 
        return [None, data_dict]


def create_stats_table(refresh_token, domain):
    NoneType = type(None)
    excel_data = create_stats(refresh_token, domain)
    if not isinstance(excel_data[0], NoneType):
        write_to_excel(excel_data[0], 'result.xlsx')
        return [excel_data, excel_data[1]]
    else:
        return [None, excel_data[1]]