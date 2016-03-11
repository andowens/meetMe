"""
Configuration of 'memos' Flask app.
Edit to fit development or deployment environment.

"""
import random

### My local development environment
PORT=5000
DEBUG = True

### MongoDB settings
MONGO_PORT=27017

### The following are for a Mongo user for accessing the meetings database
MONGO_PW = "uremember"
MONGO_USER = "main"
MONGO_URL = "mongodb://{}:{}@localhost:{}/meetings".format(MONGO_USER,MONGO_PW,MONGO_PORT)

#ix port
#PORT= 8234
#DEBUG = False # Because it's unsafe to run outside localhost
GOOGLE_LICENSE_KEY = "client_secret.json"

