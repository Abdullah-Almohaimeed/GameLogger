# GameLogger

A desktop tool that captures video game metadata from the RAWG API and stores it in a PostgreSQL database via a Windows right-click context menu.

## How It Works

Right-click any game shortcut on your desktop, select **"Check Game"**, and GameLogger will:
- Query the [RAWG API](https://rawg.io/apidocs) for game metadata
- Store the results in a local PostgreSQL database
- Log the operation to `C:\GameLogger\gamelogger.log`

## Data Captured

| Field | Source |
|---|---|
| Name | RAWG API |
| Release Year | RAWG API |
| Genres | RAWG API |
| Platforms | RAWG API |
| RAWG Rating | RAWG API |
| Metacritic Score | RAWG API |
| Average Playtime | RAWG API |
| Beat (year) | User input |
| Self Rating | User input |
| Date Added | Auto-generated |

## Prerequisites
- Python 3.x
- PostgreSQL
- A free [RAWG API key](https://rawg.io/apidocs)

## Installation

1. Clone the repo:
```
git clone https://github.com/yourusername/GameLogger.git
cd GameLogger
```

2. Run `install.bat` — this will install dependencies, copy files to `C:\GameLogger\`, create a `.env` template, and register the right-click context menu automatically.

3. Fill in your credentials in `C:\GameLogger\.env`:
```
RAWG_API_KEY=your_rawg_api_key
DB_HOST=localhost
DB_PORT=5432
DB_NAME=gamelogger
DB_USER=postgres
DB_PASSWORD=your_postgres_password
```

4. Create the database and table in PostgreSQL:
```sql
CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    released CHAR(4),
    genres VARCHAR(255),
    platforms TEXT,
    user_rating NUMERIC(3,2),
    metacritic INT,
    playtime INT,
    beat CHAR(4),
    self_rating NUMERIC(3,1),
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

5. Right-click any game shortcut and select **"Check Game"** to start logging!

## Tech Stack
- Python
- PostgreSQL
- RAWG API
- psycopg2
- python-dotenv