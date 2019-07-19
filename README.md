# ristra
A tool for facilitating the intake of refugees seeking asylum in Albuquerque.

# Trello
Join our Trello: https://trello.com/b/2WbNbMPk/ristra

# Setting up anew
1. [[stuff here about how you need to set up the virtual env after github cloning and pip requirementing]]
1. Change directory to `ristra/`.
1. Source the virtual environment `source venv/bin/activate`.
1. Comment out the entire `campaign` line in `class Campaigns` in `intake/models.py`.
1. Comment out the uncommented `fields` line in `forms/campaign.py` and uncomment the commented line.
1. Run `python manage.py makemigrations intake`.
1. Set the commenting back to how it previously was and run `python manage.py makemigrations intake` again.
1. Run `python manage.py migrate`.
1. Run `python manage.py createsuperuser` and enter your own credentials.
