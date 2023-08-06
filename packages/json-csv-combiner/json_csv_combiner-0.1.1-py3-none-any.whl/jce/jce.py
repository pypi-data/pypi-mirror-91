import pandas as pd
import glob
from tqdm import tqdm
import json

# All the functions go here

def get_json_file_count():
    """
    Get the total numebr of JSON file present in the current directory
    """

    number_of_json_file = 0
    for i in glob.glob("*.json"):
        number_of_json_file = number_of_json_file + 1

    return number_of_json_file


def get_csv_file_count():
    """
    Get the total number of CSV file present in the current directory
    """

    number_of_csv_file = 0
    for i in glob.glob("*.csv"):
        number_of_csv_file = number_of_csv_file + 1

    return number_of_csv_file


def get_excel_file_count():
    """
    Get the total number of CSV file present in the current directory
    """

    number_of_excel_file = 0
    for i in glob.glob("*.xlsx"):
        number_of_excel_file = number_of_excel_file + 1

    return number_of_excel_file


def combine_excel(output_excel_name):
    """
    Combine all the excel file by reading

    Args:
        output_file_name (string): name of the output file
    """

    combined_excel_data = pd.DataFrame()
    for f in tqdm(glob.glob("*.xlsx")):
        df = pd.read_excel(f)
        all_data = all_data.append(df, ignore_index=True)

    combined_excel_data.to_excel(output_excel_name, index=False)


def combine_csv(output_csv_name):
    """
    Combine all the excel file by reading

    Args:
        output_file_name (string): name of the output file
    """

    combined_csv_data = pd.DataFrame()
    for f in tqdm(glob.glob("*.csv")):
        df = pd.read_csv(f)
        all_data = all_data.append(df, ignore_index=True)

    combined_csv_data.to_csv(output_csv_name, index=False)


def combine_json(output_json_name):

    """
    Combine all the json file by reading

    Args:
        output_file_name (string): name of the output file
    """

    combined_json_data = []
    for f in glob.glob("*.json"):
        with open(f, "rb") as input_file:
            combined_json_data.append(json.load(input_file))

    with open(output_json_name, "wb") as output_file:
        json.dump(combined_json_data, output_file)
