from jce import *
import argparse

parser = argparse.ArgumentParser(description='Combine multiple JSON/CSV/Excel file into a signle file')
parser.add_argument('-t', '--type', type=str, metavar='', required=True, help='Type of the file to convert [json/csv/excel]')
parser.add_argument('-o', '--output', type=str, metavar='', required=True, help='Output file name')
args = parser.parse_args()

def main(file_type, output_name):

    """
    Conversion
    """
    if file_type.lower() == 'json':
        count = get_json_file_count()
        print(count)
        combine_csv(output_name)
    elif file_type.lower() == 'csv':
        count = get_csv_file_count()
        print(count)
        combine_csv(output_name)
    elif file_type.lower() == "excel":
        count = get_excel_file_count()
        print(count)
        combine_excel(output_name)
    else:
        print("Unsupported file type")


if __name__ == "__main__":
    type_of_file = args.type
    output_name = args.output
    main(type_of_file, output_name)