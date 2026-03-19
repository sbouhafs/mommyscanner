from datetime import datetime, timezone
from extensions import db


class Product(db.Model):
    """A product looked up by barcode."""

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(64), unique=True, nullable=False, index=True)
    name = db.Column(db.String(256), nullable=False)
    brand = db.Column(db.String(128))
    ingredients = db.Column(db.Text)
    image_url = db.Column(db.String(512))
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    scans = db.relationship("Scan", backref="product", lazy=True)

    def __repr__(self):
        return f"<Product {self.barcode} {self.name!r}>"


class Scan(db.Model):
    """A record of a barcode scan performed by a user."""

    __tablename__ = "scans"

    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(64), nullable=False, index=True)
    scanned_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=True)
    note = db.Column(db.String(256))

    def __repr__(self):
        return f"<Scan {self.barcode} at {self.scanned_at}>"
