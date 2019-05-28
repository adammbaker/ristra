When user accesses main site:
0) Have user sign up for an account
1) Get user to choose a location or determine with geolocation and store with request.session.keys()
2) Present user with lists of families; this will be the default view that users see
3) Provided that the user has the correct permissions, they'll be able to:
    - add new bus
    - add new family (and therefore asylees)
    - add new travel plans
    - add new medical issue

Location (abq fairgrounds/rr)
- users must be able to add locations if it's gonna be used outside of abq metro

Check if there are locations (Locations.objects.count() > 1)
- if not, direct user with correct permissions to add a Location
- if so, forward them to adding intake Bus

Breadcrumbs
