import json
from pathlib import Path

from models import EmailData


def save_email_to_disk(email_data: EmailData, output_dir: str) -> None:
    path = Path(output_dir).resolve()
    if path.is_file():
        raise ValueError(f'Directory expected, got file: {output_dir!r}')
    path.mkdir(parents=True, exist_ok=True)

    if email_data.text_body:
        (path / 'body.txt').write_text(email_data.text_body, encoding='utf-8')

    if email_data.html_body:
        (path / 'body.html').write_text(email_data.html_body, encoding='utf-8')

    for att in email_data.attachments:
        (path / att.filename).write_bytes(att.payload)

    with open(path / 'meta.json', 'w') as file:
        json.dump(email_data.to_dict(), file, indent=4)
