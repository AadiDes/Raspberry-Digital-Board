# Factory Display System

A client-specific Raspberry Pi-based dashboard to show production metrics, safety messages, and announcements.

## Features
- Fullscreen factory display page for TV (date, time, metrics, slogans)
- Admin panel to update live values and schedule image posters
- Raspberry Pi-ready kiosk setup with Flask + SQLite

## Tech Stack
- Python (Flask)
- SQLite
- HTML/CSS/JS

## Environment Variables Setup

1. Copy `.env.example` to `.env`:
   
   cp .env.example .env

2. Open `.env` and fill in your own values for `SECRET_KEY` and `ADMIN_PASSWORD`.

3. Install dependencies (if not already):
   
   pip install -r requirements.txt

The `.env` file is already in `.gitignore` and will not be committed to version control.
