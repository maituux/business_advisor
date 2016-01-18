from flask import Flask
import os
import sys
sys.path.append('/Users/utilisateur/Desktop/business/app')


#from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
#port = int(os.getenv('VCAP_APP_PORT', 8080))

app.config['SECRET_KEY'] ='sdfsdf82347$$%$%$%$&fsdfs!!ASx+__WEBB$'


#where we store the uploaded file(use double slash to avoid the IOError22: invalid filename)
UPLOAD_FOLDER = os.path.expanduser("~/Desktop/business/app/test")
#UPLOAD_FOLDER = os.path.expanduser("C:\\Users\\POLY\Google Drive\\Desktop\\business\\app\\test")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.update(dict(  
    SECRET_KEY='development key'
))

#app.config["SECRET_KEY"] = "KeepThisS3cr3t"
# the toolbar is only enabled in debug mode:
#app.debug = True
# set a 'SECRET_KEY' to enable the Flask session cookies
#app.config['SECRET_KEY'] = "KeepThisS3cr3t"
#app.config["DEBUG_TB_PANELS"] = ["flask.ext.mongoengine.panels.MongoDebugPanel"]
#toolbar = DebugToolbarExtension(app)

from app import views, signIn, upload, run_algorithm
