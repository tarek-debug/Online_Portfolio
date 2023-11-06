from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__, static_folder='../static')
app.config['MONGO_DBNAME'] = ['MONGO_DBNAME']
app.config['MONGO_URI'] = ['MONGO_URI']
app.secret_key = ['MONGO_URI']

mongo = PyMongo(app, uri=app.config['MONGO_URI'])

from app.routes import home, login, logout, about_me, academic, personal, story_writing, exploring_the_outdoor, game_development, contact, image_attribution 

app.add_url_rule('/', view_func=home)
app.add_url_rule('/login', view_func=login, methods=['POST', 'GET'])
app.add_url_rule('/logout', view_func=logout, methods=['POST', 'GET'])
app.add_url_rule('/about_me', view_func=about_me)
app.add_url_rule('/academic', view_func=academic)
app.add_url_rule('/personal', view_func=personal)
app.add_url_rule('/story_writing', view_func=story_writing)
app.add_url_rule('/exploring_the_outdoor', view_func=exploring_the_outdoor)
app.add_url_rule('/game_development', view_func=game_development)
app.add_url_rule('/contact', view_func=contact)
app.add_url_rule('/image_attribution', view_func=image_attribution)

# Register the edit_pages blueprint
from app.edit_pages import edit_pages
app.register_blueprint(edit_pages)

if __name__ == '__main__':
    app.run(debug=True)
