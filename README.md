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

### Optional Azure Maps basemap

OSM is the default basemap. To enable the `Microsoft Base Roads` option, set the Azure Maps subscription key in the environment before starting Django:

```text
MapsPrimaryKey=<your-Azure-Maps-primary-key>
```

The Azure Maps client ID is not required for this browser tile-layer integration. Restrict the subscription key to the deployed application origins and rotate it if it has been exposed.

## Azure deployment

- `runtime.txt` selects `python-3.14`
- `Procfile` starts the app with Gunicorn
- `requirements.txt` contains the production dependencies
