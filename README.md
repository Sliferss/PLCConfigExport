# PLCConfigExport

--- ruff commands for lint ---
    ruff check --fix .
    ruff format .

--- run development server ---
    py manage.py runserver

--- make database migrations from code ---
    py manage.py makemigrations

--- setup tables on fresh database / update database with new tables ---
    py manage.py migrate

--- create app folder ---
    py manage.py startapp "name"

--- create superuser ---
    py manage.py createsuper

