from flask import Flask
from flask_cors import CORS
from backend.db_connection import db
from backend.user.user_routes import user
from backend.data_analyst.analyst_routes import analyst

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(user, url_prefix='/u')
app.register_blueprint(analyst, url_prefix='/a')

@app.route('/')
def hello():
    return 'StudyBuddy API is running!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000) 