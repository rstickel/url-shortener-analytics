from datetime import datetime
from src import db
import shortuuid


def generate_short_code():
    """Generates a unique short code for the URL."""
    # A short, URL-safe UUID. Adjust length as needed.
    return shortuuid.uuid()[:8]


class ShortURL(db.Model):
    __tablename__ = 'short_urls'

    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(100), unique=True, nullable=False, default=generate_short_code)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    clicks = db.relationship('ClickEvent', backref='short_url', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ShortURL {self.short_code}: {self.long_url}>"


class ClickEvent(db.Model):
    __tablename__ = 'click_events'

    id = db.Column(db.Integer, primary_key=True)
    short_url_id = db.Column(db.Integer, db.ForeignKey('short_urls.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)  # IPv4 max 15, IPv6 max 45
    user_agent = db.Column(db.String(500), nullable=True)
    referrer = db.Column(db.String(2048), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<ClickEvent {self.id} for {self.short_url_id} at {self.timestamp}>"
