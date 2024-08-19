# KVuno Api

## Overview

This is a Flask application that processes RDS files, loads the data into a SQLite database, and tracks processed files.

The project uses SQLAlchemy for database interactions and Alembic for database migrations.

## Project Structure


### `app/`

- **`__init__.py`**: Initializes the Flask application and SQLAlchemy.
- **`routes.py`**: Defines the application's routes and handlers.
- **`config.py`**: Contains configuration settings for different environments.
- **`models/`**: Package for SQLAlchemy models.
    - **`__init__.py`**: Initializes the models package.
    - **`base.py`**: Contains the base class for SQLAlchemy models.
    - **`models.py`**: Defines database models.

### `migrations/`

Contains Alembic migration scripts and configuration files for managing database schema changes.

### `static/`

- **`data/`**: Directory where RDS files are placed for processing.

### `run.py`

The entry point for running the Flask application.

### `pyproject.toml`

Configuration file for Poetry, listing project dependencies and settings.

### `alembic.ini`

Configuration file for Alembic.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo


## Installation

### 1. Clone the Repository

```bash
git clone git@github.com:AgWISE-EiA/kvuno-api.git
cd kvuno-api
