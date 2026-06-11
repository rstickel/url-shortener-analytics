# URL Shortener with Analytics

This is a Flask-based URL shortener service that allows users to create custom short links and track detailed analytics for each click.

## Features

-   Shorten long URLs into concise, custom short links.
-   Track click analytics: timestamps, IP addresses, user agents, referrers, and (optionally) geographical data.
-   Simple web interface for URL shortening and viewing analytics.
-   Basic API for programmatic URL shortening.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/url-shortener.git
    cd url-shortener
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables:**
    Create a `.env` file in the root directory based on `.env.example`:
    ```bash
    cp .env.example .env
    ```
    Edit `.env` and set `SECRET_KEY` to a strong random string.

5.  **Initialize the Database:**
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```
    (For development convenience, you can also use `flask create-db` after `flask db init` if no data exists)

6.  **Run the application:**
    ```bash
    flask run
    ```

    The application will be accessible at `http://127.0.0.1:5000`.

## Usage

-   **Shorten a URL:** Go to the homepage and enter a long URL. You can optionally provide a custom short code.
-   **Access Short URL:** Visit `http://127.0.0.1:5000/<your_short_code>` to be redirected to the original URL.
-   **View Analytics:** Visit `http://127.0.0.1:5000/<your_short_code>/stats` to see click statistics.

## API Usage

**Shorten a URL (POST request):**

`POST /api/shorten`

**Request Body (JSON):**
```json
{
    "long_url": "https://www.example.com/very/long/url",
    "custom_code": "mycustomlink" (optional)
}
```

**Response Body (JSON):**

Success:
```json
{
    "short_url": "http://127.0.0.1:5000/mycustomlink",
    "long_url": "https://www.example.com/very/long/url",
    "short_code": "mycustomlink"
}
```

Error:
```json
{
    "error": "Custom code already in use."
}
```

## Project Structure

```
url-shortener/
├── src/
│   ├── __init__.py         # Application factory, blueprint registration, extensions
│   ├── config.py           # Configuration settings
│   ├── models.py           # SQLAlchemy database models
│   ├── forms.py            # WTForms for input validation
│   ├── views/
│   │   ├── __init__.py     # Defines the main blueprint
│   │   ├── main.py         # Web routes (index, shorten, redirect, analytics)
│   │   └── api.py          # API routes
│   ├── templates/          # Jinja2 templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── short_url.html
│   │   └── analytics.html
│   └── static/             # Static assets (CSS, JS)
│       ├── css/style.css
│       └── js/main.js
├── instance/               # Instance-specific configuration (ignored by Git)
├── migrations/             # Alembic migration scripts
├── app.py                  # Entry point for the Flask application
├── pyproject.toml          # Project metadata and dependencies
├── requirements.txt        # Python package dependencies
├── .env.example            # Example environment variables file
└── README.md               # This file
```

## Customization and Development

-   **Database:** By default, it uses SQLite. For production, consider PostgreSQL or MySQL by changing `SQLALCHEMY_DATABASE_URI` in `config.py` and installing the appropriate database driver (e.g., `psycopg2-binary` for PostgreSQL).
-   **Geo-IP Lookup:** The `ClickEvent` model includes fields for `country` and `city`, but the current implementation records `ip_address` only. To populate `country` and `city`, you'd need to integrate with a Geo-IP service (e.g., `ipapi.com`, `ipinfo.io`) using a library like `requests` or `flask-ipinfo`.
-   **Analytics Charts:** The analytics page currently displays raw data. Integrate a JavaScript charting library (e.g., Chart.js, D3.js) for interactive visualizations.
-   **Error Handling:** Implement more robust error handling and custom error pages (404, 500).
-   **User Authentication:** For multi-user support (each user manages their own links), integrate Flask-Login or Flask-Security-Too.
-   **Caching:** For performance, consider adding caching for frequently accessed data using Flask-Caching.
