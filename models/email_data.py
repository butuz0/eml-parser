from dataclasses import dataclass, field
from typing import Optional
import datetime as dt

from .email_attachment import EmailAttachment


@dataclass(frozen=True, slots=True)
class EmailData:
    email_from: str
    date: dt.datetime
    email_to: Optional[str] = None
    delivered_to: Optional[str] = None
    cc: Optional[str] = None
    subject: Optional[str] = None
    thread_topic: Optional[str] = None
    text_body: Optional[str] = None
    html_body: Optional[str] = None
    attachments: list[EmailAttachment] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            'metadata': {
                'email_from': self.email_from,
                'email_to': self.email_to,
                'delivered_to': self.delivered_to,
                'cc': self.cc,
                'subject': self.subject,
                'thread_topic': self.thread_topic,
                'date': self.date.isoformat(),
            },
            'text_body': self.text_body,
            'html_body': self.html_body,
            'attachments': [att.to_dict() for att in self.attachments],
        }
