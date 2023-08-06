# crownstone-lib-python-cloud

Asynchronous Python library to get data from the cloud, and switch Crownstones.

## Functionality

* Async: using asyncio and aiohttp, optimized for speed.
* Easy to use: sync all your Crownstone Cloud data with just one command!
* Structurally sound: find your data with ease!
* Complete: set the switch state and brightness of your Crownstones remotely!
* Flexible: Login and get the data for multiple accounts at once!

## Requirements

* Python 3.7 or higher
* Aiohttp 3.6.2

## Standard installation

cd to the project folder and run:
```console
$ python setup.py install
```

## Install in a virtual environment

To install the library execute the following command:
```console
$ python -m venv venv
```
Activate your venv using:
```console
$ source venv/bin/activate
```
Once activated, the venv is used to executed python files, and libraries will be installed in the venv.<br>
To install this library, cd to the project folder and run:
```console
$ python setup.py install
```

## Getting started

### Examples

#### Async example

```python
from crownstone_cloud import CrownstoneCloud, create_clientsession
import logging
import asyncio

# Enable logging.
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


async def main():
    # Every instance creates it's own websession for easy accessibility, however using 1 websession is recommended.
    # Create your websession like so:
    websession = create_clientsession()
    # Initialize cloud.
    cloud_user_1 = CrownstoneCloud('email_user_1', 'password_user_1', websession)
    # Login to the Crownstone Cloud and synchronize all cloud data.
    await cloud_user_1.async_initialize()

    # Get a crownstone by name that can dim, and put it on 20% brightness for user 1
    crownstone_lamp = cloud_user_1.get_crownstone('Lamp')
    await crownstone_lamp.async_set_brightness(20)

    # Login & synchronize data for an other account.
    cloud_user_2 = CrownstoneCloud('email_user_2', 'password_user_2', websession)
    await cloud_user_2.async_initialize()

    # Get a crownstone by name and turn it on for user 2.
    crownstone_tv = cloud_user_2.get_crownstone('TV')
    await crownstone_tv.async_turn_on()

    # If you want to update specific data you can get the cloud data object for your user.
    # This object has all the cloud data for your user saved in it, which was synced with async_initialize()
    # Parts of the data can also be synced individually without touching the other data.
    # To sync all data at once, use async_synchronize() instead.
    my_sphere = cloud_user_1.cloud_data.find("my_sphere_name")
    # request to sync only the locations with the cloud
    my_sphere.locations.async_update_location_data()
    # get the keys for this sphere so you can use them with the Crownstone BLE python library
    sphere_keys = my_sphere.async_get_keys()

    # Close the aiohttp clientsession after we are done.
    await websession.close()

asyncio.run(main())
```

#### Sync example

```python
from crownstone_cloud import CrownstoneCloud, run_async
import logging

# Enable logging.
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# Initialize cloud.
cloud = CrownstoneCloud('email', 'password')
# Use 'run_async' to run async functions in sync context.
# Login & synchronize all cloud data.
run_async(cloud.async_initialize())

# Get a crownstone by name and turn it on.
crownstone_coffee_machine = cloud.get_crownstone('Coffee machine')
run_async(crownstone_coffee_machine.async_turn_on())

# Close the session after we are done.
run_async(cloud.async_close_session())
```

### Initialization

The Crownstone cloud is initialized with the email and password of a user:
```python
cloud = CrownstoneCloud('email', 'password')
```
If you do not yet have a Crownstone account, go to [My Crownstone](https://my.crownstone.rocks) to set one up.
The email and password are used to re-login after an access token has expired.

You can log into multiple accounts by creating more CrownstoneCloud objects. When doing so, it is recommended to use
only 1 websession for all your requests. Create a websession and append it as parameter to all your CrownstoneCloud
objects. Take a look at the async example above.
```python
cloud = CrownstoneCloud('email', 'password', websession)
```
To log in and get all your Crownstone from the cloud:
```python
await cloud.async_initialize()
```

## Data structure

The cloud can be displayed with the following structure:
* User
    * Keys
    * Spheres
        * Locations
        * Crownstones
        * Users
        

### User

The user is the to whom the data belongs.<br> 
The user is the one that logs in using email and password.<br>
By getting a user specific access token after login, the data for that specific user can be requested.

### Keys

The keys are user specific.<br> 
They are required to connect to the crownstone bluetooth mesh.<br>
The most common used keys are the sphere keys. They are located within each individual sphere.<br>

### Spheres

Spheres are the main data entry. They have rooms (locations), Crownstones and users in them.<br>
Example spheres:
* House
* Office
* Apartment

A Sphere has the following fields in the cloud lib:
* crownstones: Crownstones
* locations: Locations
* users: Users
* keys: Dict (optional, default = None)
* name: String
* cloud_id: String
* unique_id: String
* present_people: List

### Locations

Locations are the rooms in your house or other building.<br>
For example for a house: 
* Living room
* Bedroom
* Garage
* Bathroom

A Location has the following fields in the cloud lib:
* present_people: List
* name: String
* cloud_id: String
* unique_id: String

### Crownstones

Crownstones are smart plugs that can make every device that isn't smart, way smarter!<br>
Crownstones are located within a sphere.<br>
Example names of Crownstones:
* Lamp
* Charger
* Television

A Crownstone has the following fields in the cloud lib:
* abilities: Dict
* state: Int (0..100)
* name: String
* unique_id: String
* cloud_id: String
* type: String
* sw_version: String

### Users

Users are people who have access to a sphere.<br>
A user can have 3 roles:
* Admin
* Member
* Guest

A User has the following fields in the cloud lib:
* role: String
* first_name: String
* last_name: String
* email: String
* cloud_id: String
* email_verified: Bool

## Function list

### Cloud

#### async_initialize()
> Login and sync all data for the user from the cloud.

#### async_synchronize()
> Synchronize all data for a user. Use case is to update the local data with new data from the cloud.
> This function is already called in `async_initialize()`.

#### get_crownstone(crownstone_name: String) -> Crownstone
> Get a Crownstone object by name for a user, if it exists.

#### get_crownstone_by_id(crownstone_id: String) -> Crownstone
> Get a Crownstone object by it's id for a user, if it exists.

#### async_close_session()
> Async function. This will close the websession in requestHandler to cleanup nicely after the program has finished.

### Spheres

#### async_update_sphere_data()
> Async function. Sync the Spheres with the cloud. Calling the function again after init will update the current data.

#### find(sphere_name: String) -> Sphere
> Returns a sphere object if one exists by that name.

#### find_by_id(sphere_id: String) -> Sphere
> Return a sphere object if one exists by that id.

### Sphere

#### async_update_sphere_presence()
> Async function. Sync the presence of users in the sphere with the cloud.

#### async_get_keys() -> Dict
> Async function. Returns a dict with the keys of this sphere. 
> The keys can be used for BLE connectivity with the Crownstones.

### Crownstones

#### async_update_crownstone_data()
> Async function. Sync the Crownstones with the cloud for a sphere. 
> Calling the function again after init will update the current data.

#### find(crownstone_name: String) -> Crownstone
> Return a Crownstone object if one exists by that name.

#### find_by_id(crownstone_id: String) -> Crownstone
> Return a Crownstone object if one exists by that id.

### Crownstone

#### async_turn_on()
> Async function. Send a command to turn a Crownstone on. 
> To make this work make sure to be in the selected sphere and have Bluetooth enabled on your phone.

#### async_turn_off()
> Async function. Send a command to turn a Crownstone off. 
> To make this work make sure to be in the selected sphere and have Bluetooth enabled on your phone.

#### async_set_brightness(value: Integer)
> Async function. Send a command to set a Crownstone to a given brightness level. 
> To make this work make sure to be in the selected sphere and have Bluetooth enabled on your phone.
> The value parameter should be between 0 and 100.

### Locations

#### async_update_location_data()
> Async function. Sync the Locations with the cloud for a sphere. Calling the function again after init will update the current data.

#### async_update_location_presence()
> Async function. Sync the presence with the cloud. This will replace the current presence with the new presence.

#### find(location_name: String) -> Location
> Return a location object if one exists by that name.

#### find_by_id(location_id: String) -> Location
> Return a location object if one exists by that id.

### Users

#### async_update_user_data()
> Async function. Sync the Users with the cloud for a sphere. Calling the function again after init will update the current data.

#### find_by_first_name(first_name: String) -> List
> Returns a list of all users with that first name, as duplicate first names can exist.

#### find_by_last_name(last_name: String) -> List
> Return a list of all users with that last name, as duplicate last names can exist.

#### find_by_id(user_id: String) -> Location
> Return a location object if one exists by that id.

## Async vs sync
The lib can be used synchronously and asynchronously.<br>
The disadvantage of sync context is that all functions are blocking. 
The program will simply wait until a function is complete. In async context, functions (coroutines) can yield control,
which means that functions can be "paused" while they are waiting for external data to come in, like data from a server.
Other functions can then be executed in the meantime. This way the program is always busy.<br>

All async functions in the library API functions in this library have the prefix **async_**
Async functions need to be awaited:
```Python
await cloud.async_close_session()
```
All the async functions mentioned above can also be used synchronously.<br>
Use the `run_async()` function like so:
```Python
from crownstone_cloud import run_async

run_async(cloud.async_close_session())
```
Make sure to see the examples above!

## Testing

To run the tests using tox install tox first by running:
```console
$ pip install tox
```
To execute the tests cd to the project folder and run:
```console
$ tox
```
To see which parts of the code are covered by the tests, a coverage report is generated after the tests have been successful.<br>
To see the coverage report run:
```console
$ coverage report
```
If you like to get a better overview of the test you can generate a HTML file like so:
```console
$ coverage html
```
To view your html file directly on Linux:
```console
$ ./htmlcov/index.html
```
On Windows simply navigate to the htmlcov folder inside the project folder, and double-click index.html. It will be executed in your selected browser.
