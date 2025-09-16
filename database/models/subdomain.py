from mongoengine import Document, StringField, DateTimeField, ListField
from datetime import datetime


class Subdomains(Document):
    program_name = StringField(required=True)
    subdomain = StringField(required=True)
    scope = StringField(required=True)
    providers = ListField(StringField())
    created_date = DateTimeField(default=datetime.now)
    last_update = DateTimeField(default=datetime.now)

    meta = {"indexes": [{"fields": ["program_name", "subdomain"], "unique": True}]}

    def json(self):
        return {
            "program_name": self.program_name,
            "subdomain": self.subdomain,
            "scope": self.scope,
            "providers": self.providers or [],
            "created_date": (
                self.created_date.isoformat() if self.created_date else None
            ),
            "last_update": (self.last_update.isoformat() if self.last_update else None),
        }
