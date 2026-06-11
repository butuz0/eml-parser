"""Module for saving email data to disk."""

import json
from pathlib import Path

from constants import (
    BODY_TXT_FILENAME,
    BODY_HTML_FILENAME,
    METADATA_FILENAME,
)
from models import EmailData


def save_email_to_disk(email_data: EmailData, output_dir: str) -> None:
    """
    Save email text and HTML bodies, metadata, and
    attachments to the designated output directory.
    """

    path = Path(output_dir).resolve()
    if path.is_file():
        raise ValueError(f'Directory expected, got file: {output_dir!r}')
    path.mkdir(parents=True, exist_ok=True)

    if email_data.text_body:
        (path / BODY_TXT_FILENAME).write_text(email_data.text_body, encoding='utf-8')

    if email_data.html_body:
        (path / BODY_HTML_FILENAME).write_text(email_data.html_body, encoding='utf-8')

    for att in email_data.attachments:
        (path / att.filename).write_bytes(att.payload)

    with open(path / METADATA_FILENAME, 'w') as file:
        json.dump(email_data.to_dict(), file, indent=4)
