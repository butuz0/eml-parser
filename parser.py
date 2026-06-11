"""
Parsing logic for extracting metadata, content
bodies, and attachments from EML files.
"""

import email
from email import policy
from pathlib import Path
from typing import Tuple, Optional

from models import EmailData, EmailAttachment
from utils import sanitize_filename, replace_inline_attachments_src


def parse_eml(file_path: str | Path) -> EmailData:
    """Parse an EML file into a structured EmailData object."""

    path = Path(file_path).resolve()
    if not path.is_file():
        raise ValueError(f'.eml file not found: {file_path!r}')
    if path.suffix != '.eml':
        raise ValueError(f'.eml file expected, got: {file_path!r}')

    with open(path, 'rb') as file:
        msg = email.message_from_binary_file(file, policy=policy.default)

    text_body, html_body = _extract_bodies(msg)
    attachments = _extract_attachments(msg)

    if html_body:
        html_body = replace_inline_attachments_src(html_body, attachments)

    date = msg.get('Date')

    return EmailData(
        email_from=msg.get('From'),
        date=date.datetime if date else None,
        email_to=msg.get('To'),
        delivered_to=msg.get('Delivered-To'),
        cc=msg.get('Cc'),
        subject=msg.get('Subject'),
        thread_topic=msg.get('Thread-Topic'),
        text_body=text_body,
        html_body=html_body,
        attachments=attachments,
    )


def _extract_bodies(msg: email.message.EmailMessage) -> Tuple[Optional[str], Optional[str]]:
    """Extract plain text and HTML bodies from the MIME message."""

    text_body = None
    html_body = None

    for part in msg.walk():
        if part.is_multipart() or part.get_filename():
            continue

        content_type = part.get_content_type()

        if content_type == 'text/plain':
            text_body = part.get_content()
        elif content_type == 'text/html':
            html_body = part.get_content()

    return text_body, html_body


def _extract_attachments(msg: email.message.EmailMessage) -> list[EmailAttachment]:
    """
    Extract and decode attachments content and metadata
    from a MIME message, assigning safe filenames.
    """

    attachments = []

    for part in msg.walk():
        if part.is_multipart() or (original_filename := part.get_filename()) is None:
            continue

        safe_filename = sanitize_filename(original_filename)
        cid = part.get('Content-ID')

        attachments.append(
            EmailAttachment(
                original_filename=original_filename,
                safe_filename=safe_filename,
                content_type=part.get_content_type(),
                payload=part.get_payload(decode=True),
                cid=cid.strip('<>') if cid else None,
                content_disp=part.get_content_disposition(),
            )
        )

    return attachments
