import tabula
import argparse
import pandas as pd


parser = argparse.ArgumentParser(description="Process KVDT dataset.")
parser.add_argument("--kvdt_specification", help="Path to the KVDT specification PDF")
parser.add_argument("--kvdt_file_path", help="Path to the KVDT .con file")
parser.add_argument("--output_path", help="Path to the output file")

args = parser.parse_args()

kvdt_specification = args.kvdt_specification
kvdt_file_path = args.kvdt_file_path
output_path = args.output_path


"""
Reads and processes a KVDT (Kassenärztliche Vereinigung-Datentransfer) dataset from a PDF file.

The function takes a file path to a PDF file containing KVDT data, reads the tables from the PDF, and returns a dictionary mapping the field identifiers (FK) to their corresponding field names.

Args:
    file_path (str): The file path to the PDF file containing the KVDT data.

Returns:
    dict: A dictionary mapping the field identifiers (FK) to their corresponding field names.
"""
def read_kvdt_dataset(file_path):
    # Read the PDF file and extract the tables
    tables = tabula.read_pdf(file_path, pages="all")
    data_dict = {}

    # Process the extracted tables
    for table in tables:
        if "FK" in table.columns and "Field name" in table.columns:
            # Convert the table to a dictionary for efficient lookuptable_dict = table.set_index('FK').to_dict()['Field name']
            table_dict = table.set_index("FK").to_dict()["Field name"]
            data_dict.update(table_dict)

    # remove any values don't have a table identifier
    data_dict = {k: v for k, v in data_dict.items() if not pd.isna(k)}

    # round the values up to remove trailing .0
    data_dict = {round(float(k)): v for k, v in data_dict.items()}

    # convert to strings and pad with a zero to ensure a 4 digit identifier
    updated_table_dict = {}
    for key, value in data_dict.items():
        key_str = str(key)
        if len(key_str) == 3 and key_str != "nan":
            key_str = "0" + key_str
        updated_table_dict[key_str] = value

    return updated_table_dict


def lookup_value(data_dict, value):
    if value in data_dict:
        return data_dict[value]

    return None

kvdt_description = read_kvdt_dataset(kvdt_specification)

with open(kvdt_file_path, "r", encoding="ISO-8859-1") as kvdt_file, open(
    output_path, "w", encoding="ISO-8859-1"
) as output_file:
    output_file.write(
        "# first 3 characters are the field length, next 4 are the field identifier (FK) and the value follows afterwards\n\n"
    )

    for line in kvdt_file:
        length = line[1:3]
        identifier = line[3:7]
        value = line[7:]
        result = lookup_value(kvdt_description, identifier)

        # replace any newlines with spaces
        result = result.replace("\n", " ")
        result = result.replace("\r", " ")

        if result:
            updated_line = "{:<19} = {} length, {}: {}\n".format(
                line.strip(), length, result, value.strip()
            )
        else:
            updated_line = line.strip() + ",No match found\n"

        output_file.write(updated_line)  # Write the updated row to the output file

print(f"Processing completed. Output saved to {kvdt_file_path}")
