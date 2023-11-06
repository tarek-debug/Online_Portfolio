from flask import render_template, url_for, request, session, redirect, render_template
from app import app, mongo
from flask_pymongo import PyMongo
import bcrypt
from bson.objectid import ObjectId
from gridfs import GridFS
import base64
from flask import redirect, url_for, render_template, abort
from base64 import b64encode
from flask import jsonify

app.config['MONGO_DBNAME'] = ['MONGO_DBNAME'] 
app.config['MONGO_URI'] = ['MONGO_URI'] 

mongo = PyMongo(app, uri=app.config['MONGO_URI'])
app.secret_key = [app.secret_key]
fs = GridFS(mongo.db)

@app.route('/')
def home():
    logged_in = 'username' in session
    view_mode = request.args.get('view_mode')
    # Redirect to the guest view if 'admin=view' is not present
    if not logged_in and view_mode != 'guest':
        return redirect(url_for('home', view_mode='guest'))
    return render_template('home.html', logged_in=logged_in, view_mode=view_mode)

@app.route('/get_sentences')
def get_sentences():
    sentences_collection = mongo.db.home_page.find({})
    sentences = [item['sentence'] for item in sentences_collection]
    return jsonify(sentences=sentences)

@app.route('/get_circular_data')
def get_circular_data():
    collection = mongo.db.home_circular_barplot.find({})
    data = []
    for item in collection:
        # Remove the '_id' field from each item
        item.pop('_id', None)
        data.append(item)
    print (data)
    return jsonify(data)

@app.route('/get_projects')
def get_projects():
     # Connect to your MongoDB
    db = mongo.db
    # Connect to your MongoDB

    # Retrieve data from your tables
    project_data = {
        "Machine Learning": [],
        "Cybersecurity": [],
        "Database Development": [],
        "Game Development": [],
        "Story Writing": [],
    }

    # Academic and Personal Projects
    for collection_name in ['academic_projects_table', 'personal_projects_table']:
        collection = db[collection_name]
        for doc in collection.find():
            category = doc['Category']
            if category in ["Machine Learning", "Cybersecurity", "Database Development"]:
                project_data[category].append({
                    'title': doc['Name'],
                    'description': doc['Description'],
                    'detailsURL': doc['Source Code'],
                    'imagePath': doc['Image preview']
           
                })

    # Game Development
    game_dev_collection = db['game_dev_table']
    for doc in game_dev_collection.find():
        project_data["Game Development"].append({
            'title': doc['Name'],
            'description': doc['Description'],
            'detailsURL': doc['Source Code'],
            'imagePath': doc['Image preview']

        })

    # Story Writing
    story_writing_collection = db['story_writing_table']
    for doc in story_writing_collection.find():
        project_data["Story Writing"].append({
            'title': doc['Title'],
            'description': doc['Description'],
            'detailsURL': doc['Link to Story'],
            'imagePath': doc['Image']
        })
    # Return the data as JSON
    return jsonify(project_data)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'name': request.form['username']})
        if login_user:
            if bcrypt.checkpw(request.form['pass'].encode('utf-8'), login_user['password']):
                session['username'] = request.form['username']
                return redirect(url_for('home'))

        return 'Invalid username/password combination'

    return render_template('login.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))

@app.route('/about_me')
def about_me():
    logged_in = 'username' in session
    view_mode = request.args.get('view_mode')

    if not logged_in and view_mode != 'guest':
        return redirect(url_for('about_me', view_mode='guest'))

    # Retrieve the about_data from the database
    about_me_data = mongo.db.about_me_page.find_one({'_id': ObjectId('64a09cee4df65a0ffc1e996c')})
    profile_photo = about_me_data.get('profile_photo_path') if about_me_data else ''


    # Retrieve the about_data from the database
    about_me_data = mongo.db.about_me_page.find_one({'_id': ObjectId('6499aafb464debafe52af92d')})

    # Define the keys and default values to retrieve from about_me_data
    data_keys = {
        'about_me_title': '',
        'about_text_title': '',
        'about_me_intro': '',
        'about_me_content': [],

    }

    # Retrieve the values from about_me_data using the keys
    data_values = {key: about_me_data.get(key, default_value) for key, default_value in data_keys.items()}

    # Unpack the values
    about_me_title, about_text_title, about_me_intro, about_me_content = data_values.values()

    # Retrieve the specific values from the nested structure
    technical_skills = about_me_content[0][0] if about_me_content else ''
    softwares = about_me_content[0][1][0] if about_me_content else ''
    softwares_text = about_me_content[0][1][1] if about_me_content else ''
    coding_lang = about_me_content[0][2][0] if about_me_content else ''
    coding_lang_text = about_me_content[0][2][1] if about_me_content else ''
    frameworks = about_me_content[0][3][0] if about_me_content else ''
    frameworks_text = about_me_content[0][3][1] if about_me_content else ''
    leadership_skills= about_me_content[1][0] if about_me_content else ''
    quest_leader= about_me_content[1][1][0] if about_me_content else ''
    quest_description= about_me_content[1][1][1] if about_me_content else ''
    resident_advisor= about_me_content[1][2][0] if about_me_content else ''
    resident_advisor_description= about_me_content[1][2][1] if about_me_content else ''
    experience = about_me_content[2][0] if about_me_content else ''
    experience_table_title = about_me_content[2][1] if about_me_content else ''
    count_1 = about_me_content[2][2][0] if about_me_content else ''
    exp_1 = about_me_content[2][2][1] if about_me_content else ''
    count_2 = about_me_content[2][3][0] if about_me_content else ''
    exp_2 = about_me_content[2][3][1] if about_me_content else ''
    count_3 = about_me_content[2][4][0] if about_me_content else ''
    exp_3 = about_me_content[2][4][1] if about_me_content else ''
    aspirations = about_me_content[3][0] if about_me_content else ''
    asp1 = about_me_content[3][1] if about_me_content else ''
    asp2 = about_me_content[3][2] if about_me_content else ''
    asp3 = about_me_content[3][3] if about_me_content else ''
    asp4 = about_me_content[3][4] if about_me_content else ''


    return render_template('about_me.html', logged_in=logged_in, view_mode=view_mode, about_me_title=about_me_title,
                           about_text_title=about_text_title, about_me_intro=about_me_intro, profile_photo= profile_photo,
                           technical_skills=technical_skills, softwares=softwares, softwares_text=softwares_text,
                           coding_lang=coding_lang, coding_lang_text=coding_lang_text, frameworks=frameworks,
                           frameworks_text=frameworks_text, leadership_skills= leadership_skills , quest_leader=quest_leader,
                            quest_description=quest_description, resident_advisor=resident_advisor,
                            resident_advisor_description=resident_advisor_description,
                             experience=experience, experience_table_title=experience_table_title,
                           count_1=count_1, exp_1=exp_1, count_2=count_2, exp_2=exp_2, count_3=count_3, exp_3=exp_3,
                           aspirations=aspirations, asp1=asp1, asp2=asp2, asp3=asp3, asp4=asp4)

@app.route('/academic')
def academic():
    logged_in = 'username' in session
    view_mode = request.args.get('view_mode')

    if not logged_in and view_mode != 'guest':
        return redirect(url_for('home', view_mode='guest'))

    # Fetch the documents from the MongoDB collection
    documents = list(mongo.db.academic_projects_table.find())

    academic_page_text = mongo.db.academic_projects_main_page.find_one({'_id': ObjectId('64a1c451b8eedcc8f01f326e')})
    academic_main_title = academic_page_text['academic_main_title'] if academic_page_text else ' Empty'
    academic_projects_introduction = academic_page_text['academic_projects_introduction']  if academic_page_text else ' Empty'

    return render_template('academic.html', logged_in=logged_in, view_mode=view_mode, documents=documents,
                           academic_main_title=academic_main_title, academic_projects_introduction=academic_projects_introduction)





@app.route('/personal')
def personal():
    logged_in = 'username' in session
    view_mode = request.args.get('view_mode')

    if not logged_in and view_mode != 'guest':
        return redirect(url_for('personal', view_mode='guest'))

    # Fetch the documents from the MongoDB collection
    documents = list(mongo.db.personal_projects_table.find())

    personal_projects_text= mongo.db.personal_projects_main_page.find_one({'_id': ObjectId('64a787e80af6a3f5c9492507')})
    personal_projects_main_title= personal_projects_text['personal_projects_main_title'] if personal_projects_text else ' Empty'
    personal_projects_main_intro= personal_projects_text['personal_projects_main_intro'] if personal_projects_text else ' Empty'

    return render_template('personal.html', logged_in=logged_in, view_mode=view_mode, documents=documents ,
                           personal_projects_main_title=personal_projects_main_title, personal_projects_main_intro=personal_projects_main_intro)




@app.route('/story_writing')
def story_writing():
    logged_in = 'username' in session
    view_mode = request.args.get('view_mode')

    if not logged_in and view_mode != 'guest':
        return redirect(url_for('story_writing', view_mode='guest'))
    # Fetch the documents from the MongoDB collection
    documents = list(mongo.db.story_writing_table.find())

    story_writing_main_text= mongo.db.story_writing_main_page.find_one({'_id': ObjectId('64a7882a0af6a3f5c9492508')})
    story_writing_main_title= story_writing_main_text['story_writing_main_title'] if story_writing_main_text else ' Empty'
    story_writing_main_intro= story_writing_main_text['story_writing_main_intro'] if story_writing_main_text else ' Empty'
    return render_template('story_writing.html', logged_in=logged_in, view_mode=view_mode, documents=documents, 
                           story_writing_main_title=story_writing_main_title, story_writing_main_intro=story_writing_main_intro)


@app.route('/exploring_the_outdoor')
def exploring_the_outdoor():
    logged_in = 'username' in session
    view_mode = request.args.get('view_mode')

    if not logged_in and view_mode != 'guest':
        return redirect(url_for('exploring_the_outdoor', view_mode='guest'))

    # Fetch the documents from the MongoDB collection
    outdoor_page_text= mongo.db.exploring_the_outdoor_page.find_one({'_id': ObjectId('64a788640af6a3f5c9492509')})
    outdoor_title= outdoor_page_text['outdoor_title'] if outdoor_page_text else ' Empty'
    outdoor_introduction= outdoor_page_text['outdoor_introduction'] if outdoor_page_text else ' Empty'
    map_title= outdoor_page_text['map_title'] if outdoor_page_text else ' Empty'
    
    # Fetch the coordinates data from MongoDB
    map_coordinates = mongo.db.map_coordinates.find()
    hiked_locations = []
    desired_hike_locations = []
    for coord in map_coordinates:
        location_data = {
            'name': coord['name'], # assuming you have no specific name for the locations
            'coordinates': [coord['Longitude'], coord['Latitude']]
        }
        if coord['type'] == 'hiked place':
            hiked_locations.append(location_data)
        else:
            desired_hike_locations.append(location_data)

    return render_template('exploring_the_outdoor.html', logged_in=logged_in, view_mode=view_mode,
                           outdoor_title=outdoor_title, outdoor_introduction=outdoor_introduction,
                           map_title=map_title, hiked_locations=hiked_locations,
                           desired_hike_locations=desired_hike_locations)


@app.route('/game_development')
def game_development():
    logged_in = 'username' in session
    view_mode = request.args.get('view_mode')
    if not logged_in and view_mode != 'guest':
        return redirect(url_for('game_development', view_mode='guest'))
    # Fetch the documents from the MongoDB collection
    documents = list(mongo.db.game_dev_table.find())

    game_dev_page_text= mongo.db.game_dev_main_page.find_one({'_id': ObjectId('64a788e90af6a3f5c949250a')})
    game_dev_main_title= game_dev_page_text['game_dev_main_title'] if game_dev_page_text else ' Empty'
    game_dev_main_intro= game_dev_page_text['game_dev_main_intro'] if game_dev_page_text else ' Empty'


    return render_template('game_development.html', logged_in=logged_in, view_mode=view_mode, documents=documents, 
                           game_dev_main_title=game_dev_main_title, game_dev_main_intro=game_dev_main_intro)


@app.route('/contact')
def contact():
    logged_in = 'username' in session
    view_mode = request.args.get('view_mode')

    if not logged_in and view_mode != 'guest':
        return redirect(url_for('contact', view_mode='guest'))
    
    contacts = list(mongo.db.contacts.find({}))
    # No need to encode the images, as they are already base64 encoded strings

    return render_template('contact.html', logged_in=logged_in, view_mode=view_mode, contacts=contacts)

@app.route('/image_attribution')
def image_attribution():
    logged_in = 'username' in session
    view_mode = request.args.get('view_mode')

    if not logged_in and view_mode != 'guest':
        return redirect(url_for('image_attribution', view_mode='guest'))
    # Fetch the documents from the MongoDB collection
    documents = list(mongo.db.image_attribution_table.find())


    return render_template('image_attribution.html', logged_in=logged_in, view_mode=view_mode, documents=documents)


if __name__ == '__main__':
    app.run(debug=True)
