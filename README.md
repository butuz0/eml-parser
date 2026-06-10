# CLI .eml Parser

A command-line utility to parse `.eml` files. It extracts email metadata into a structured `JSON` file,
saves the plain text and `HTML` bodies, and dumps all file attachments into the specified directory.

## Features

- **Metadata Extraction**: Parses core email headers (From, To, Subject, Thread-Topic, Date, CC, Delivered-To) and saves
  them in `meta.json`.

- **Body Separation**: Extracts and decodes `text/plain` and `text/html` parts into dedicated `body.txt` and `body.html`
  files.

- **Attachment Downloader**: Saves all email attachments them using their original filenames.

## Requirements

- Python 3.10 or higher (dataclass `slots` support)

## Usage

Run the script from your terminal by providing the path to the `.eml` file and the directory where the extracted
contents will be saved

```bash
python main.py emails/invoice.eml output/parsed_invoice
```

This parses `invoice.eml` file, creates the `output/parsed_invoice` directory, and places all the extracted data
inside it.

## Making the script globally accessible

To run this parser from any directory in your OS without typing the full path to `main.py`, you can set up a command
alias.

### macOS/Linux

1. Open your shell configuration file in a text editor:

    ```bash
    nano ~/.zshrc
    ```

   Use `~/.bashrc` if you are using Bash instead of Zsh

2. Add the following line at the bottom of the file, replacing the path with the actual absolute path to the `main.py`
   file:

    ```bash
    alias eml-parser="python3 /absolute/path/to/your/project/main.py"
    ```

3. Save the file, exit the editor, and reload the configuration:

    ```bash
    source ~/.zshrc
    ```

### You can now use the tool anywhere:

```bash
cd ~/Downloads
eml-parser sample.eml ./extracted_data
```
