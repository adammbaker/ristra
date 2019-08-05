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

# The format of Ristra
Ristra is intended to be used by non-profits who are assisting individuals released by ICE and who need assistance traveling to their destination.

## User accounts
User accounts are required for using this site. Accounts are free to sign up for and they determine your abilities.

### Volunteers
Most users will be volunteers. These accounts are the basic accounts that let volunteers assign families to rooms, take down information on their sponsor, travel plans, and family members.

### Team Leads
Team Leads will be able to do everything a Volunteer can do while also being able to add staging locations and intake buses to (TK) Ristra for a given campaign.

### Points of contact
Points of Contact are the heads of organizations and can do anything a Team Lead can do including creating an organization. Points of Contact are also known as Site Coordinators.

## Campaigns
As another method to mitigate data extraction, the concept of a campaign is utilized. Basically, a campaign restricts the information a user has access by tying their account temporarily to an organization. A campaign is a time-based authorization token that limits a user's view to families (and the children of families) for refugees who arrived on a bus a couple of days before the campaign's start date.

### Starting a campaign
Points of Contact are the only user type to be able to start a campaign. A POC can create an unlimited number of campaigns of varying lengths to help limit the information a user has access to.

Each campaign has a shortened link (à la bit.ly) and a QR code (which links to that shortened link). The short link allows for computer users to manually enter the shortened link and the QR code is intended for use by mobile users. When viewing an individual campaign, this page can be printed and placed in areas around the staging location for convenient user on-boarding.

These shortened links have limited duration as well, so printouts will need to be refreshed as needed. By visiting these links, the user's account is tied directly to the campaign's duration and organization and is indirectly tied to the families belonging to associated intake buses.

## Ristra's Components
### Organization
The organization is the foundation of Ristra's logic. Initially intended for the use by one individual organization, Ristra has been further developed to be used by multiple organizations working in assisting refugees recently released from ICE's detention.

Currently a Point of Contact can only be in charge of a single organization. This may change as needed in the future. Only POCs can edit the information of an individual organization.

### Location
Under each organization, there are locations that the organization uses to receive and process refugees. Locations can be anything but are most commonly motels, dormitories, or churches.

### Intake Bus
Intake buses are the vehicles in which refugees are brought from where ICE released them to the location that belongs to the user's organization. In our case they are buses but they could be individual cars if necessary. What's important is that these are grouped by common arrival.

### Family
On the buses full of refugees are family units. When we were receiving refugees, they were only family units. All other individuals detained by ICE were deported or released in Mexico.

This model is very shallow; that is, it contains many trivia regarding the family but does not speak much to the individuals. It serves as a focal point connecting individual asylees, the family's sponsor, and their travel plans.

### Sponsor
As part of the conditions for release, each family must have the name, address, and contact information for someone already living in the United States of America who will be responsible for the family. Families can only have one sponsor at a time, though this may be able to change in the future as needed. This model is responsible for providing the information necessary for the Travel Team to make travel arrangements for the family.

### Travel Plan
This model contains the details and in future will provide helpful links for validating and centralizing travel information for the given family.

### Asylee
Asylees are considered the individual members of the family unit.

### Medical
Any medical issues that an Asylee is treated for will be noted in this model.

## Capacities
Capacities are the specializations of the individual Volunteers that they choose for themselves in the signup process. Team Leads in their capacity as Team Lead can only be in charge of one specialty at the moment. This may change in the future if there is a desire.

### Activities
Volunteers who choose Activities as a capacity are willing to help in areas that will keep Asylees, specifically children, active and engaged.

*Spanish level desired: minimal*

### Change of Address
Volunteers who choose Change of Address as a capacity will be involved with changing the address or updating contact information as necessary.

*Spanish level desired: minimal*

### Clothes
Volunteers who choose Clothes as a capacity are willing to help in the clothing needs of the organization, sorting and separating donations and making them available to Asylees.

*Spanish level desired: mimimal*

### Departure Bags
Volunteers who choose Departure Bags as a capacity are willing to help prepare meals and various other packets to aid the Family in their travels to their destination.

*Spanish level desired: minimal*

### Food
Volunteers who choose Food as a capacity are willing to contact local restaurants to see if they wish to provide food, to collect any donated food items, cook foods that need to be cooked, and help in general in the kitchen at the Location. Oftentimes these Families have been traveling for a long time without access to adequate food or water, even in government detention.

*Spanish level desired: minimal*

### Intake
Volunteers who choose Intake as a capacity are willing to be personal guides to Families as they are processed from the Intake Bus to their housing at the Location and to connecting them to transportation options to get them to their destination.

*Spanish level desired: moderate*

### Medical
Volunteers who choose Medical as a capacity are willing to help treat medical issues to the best of their ability and document the treatment in Ristra.

*Spanish level desired: minimal*

### Travel
Volunteers who choose Travel as a capacity are willing to help contact the Family's Sponsor and communicate to the Sponsor the transportation details. These volunteers will document as thoroughly as possible the necessary information for a Travel Plan.**

*Spanish level desired: high*

### Transport
Volunteers who choose Transport as a capacity are willing to connect Families to local and long-distance transportation as well as be a personal driver for them. In Albuquerque we have access to a city-provided transportation bus which with a certain frequency can take Families from the Location to a bus station or to the airport.

*Spanish level desired: moderate*

### Volunteer Coordinator
Volunteers who choose Volunteer Coordinator as a capacity are willing to coordinate volunteers to better accommodate refugee assistance.

*Spanish level desired: minimal*

### Other
This is a miscellaneous category for Volunteers who are undecided in their personal capacities or wish to take a position that isn't currently described.
