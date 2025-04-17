from flask import Flask

from backend.db_connection import db
from backend.auth.auth_routes import auth
# from backend.users.user_routes import users # Removed old import
from backend.data_analyst.analyst_routes import analyst

# Import new blueprints
from backend.user_profile.profile_routes import user_profile_bp
from backend.user_resources.resource_routes import user_resources_bp
from backend.user_matching.matching_routes import user_matching_bp
from backend.user_groups.group_routes import user_groups_bp
from backend.test.test_routes import test
import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)

    # Load environment variables
    # This function reads all the values from inside
    # the .env file (in the parent folder) so they
    # are available in this file.  See the MySQL setup 
    # commands below to see how they're being used.
    load_dotenv()

    # secret key that will be used for securely signing the session 
    # cookie and can be used for any other security related needs by 
    # extensions or your application
    # app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # # these are for the DB object to be able to connect to MySQL. 
    # app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER').strip()
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD').strip()
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST').strip()
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT').strip())
    app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME').strip()  # Change this to your DB name

    # Initialize the database object with the settings above. 
    app.logger.info('current_app(): starting the database connection')
    db.init_app(app)


    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.logger.info('current_app(): registering blueprints with Flask app object.')   
    app.register_blueprint(auth)

    app.register_blueprint(analyst,     url_prefix='/a')

    # Register new blueprints
    # app.register_blueprint(user_profile_bp)   # Prefix is '/users' defined in blueprint
    app.register_blueprint(user_profile_bp, url_prefix='/users')
    app.register_blueprint(user_resources_bp) 
    app.register_blueprint(user_matching_bp)  
    app.register_blueprint(user_groups_bp, url_prefix='/groups')
    app.register_blueprint(test)

    # Don't forget to return the app object
    return app

