
from flask import Flask

#from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

#app.config["SECRET_KEY"] = "KeepThisS3cr3t"
# the toolbar is only enabled in debug mode:
#app.debug = True
# set a 'SECRET_KEY' to enable the Flask session cookies
#app.config['SECRET_KEY'] = "KeepThisS3cr3t"
#app.config["DEBUG_TB_PANELS"] = ["flask.ext.mongoengine.panels.MongoDebugPanel"]
#toolbar = DebugToolbarExtension(app)

from app import views

