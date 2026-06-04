from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EmailAttachment:
    filename: str
    content_type: str
    payload: bytes

    def to_dict(self) -> dict:
        return {
            'filename': self.filename,
            'content_type': self.content_type,
            # 'payload': self.payload,
            'size_bytes': len(self.payload),
        }
