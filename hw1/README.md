# NYC Restaurant Explorer

A small Django app that helps a group of friends browse NYC restaurants and flag the ones they want to visit together. See [`_docs/plan.md`](_docs/plan.md) for the full product spec and [`backlog.md`](backlog.md) for the implementation task list.

## Requirements

* Python 3.11+ (developed with 3.13)
* Internet access (only needed once, to import restaurant data)

## Setup

Run these from the `hw1/` directory (the one containing `manage.py`).

**1. Create and activate a virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Run database migrations**

```bash
python manage.py migrate
```

This creates a local `db.sqlite3` file with the `Restaurant` and `WantToGo` tables.

**4. Import restaurant data from the NYC API**

```bash
python manage.py import_restaurants
```

This pulls records from the NYC DOHMH Restaurant Inspection Results open dataset (`data.cityofnewyork.us`), deduplicates by restaurant, and stores name/borough/cuisine/address locally. Optionally pass `--limit N` to control how many inspection rows are fetched before deduplicating (default 2000):

```bash
python manage.py import_restaurants --limit 500
```

Safe to re-run — it upserts by restaurant id rather than creating duplicates.

**5. Start the development server**

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in a browser.

**6. Run the automated tests**

```bash
python manage.py test
```

## Using the app

1. Type your name in the "Your name" box and click **Save name**.
2. Browse the restaurant table, or narrow it down with the name search box and the borough/cuisine dropdowns (all three combine together).
3. Click **Want to Go** on a restaurant to flag it; click **Remove Want to Go** to unflag it.
4. Each restaurant shows the names of everyone who flagged it. Restaurants flagged by two or more people are highlighted and labeled "Shared match".

## Known limitations / assumptions (Version 1)

* **No accounts or identity verification.** A "visitor" is just whatever name is typed into the name box, stored in the browser session. Anyone can flag as any name, and two different people typing the same name are treated as one person (their flag toggles the same record). Names are also matched case-sensitively and exact match, so "Alex" and "alex" are treated as different people.
* **Restaurant data is a point-in-time snapshot.** `import_restaurants` fetches a batch of recent inspection rows and keeps one record per restaurant; it does not sync deletions, closures, or full citywide coverage, and needs to be re-run manually to refresh.
* **Sessions are cookie-based and local to one browser.** Flags persist in the shared database (visible to everyone), but the "who am I" name is per-browser-session — clearing cookies or switching browsers loses the remembered name.
* **No pagination.** The restaurant list renders every matching row on one page; this is fine for a small imported dataset but would need pagination for a full citywide import.
* **Single shared database, no multi-tenancy.** All visitors see and flag against the same restaurant list and the same flags — there's no separation between different friend groups.
