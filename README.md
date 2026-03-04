# MommyScanner

A barcode scanner web app for moms, built with Python/Flask and backed by SQLite. Product data is fetched from [Open Food Facts](https://world.openfoodfacts.org/).

## Features

- **Barcode lookup** – enter any product barcode to retrieve its name, brand, and ingredients
- **Scan history** – every scan is saved to the local database
- **Product cache** – products are stored locally after the first lookup to avoid repeated API calls
- **Database version control** – schema changes are managed through [Alembic](https://alembic.sqlalchemy.org/) migrations (via Flask-Migrate)

## Project structure

```
.
├── main.py              # Flask app factory & entry point
├── models.py            # SQLAlchemy models (Product, Scan)
├── routes.py            # URL route handlers
├── requirements.txt     # Python dependencies
├── migrations/          # Alembic migration scripts (database version control)
│   └── versions/        # Individual migration files
├── templates/           # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── history.html
│   └── products.html
├── .replit              # Replit run configuration
└── replit.nix           # Nix package dependencies for Replit
```

## Local development

```bash
# Install dependencies
pip install -r requirements.txt

# Apply database migrations
flask --app main db upgrade

# Run the development server
python main.py
```

Then open <http://localhost:5000> in your browser.

## Database migrations

Schema changes are tracked as versioned migration scripts under `migrations/versions/`.

```bash
# Create a new migration after changing models.py
flask --app main db migrate -m "describe your change"

# Apply pending migrations
flask --app main db upgrade

# Roll back the last migration
flask --app main db downgrade
```

## Deployment on Replit

Click **Run** in your Replit workspace. The `.replit` file configures the app to start automatically. For production deployments, the gunicorn command in the `[deployment]` section is used.