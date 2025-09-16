from mongoengine import Document, StringField, DateTimeField, DictField, ListField
from datetime import datetime


class Programs(Document):
    program_name = StringField(required=True)
    created_date = DateTimeField(default=datetime.now)
    config = DictField()
    scopes = ListField(StringField(), default=[])
    ooscopes = ListField(StringField(), default=[])

    meta = {"indexes": [{"fields": ["program_name"], "unique": True}]}

    def json(self):
        return {
            "program_name": self.program_name,
            "created_date": (
                self.created_date.isoformat() if self.created_date else None
            ),
            "config": self.config or {},
            "scopes": self.scopes or [],
            "ooscopes": self.ooscopes or [],
        }
