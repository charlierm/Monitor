from flask import Flask
app = Flask(__name__)

from monitor.views import *
from monitor.filters import *
