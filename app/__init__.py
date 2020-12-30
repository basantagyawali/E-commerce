from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os

# getting current folder location
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# configuration
app.config.from_object(Config)

#database initialize
db = SQLAlchemy(app)

#for the different update in the database
migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        ''' it is done beacaue if the drop column doesnot work in sqlite
        and if not work then delete migration and reintialize it  '''
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "customers.customerLogin"

# for the images configuration
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

from .products import bp as products_blueprint
app.register_blueprint(products_blueprint)

from .admin import bp as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix="/admin")

from .customers import bp as customers_blueprint
app.register_blueprint(customers_blueprint, url_prefix='/customer')

from .carts import bp as carts_blueprint
app.register_blueprint(carts_blueprint)

from .error  import bp as error_blueprint
app.register_blueprint(error_blueprint)

