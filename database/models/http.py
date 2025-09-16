from mongoengine import Document, StringField, DateTimeField, ListField, DictField
from datetime import datetime


class Http(Document):
    program_name = StringField(required=True)
    subdomain = StringField(required=True)
    scope = StringField(required=True)
    ips = ListField(StringField())
    tech = ListField(StringField())
    title = StringField()
    status_code = StringField()
    headers = DictField()
    url = StringField()
    final_url = StringField()
    favicon = StringField()
    created_date = DateTimeField(default=datetime.now())
    last_update = DateTimeField(default=datetime.now())

    meta = {
        "indexes": [
            {
                "fields": ["program_name", "subdomain"],
                "unique": True,
            }  # Create a unique index on 'program_name' and 'subdomain'
        ]
    }

    def json(self):
        return {
            "program_name": self.program_name,
            "subdomain": self.subdomain,
            "scope": self.scope,
            "ips": self.ips or [],
            "tech": self.tech or [],
            "title": self.title,
            "status_code": self.status_code or [],
            "headers": self.headers or {},
            "url": self.url,
            "final_url": self.final_url,
            "favicon": self.favicon,
            "created_date": (
                self.created_date.isoformat() if self.created_date else None
            ),
            "last_update": self.last_update.isoformat() if self.last_update else None,
        }
