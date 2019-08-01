# ristra
A tool for facilitating the intake of refugees seeking asylum in Albuquerque.

# Trello
Join our Trello: https://trello.com/b/2WbNbMPk/ristra

# Setting up anew
1. Clone this git repository.
1. Change directory to `ristra/`.
1. Install virtualenv and create a python3 virtual environment; `virtualenv -p python3 venv`.
1. Activate the virtual environment; `source venv/bin/activate`.
1. Download the necessary libraries; `pip install -r requirements.txt`.
1. Comment out the entire `campaign` line in `class Campaigns` in `intake/models.py`.
1. Comment out the uncommented `fields` line in `intake/forms/campaign.py` and uncomment the commented line.
1. Run `python manage.py makemigrations intake`.
1. Set the commenting back to how it previously was and run `python manage.py makemigrations intake` again.
1. Run `python manage.py migrate`.
1. Run `python manage.py bootstrap` to initialize necessary tables.
1. Run `python manage.py createsuperuser` and enter your own credentials.
