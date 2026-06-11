"""Utility functions for string normalization and text processing."""

import re
from pathlib import Path

from models import EmailAttachment


def sanitize_filename(original_name: str) -> str:
    """Transforms original filename into an OS-safe alternative."""

    clean_name = Path(original_name).name
    if not clean_name:
        clean_name = 'attachment'

    stem = Path(clean_name).stem
    suffix = Path(clean_name).suffix

    safe_stem = re.sub(r'[\\/*?:"<>|% \t\x00-\x1F\x7F]', '_', stem)[:100]

    return f'{safe_stem}{suffix}'


def replace_inline_attachments_src(
        html_content: str,
        attachments: list[EmailAttachment],
) -> str:
    """
    Resolves inline CID attachment references
    in HTML to match local filenames.
    """

    cid_to_filename = {
        att.cid: att.safe_filename
        for att in attachments
        if att.content_disp == 'inline'
    }

    if not cid_to_filename:
        return html_content

    def replace_match(match: re.Match[str]) -> str:
        quote_char = match.group(1)
        cid_value = match.group(2)

        if cid_value in cid_to_filename:
            return f'src={quote_char}{cid_to_filename[cid_value]}{quote_char}'

        return match.group(0)

    pattern = r'src=(["\'])cid:([^"\']+)\1'
    return re.sub(pattern, replace_match, html_content)
