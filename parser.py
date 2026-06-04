import email
from email import policy
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Tuple, Optional

from models import EmailData, EmailAttachment


def parse_eml(file_path: str | Path) -> EmailData:
    path = Path(file_path).resolve()
    if not path.is_file():
        raise ValueError(f'.eml file not found: {file_path!r}')
    if path.suffix != '.eml':
        raise ValueError(f'.eml file expected, got: {file_path!r}')
 
    with open(path, 'rb') as file:
        msg = email.message_from_binary_file(file, policy=policy.default)

    text_body, html_body = _extract_bodies(msg)
    attachments = _extract_attachments(msg)

    return EmailData(
        email_from=msg.get('From'),
        date=parsedate_to_datetime(msg.get('Date')),
        email_to=msg.get('To'),
        delivered_to=msg.get('Delivered-To'),
        cc=msg.get('Cc'),
        subject=msg.get('Subject'),
        thread_topic=msg.get('Thread-Topic'),
        text_body=text_body,
        html_body=html_body,
        attachments=attachments,
    )


def _extract_bodies(msg: email.message.Message) -> Tuple[Optional[str], Optional[str]]:
    text_body = None
    html_body = None

    for part in msg.walk():
        if part.is_multipart() or part.get_filename():
            continue

        content_type = part.get_content_type()
        content_charset = part.get_content_charset('utf-8')

        if content_type == 'text/plain':
            text_body = part.get_payload(decode=True).decode(content_charset, errors='replace')
        elif content_type == 'text/html':
            html_body = part.get_payload(decode=True).decode(content_charset, errors='replace')

    return text_body, html_body


def _extract_attachments(msg: email.message.Message) -> list[EmailAttachment]:
    attachments = []

    for part in msg.walk():
        if part.is_multipart() or (filename := part.get_filename()) is None:
            continue

        attachments.append(
            EmailAttachment(
                filename=filename,
                content_type=part.get_content_type(),
                payload=part.get_payload(decode=True),
            )
        )

    return attachments
