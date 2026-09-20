# Pro Auction Live

A Django web application for running a live sports auction. Create an auction event, import players from a CSV or Excel file, manage live bidding, assign teams and roles, revisit archived events, and export final results.

## Features

- Create an event with a configurable number of teams, team budget, and admin PIN.
- Import player data from `.csv` or `.xlsx` files.
- Auto-map common player-column names such as name, email, category, position, department, year, base price, and image URL.
- Run live player selection and bidding, then mark players as sold or unsold.
- Prioritize players, revisit the unsold pool, transfer sold players, and rename teams.
- Assign captain and vice-captain names to teams.
- Keep a history of auction events and export the active event as CSV.

## Tech stack

- Python and Django 4.2
- SQLite for local development; PostgreSQL for production
- Pandas and OpenPyXL for spreadsheet imports/exports
- Gunicorn and WhiteNoise for production hosting
- Tailwind CSS (loaded from CDN)

## Requirements

- Python 3.8 or later
- `pip`

## Run locally

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

Open <http://127.0.0.1:8000/> in a browser.

To run Django's configuration checks:

```bash
python3 manage.py check
```

## Starting an auction

1. Open the home page.
2. Enter an event name and an admin PIN.
3. Upload a CSV or Excel player list.
4. Set the number of teams and their starting budget.
5. Select **Create New Event**.
6. Use the dashboard to spin for players, update bids, sell/mark unsold players, and manage teams.

Creating a new event archives the previous active event rather than deleting it.

### Player file format

The importer requires a player-name column. It recognizes these common aliases:

| Application field | Accepted column names |
| --- | --- |
| Name | `player`, `player name`, `fullname`, `name`, `full name` |
| Email | `email`, `email address`, `contact`, `mail`, `id`, `Mobile No.` |
| Category | `category`, `cat`, `group`, `tier`, `type`, `role` |
| Position | `position`, `speciality`, `playing role`, `playing position` |
| Department | `department`, `dept`, `branch`, `section` |
| Year | `year`, `y` |
| Base price | `baseprice`, `base price`, `cost`, `starting bid`, `price`, `points`, `base` |
| Image URL | `image`, `photo`, `pic`, `url`, `image link` |

Missing base prices are imported as `0`. Duplicate non-empty email addresses are removed during import.

## Main routes

| Route | Purpose |
| --- | --- |
| `/` | Create a new auction or resume the active one |
| `/dashboard/` | Live auction dashboard |
| `/archives/` | Archived auction list |
| `/archives/<event-id>/` | Archive details |
| `/export/` | Download the active event's final CSV report |

## Environment variables

Create a local `.env` file if needed. It is intentionally ignored by Git.

```dotenv
SECRET_KEY=replace-with-a-long-random-value
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

For production, set `DEBUG=False`, use a unique `SECRET_KEY`, and restrict `ALLOWED_HOSTS` to the public hostname.

## Deploy to Render

The repository includes [`build.sh`](build.sh), which installs packages, collects static files, and applies migrations.

Before deploying, configure [`sports_auction/settings.py`](sports_auction/settings.py) to use `DATABASE_URL` so Render can connect PostgreSQL:

```python
import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}
```

Then:

1. Push this repository to GitHub.
2. In Render, create a PostgreSQL database.
3. Create a Python **Web Service** connected to this repository.
4. Set the build command to `./build.sh`.
5. Set the start command to `gunicorn sports_auction.wsgi:application`.
6. Add these Render environment variables:

   ```text
   DATABASE_URL=<Render internal PostgreSQL URL>
   SECRET_KEY=<generate a secure value in Render>
   DEBUG=False
   ALLOWED_HOSTS=<your-service>.onrender.com
   ```

SQLite is suitable only for local development; it is not a durable production database on typical cloud deployments. The local `db.sqlite3` file is ignored, so seed/import your auction data after deploying or migrate it deliberately.

See [Render's Django deployment documentation](https://render.com/docs/deploy-django) for the current platform instructions.

## Project structure

```text
auction_engine/       Auction models and application views
sports_auction/       Django project configuration and URL routes
templates/            Setup, dashboard, and archive templates
build.sh              Render build script
requirements.txt      Python dependencies
manage.py             Django management entry point
```

## Security note

The current application exposes several management endpoints for use by the live dashboard. Before sharing it publicly, review authentication, admin-PIN handling, CORS settings, and the image-proxy endpoint to ensure they match your intended audience.
