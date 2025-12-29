# Plex873 Database Schema

This project uses a MySQL/MariaDB database to manage a movie library. The schema consists of two primary tables designed to separate core ownership data from cached metadata fetched via the TMDB API.

## Installation Guide

### 1. Prerequisites
* **OS**: Fedora, RHEL, or CentOS Stream (Recommended)
* **Python**: 3.9+
* **Database**: MariaDB or MySQL
* **Web Server**: Nginx

### 2. Clone & Environment Setup
Navigate to your preferred installation directory (e.g., `/opt/`) and clone the repository.

```bash
cd /opt
sudo git clone [https://github.com/Operator873/Plex873-webapp.git](https://github.com/Operator873/Plex873-webapp.git) plex873
cd plex873

# Create a virtual environment
python3 -m venv .venv

# Activate the environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
This application uses environment variables for security to ensure sensitive keys are not hardcoded. A sanitized example file (`.env.example`) is provided in the repository.

```bash
# Copy the example file to a production .env file
cp .env.example .env

# Edit the file with your specific secrets
nano .env
```

### 4. Database Initialization
Log into your MySQL/MariaDB server and create the database and tables using the SQL commands found in the **Table Definitions** section above.

```bash
# Example: Import schema if saved to a file
mysql -u root -p < database_schema.sql
```  

*Alternatively, you can just copy/paste the commands into a SQL shell*

### 5. Running the Application

**Option A: Development (Debug Mode)**
Use this for local testing to see errors in real-time.
```bash
python3 run.py
# Access at http://<server-ip>:5000
```

**Option B: Production (Systemd & Gunicorn)** For a permanent deployment, use Systemd to manage the Gunicorn process.

1. Create a systemd service file at `/etc/systemd/system/plex873.service`:

```ini
[Unit]
Description=Gunicorn instance to serve Plex873
After=network.target

[Service]
# Adjust User/Group to match your specific setup (e.g., 'hades')
User=hades
Group=nginx
WorkingDirectory=/opt/plex873
Environment="PATH=/opt/plex873/.venv/bin"
ExecStart=/opt/plex873/.venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 -m 007 run:app

[Install]
WantedBy=multi-user.target
```

2. Reload Systemd and start the service
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now plex873.service
```

## Database design
### Relationships

* **One-to-One**: The relationship between `movies` and `movie_metadata` is 1:1.
* **Primary Key Sharing**: Both tables use `tmdbid` (The Movie Database ID) as their Primary Key.
* **Foreign Key**: `movie_metadata.tmdbid` is a Foreign Key referencing `movies.tmdbid`.

---

### Table Definitions

#### 1. `movies`
This is the parent table. It represents the physical existence of a file in the library and who owns it.

* **tmdbid** (PK): The unique ID from The Movie Database.
* **title**: The movie title as parsed from the filename.
* **year**: The release year.
* **owner**: The specific user or library section this file belongs to (e.g., "Operator873").

#### 2. `movie_metadata`
This is the child table. It acts as a local cache for API data to reduce external requests and speed up page loads.

* **tmdbid** (PK, FK): links back to the `movies` table.
* **poster_path**: The URL suffix for the movie poster.
* **backdrop_path**: The URL suffix for the large background image.
* **overview**: The full plot summary.
* **vote_average**: The community rating (0.0 - 10.0).
* **release_date**: The specific theatrical release date.

---

### Initialization SQL

You can run the following SQL commands to manually create the tables in your MySQL database.

```sql
-- 1. Create the Parent Table (movies)
CREATE TABLE IF NOT EXISTS movies (
    tmdbid INT NOT NULL,
    title VARCHAR(255),
    year INT,
    owner VARCHAR(255),
    PRIMARY KEY (tmdbid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Create the Child Table (movie_metadata)
-- Includes a foreign key constraint to ensure metadata cannot exist without a parent movie.
-- ON DELETE CASCADE ensures if you delete a movie, its cached metadata is also removed.
CREATE TABLE IF NOT EXISTS movie_metadata (
    tmdbid INT NOT NULL,
    poster_path VARCHAR(255),
    backdrop_path VARCHAR(255),
    overview TEXT,
    vote_average FLOAT,
    release_date DATE,
    PRIMARY KEY (tmdbid),
    CONSTRAINT fk_movie_metadata_movies 
        FOREIGN KEY (tmdbid) 
        REFERENCES movies (tmdbid) 
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;