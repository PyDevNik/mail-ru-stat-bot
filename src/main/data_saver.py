import pandas as pd


def list_to_dataframe(data_list: list):
    dataframe = pd.DataFrame(data_list)
    return dataframe


def write_to_excel(data: pd.DataFrame, filename: str):
    data.to_excel(filename)
