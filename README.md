# KVDT Dataset Decoder

This Python script processes a [KVDT](https://de.wikipedia.org/wiki/KVDT) (Kassenärztliche Vereinigung DatenTransfer) dataset by extracting information from a KVDT specification PDF and a KVDT .con file. It generates an output file with the processed data, including field lengths, identifiers, and corresponding values.

## Requirements

- Python 3.x
- PyPDF2
- tabula-py
- pandas
- argparse

You can install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

To run the script, use the following command:

```
python reader.py --kvdt_specification <path_to_specification_pdf> --kvdt_file_path <path_to_kvdt_con_file> --output_path <path_to_output_file>
```

Replace the following placeholders with the appropriate paths:
- `<path_to_specification_pdf>`: Path to the KVDT specification PDF file (available [here](https://update.kbv.de/ita-update/Abrechnung/KBV_ITA_VGEX_Datensatzbeschreibung_KVDT.pdf)).
- `<path_to_kvdt_con_file>`: Path to the KVDT .con file.
- `<path_to_output_file>`: Path to the output file where the processed data will be saved.


## Example

Suppose you have the following files:
- KVDT specification PDF: `kvdt_spec.pdf`
- KVDT .con file: `data.con`
- Desired output file: `output.txt`

You can run the script using the command:

```bash
python reader.py --kvdt_specification kvdt_spec.pdf --kvdt_file_path data.con --output_path output.txt
```

After running the script, the processed data will be saved in `output.txt`.

## License

This project is licensed under the [MIT License](LICENSE).
