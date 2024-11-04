# Kraken technical challenge

This project is a Django web app that imports energy meter reading data from D0010 flow files and stores it in a SQLite database. The web app allows users to browse the imported information using either an MPAN or meter serial number.

Authored by Nitish Lobo.

## Installation instructions

### System prerequistes

- MacOS or Linux (developed on MacOS)
- Python 3.12

### Steps for running the app

1. Navigate to root directory of this project, create and activate a python virtual environment.

    ```bash
    python -m venv .venv
    ```

    ```bash
    source .venv/bin/activate
    ```

2. Install the python libraries for this project using the requirements.txt file

    ```bash
    pip install -r requirements/all.txt
    ```

3. Navigate into project

    ```bash
    cd src
    ```

4. Create the migration files (if not already present)

   ```bash
   python manage.py makemigrations
   ```

5. Apply the migrations

    ```bash
    python manage.py migrate
    ```

6. Import the data

    ```bash
    python manage.py import_d0010_files ../data
    ```

7. Create the superuser

    ```bash
    python manage.py createsuperuser
    ```

    Here is an example:  
    Username: test  
    Email address: <test@kraken.tech>  (without the <>)
    Password: (something secure)  

8. Run the server locally

    ```bash
    python manage.py runserver
    ```

9. Navigate to the admin web app on the browser as per the host and port stdout when you ran the above runserver command.  
    Example:  
    <http://127.0.0.1:8000/admin>

10. Once in the `Energy Readings` view, you can search by either of the following:

    - Flow file name, e.g.: `DTC5259`
    - MPAN Core, e.g.: `1013044353630`
    - Meter ID, e.g.: `D03L80840`
    - Register reading, e.g.: `68902.0`
    - Reading at, e.g.: `2016` or `2016-02` or `2016-02-21` (for year, year-month and year-month-day respectively)

    Note: you can also browse via date hierarchy for ease of use.

### Steps for running the test suite

1. Navigate to root directory of this project and then run the following:

    ```bash
    cd src
    pytest
    ```

    Note: the relevant test configurations have already been made and are in `pyproject.toml` > `Testing and coverage` > `[tool.pytest.ini_options]` > `addopts`, etc.

## Assumptions

- All datetimes from the flow file are assumed to be in UTC.
- D0010 flow files will always have a file footer.
- Any data after file footer is either a blank line or invalid data

## Future improvements

- Check if the file data has been previously added to the database.
  In this case, do not add it again. To do this, utilise the file name, header and footer metadata (such as file_created_at, etc.) to ensure uniqueness.
  Also inform the user that this has been previously addded.
- Have a confirmation step before truncating all tables (management command) incase the user accidentally ran the command.
- Normalise EnergyReading model into smaller models. Denormalising EnergyReading model would also mean that views need to be added rather than being limited to Django admin StackInline or TabularInline setup.
- Create a view instead of using Django admin registers.
- Have a view with some graphs to visualise the data and show users their energy usage based on their MPAN.
- Add integration tests to complement existing unit tests.
- Make `import_file()` in `src/meter_readings/management/commands/import_d0010_files.py` looping more efficient. Refactor so that the data isn't having to get looped over twice.

## Additional considerations

- Would go through deployment checklist before releasing app to production:
  <https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/>
  (includes but is not limited to turning off `DEBUG` in settings.py)

## Bonus features of this project

- ReadOnlyAdminMixin for admin registered views
- Additional command to truncate all database tables
- Makefile to easily remember and run the commands. Includes `make help` which gives a list of the commands
- Linting (git hooks) and configurations (pyproject.toml)
- `.env` file for secrets
- `requirements.txt` split into prod, dev and test
