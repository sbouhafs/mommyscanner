import requests
from flask import jsonify, render_template, request

OPEN_FOOD_FACTS_URL = "https://world.openfoodfacts.org/api/v2/product/{barcode}.json"


def _lookup_product(barcode):
    """Fetch product info from Open Food Facts. Returns a dict or None."""
    try:
        resp = requests.get(
            OPEN_FOOD_FACTS_URL.format(barcode=barcode), timeout=5
        )
        data = resp.json()
        if data.get("status") == 1:
            product = data["product"]
            return {
                "name": product.get("product_name") or "Unknown product",
                "brand": product.get("brands") or "",
                "ingredients": product.get("ingredients_text") or "",
                "image_url": product.get("image_url") or "",
            }
    except Exception:
        pass
    return None


def register_routes(app):
    from models import Product, Scan
    from extensions import db

    @app.route("/")
    def index():
        recent_scans = (
            Scan.query.order_by(Scan.scanned_at.desc()).limit(10).all()
        )
        return render_template("index.html", recent_scans=recent_scans)

    @app.route("/scan", methods=["POST"])
    def scan():
        barcode = (request.json or {}).get("barcode", "").strip()
        if not barcode:
            return jsonify({"error": "No barcode provided"}), 400

        # Record the scan
        scan_record = Scan(barcode=barcode)

        # Check local cache first
        product = Product.query.filter_by(barcode=barcode).first()
        if not product:
            info = _lookup_product(barcode)
            if info:
                product = Product(barcode=barcode, **info)
                db.session.add(product)

        if product:
            scan_record.product_id = product.id

        db.session.add(scan_record)
        db.session.commit()

        if product:
            return jsonify(
                {
                    "barcode": barcode,
                    "name": product.name,
                    "brand": product.brand,
                    "ingredients": product.ingredients,
                    "image_url": product.image_url,
                }
            )
        return jsonify({"barcode": barcode, "name": "Product not found"}), 404

    @app.route("/history")
    def history():
        scans = Scan.query.order_by(Scan.scanned_at.desc()).all()
        return render_template("history.html", scans=scans)

    @app.route("/products")
    def products():
        all_products = Product.query.order_by(Product.name).all()
        return render_template("products.html", products=all_products)
