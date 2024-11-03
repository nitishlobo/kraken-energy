# Technical test requirements

## Checklist

- Python 3.10 or above
- Work on macOS or Linux and run without Docker
- Django web app
- .git folder with commit history
- README.md
  - explain how to install and use project
  - include name - Nitish Lobo
  - instructions on how to run the tests
- Management command that can be called with the path to:
  - D0010 file
  - D0010 files
  - Data should be read from file and stored in local db (Postgres or SQLite)
- Error handling
- Version of Django admin site that allows user to:
  - Search for reading values and dates associated with either:
    - an MPAN
    - a meter serial number
    - results should show filename of the flow file that the reading came from
- Test suite
- Document any assumptions made or ideas to improve the project
- Go through any unsafe production settings in settings.py
  - Switch DEBUG from True to False
  - See <https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/>
- List of "what you didn't have time to complete"
- Gzipped tarball in google drive with a link emailed back to <ben.smith1@kraken.tech>

## Additional notes

- Flow files
  - pipe-delimtied text files
  - import each file into database
  - D0010 files are the only files relevant for this project
  - imported via command line, but later a REST interface could be added to allow user to upload via web
