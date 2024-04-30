import tabula
import pandas as pd

def lookup_value(data_dict, lookup_value):
    if lookup_value in data_dict:
        return data_dict[lookup_value]

    return None

pdf_path = "/Users/vadim.peretokin/Downloads/KBV_ITA_VGEX_Datensatzbeschreibung_KVDT en.pdf"
kvdt_file_path = "/Users/vadim.peretokin/Desktop/Z05123456699_27.01.2024_12.00.con.annotated.2"

def read_kvdt_dataset(file_path):
   # Read the PDF file and extract the tables
    tables = tabula.read_pdf(file_path, pages='all')
    data_dict = {}

    # Process the extracted tables
    for table in tables:
        if 'FK' in table.columns and 'Field name' in table.columns:
            # Convert the table to a dictionary for efficient lookuptable_dict = table.set_index('FK').to_dict()['Field name']
            table_dict = table.set_index('FK').to_dict()['Field name']
            data_dict.update(table_dict)

    # remove any values don't have a table identifier
    data_dict = {k: v for k, v in data_dict.items() if not pd.isna(k)}

    # round the values up to remove trailing .0
    data_dict = {round(float(k)): v for k, v in data_dict.items()}

    # convert to strings and pad with a zero to ensure a 4 digit identifier
    updated_table_dict = {}
    for key, value in data_dict.items():
        key_str = str(key)
        if len(key_str) == 3 and key_str != 'nan':
            key_str = '0' + key_str
        updated_table_dict[key_str] = value

    return updated_table_dict

kvdt_description = read_kvdt_dataset(pdf_path)

with open(kvdt_file_path, 'r', encoding='ISO-8859-1') as kvdt_file, open('output.txt', 'w', encoding='ISO-8859-1') as output_file:
    for line in kvdt_file:
        length = line[1:3]
        identifier = line[3:7]
        value = line[7:]
        result = lookup_value(kvdt_description, identifier)

        # replace any newlines with spaces
        result = result.replace('\n', ' ')
        result = result.replace('\r', ' ')

        if result:
            updated_line = "{:<19} = {} length, {}: {}\n".format(line.strip(), length, result, value.strip())
        else:
            updated_line = line.strip() + ',No match found\n'

        output_file.write(updated_line)  # Write the updated row to the output file

print("Processing completed. Output saved to output.txt.")
