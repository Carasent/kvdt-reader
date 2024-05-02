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

As an example, input format that looks like this:

```
0138000con0
017910320240130
01091064
01091321
01091323
0138000besa
0180201010100300
0430203H+H Topp-Gl�cklich, KBV-Testpraxis
```

Will be transformed into something more readable:

```
# first 3 characters are the field length, next 4 are the field identifier (FK) and the value follows afterwards

0138000con0         = 13 length, Record type: con0
017910320240130     = 17 length, Creation date: 20240130
01091064            = 10 length, Character set used: 4
01091321            = 10 length, Data packets contained in this file: 1
01091323            = 10 length, Data packets contained in this file: 3
0138000besa         = 13 length, Record type: besa
0180201010100300    = 18 length, Establishment number (BSNR) or secondary establishment number (NBSNR): 010100300
```

## License

This project is licensed under the [MIT License](LICENSE).
