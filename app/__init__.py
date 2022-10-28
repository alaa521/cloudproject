from flask import Flask

global memcache

webapp = Flask(__name__)
memcache = {}

data =len(memcache)

from app import main




