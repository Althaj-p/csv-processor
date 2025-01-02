# Django CSV Upload API

## Overview
This project implements a Django REST Framework (DRF) API for uploading and processing CSV files. The API validates the data, saves valid records to the database, and provides a detailed summary of the operation.

---

## Features
- Upload CSV files via a POST endpoint.
- Validate data:
  - `name`: Must be a non-empty string.
  - `email`: Must be a valid email address.
  - `age`: Must be an integer between 0 and 120.
- Skip duplicate email addresses gracefully.
- Return a summary of:
  - Total valid records saved.
  - Total rejected records.
  - Detailed errors for rejected records.

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- Django 4.x
- Django REST Framework

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>

2. Create a virtual environment and activate it:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
  ```bash
  pip install -r requirements.txt

4. Run migrations to set up the database:
  ```bash
  python manage.py makemigrations
  python manage.py migrate

5. Start the development server:
  python manage.py runserver


URLS:
:- Home Page : http://127.0.0.1:8000/Api/home
