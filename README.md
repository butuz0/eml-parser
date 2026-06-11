# CLI .eml Parser

A command-line utility to parse `.eml` files. It extracts email metadata into a structured `JSON` file,
saves the plain text and `HTML` bodies, and dumps all file attachments into the specified directory.

## Features

- **Metadata Extraction**: Parses core email headers (From, To, Subject, Thread-Topic, Date, CC, Delivered-To) and
  saves
  them in `meta.json`.

- **Body Separation**: Extracts and decodes `text/plain` and `text/html` parts into dedicated `body.txt` and `body.html`
  files.

- **OS-Safe Attachment Downloader**: Saves all email attachments using a strict filename sanitization pipeline.

- **Bulk Processing (`Bash`)**: Recursively scans directories for `.eml` files, and packs results into a `.tgz` archive.

Why Bash? That's one of life's greatest mysteries.

## Requirements

- Python 3.10 or higher (dataclass `slots` support)
- Bash 3.2 or higher

## Usage

### 1. Parsing a Single `.eml` File

Run the script from your terminal by providing the path to the `.eml` file and the directory where the extracted
contents will be saved:

```bash
python main.py emails/invoice.eml output/parsed_invoice
```

Once executed, the tool organizes the parsed email components within the output directory as follows:

```text
output/parsed_invoice/
├── meta.json             # Extracted headers and attachment mapping
├── body.txt              # Text body
├── body.html             # HTML body with localized attachment paths
└── [attachment_files]    # Sanitized attachment files (e.g., report.pdf, logo_1.png)
```

### 2. Bulk Processing a Directory (Bash)

Make the script executable:

```bash
chmod +x parse_bulk.sh
```

Run the bulk script from your terminal by providing the path to the directory where the `.eml` files are located:

```bash
./parse_bulk.sh /path/to/emails_directory
```

Once executed, the bulk script creates an isolated, timestamped archive alongside your target folder:

```text
/path/to/
├── emails_directory/                     # Your source folder (untouched)
└── emails_directory_20260611_181722.tgz  # The resulting parsed data archive
```

Inside the archive, every email gets its own dedicated subfolder containing its `meta.json`, `body.txt`, `body.html`,
and attachments.

## Making the scripts globally accessible

To run this parser from any directory in your OS without typing the full path to `main.py`, you can set up a command
alias.

### macOS/Linux

1. Open your shell configuration file in a text editor:

    ```bash
    nano ~/.zshrc
    ```

   _(Use `~/.bashrc` if you are using Bash instead of Zsh)_

2. Add the following line at the bottom of the file, replacing the path with the actual absolute paths:

    ```bash
    # Shortcut for single file parser
    alias eml-parser="python3 /absolute/path/to/your/project/main.py"

    # Shortcut for the bulk parser
    alias eml-bulk-parser="bash /absolute/path/to/your/project/parse_bulk.sh"
    ```

3. Save the file, exit the editor, and reload the configuration:

    ```bash
    source ~/.zshrc
    ```

### You can now use the tool anywhere:

Parse one file inside Downloads:

```bash
cd ~/Downloads
eml-parser ./incoming_emails/sample.eml ./extracted_data
```

Parse a folder inside Downloads:

```bash
cd ~/Downloads
eml-bulk-parser ./incoming_emails
```
