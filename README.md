# BlueSplit

A Django 6 application scaffolded to run on Azure Web App.

## Local setup

1. Create and activate the virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
3. Run migrations and start the development server:
   ```powershell
   python manage.py migrate
   python manage.py runserver
   ```

## Azure deployment

- `runtime.txt` selects `python-3.14`
- `Procfile` starts the app with Gunicorn
- `requirements.txt` contains the production dependencies
