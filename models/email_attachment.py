"""Data model representing email attachment metadata and content."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class EmailAttachment:
    original_filename: str
    safe_filename: str
    content_type: str
    payload: bytes
    cid: Optional[str] = None
    content_disp: Optional[str] = None

    def to_meta_dict(self) -> dict:
        return {
            'original_filename': self.original_filename,
            'safe_filename': self.safe_filename,
            'content_type': self.content_type,
            'size_bytes': len(self.payload),
            'content_id': self.cid,
            'content_disposition': self.content_disp,
        }
