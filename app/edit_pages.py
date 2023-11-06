import json
import os
from urllib.parse import urlparse
from flask import Blueprint, request, render_template, url_for, Markup, send_file
from flask_pymongo import PyMongo
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from app import app
from flask import jsonify
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from gridfs import GridFS
import base64
import io
from bson.binary import Binary
edit_pages = Blueprint('edit_pages', __name__)
mongo = PyMongo(app)
fs = GridFS(mongo.db)
from flask import request, jsonify
import json
import os
from werkzeug.utils import secure_filename
@app.route('/add_or_update_sentence', methods=['POST'])
def add_or_update_sentence():
    new_sentence = request.form.get('sentence')
    # Logic to add or update the sentence in your MongoDB collection
    mongo.db.home_page.insert_one({'sentence': new_sentence})
    return jsonify(success=True)

@app.route('/delete_sentence', methods=['POST'])
def delete_sentence():
    sentence_to_delete = request.json['sentence']

    # Delete the sentence from the database
    result = mongo.db.home_page.delete_one({'sentence': sentence_to_delete})

    if result.deleted_count > 0:
        return jsonify(success=True)
    else:
        return jsonify(success=False)


# Route to add a bar
@app.route('/add_bar', methods=['POST'])
def add_bar():
    bar_data = request.json
    mongo.db.home_circular_barplot.insert_one(bar_data)
    return jsonify({'status': 'success'})


@app.route('/edit_bar', methods=['POST'])
def edit_bar():
    category = request.json['Category']
    value = request.json['Value']
    inner_value = request.json['InnerValue']
    mongo.db.home_circular_barplot.update_one({"Category": category}, {"$set": {"Value": value, "InnerValue": inner_value}})
    print(category)
    print(value)
    print(inner_value)
    
    return jsonify({"status": "success"})

@app.route('/remove_bar', methods=['POST'])
def remove_bar():
    category = request.json['Category']
    mongo.db.home_circular_barplot.delete_one({"Category": category})
    return jsonify({"status": "success"})


@edit_pages.route('/edit_about', methods=['POST'])
def edit_about():
    # Retrieve all the form fields
    about_me_title = request.form.get('about_me_title')
    about_text_title = request.form.get('about_text_title')
    about_me_intro = request.form.get('about_me_intro')
    technical_skills = request.form.get('technical_skills')
    softwares = request.form.get('softwares')
    softwares_text = request.form.get('softwares_text')
    coding_lang = request.form.get('coding_lang')
    coding_lang_text = request.form.get('coding_lang_text')
    frameworks = request.form.get('frameworks')
    frameworks_text = request.form.get('frameworks_text')
    experience = request.form.get('experience')
    experience_table_title = request.form.get('experience_table_title')
    count_1 = request.form.get('count_1')
    exp_1 = request.form.get('exp_1')
    count_2 = request.form.get('count_2')
    exp_2 = request.form.get('exp_2')
    count_3 = request.form.get('count_3')
    exp_3 = request.form.get('exp_3')
    aspirations = request.form.get('aspirations')
    asp1 = request.form.get('asp1')
    asp2 = request.form.get('asp2')
    asp3 = request.form.get('asp3')
    asp4 = request.form.get('asp4')
    photo_data = request.form.get('profile_photo')
    # Create a filter to identify the document
    filter = {'_id': ObjectId('6499aafb464debafe52af92d')}  # You need to specify the filter criteria to update the correct document

    # Update the document using the specified filter and form fields
    mongo.db.about_me_page.update_one(
        filter,
        {
            '$set': {
                'about_me_title': about_me_title,
                'about_text_title': about_text_title,
                'about_me_intro': about_me_intro,
                'about_me_content.0.0': technical_skills,
                'about_me_content.0.1.0': softwares,
                'about_me_content.0.1.1': softwares_text,
                'about_me_content.0.2.0': coding_lang,
                'about_me_content.0.2.1': coding_lang_text,
                'about_me_content.0.3.0': frameworks,
                'about_me_content.0.3.1': frameworks_text,
                'about_me_content.2.0': experience,
                'about_me_content.2.1': experience_table_title,
                'about_me_content.2.2.0': count_1,
                'about_me_content.2.2.1': exp_1,
                'about_me_content.2.3.0': count_2,
                'about_me_content.2.3.1': exp_2,
                'about_me_content.2.4.0': count_3,
                'about_me_content.2.4.1': exp_3,
                'about_me_content.3.0': aspirations,
                'about_me_content.3.1': asp1,
                'about_me_content.3.2': asp2,
                'about_me_content.3.3': asp3,
                'about_me_content.3.4': asp4,
                'profile_photo': photo_data,
            }
        },
        upsert=True
    )
    
    return 'About me data updated successfully!'




@edit_pages.route('/edit_about_me_photo', methods=['POST'])
def edit_about_me_photo():
    # Retrieve the photo data from the request
    photo_file = request.files['profile_photo']
    
    # Create the image folder if it doesn't exist
    image_folder = 'static/img'
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # Secure the filename and save the file to the server
    filename = secure_filename('profile_photo.' + photo_file.filename.split('.')[-1])
    image_path = os.path.join(image_folder, filename)
    photo_file.save(image_path)

    # Update the database with the new photo path (if necessary)
    filter = {'_id': ObjectId('64a09cee4df65a0ffc1e996c')}
    mongo.db.about_me_page.update_one(
        filter,
        {
            '$set': {
                'profile_photo_path': '/' + image_path
            }
        }
    )

    # Return the new photo path to the client
    return jsonify({'newPath': '/' + image_path})


@edit_pages.route('/edit_resume', methods=['POST'])
def edit_resume():
    # Retrieve the resume data from the request
    resume_data = request.form['resumeData'].split(',')[1]  # Remove "data:application/pdf;base64," prefix

    # Convert the base64 data to binary
    resume_data_binary = base64.b64decode(resume_data)

    # Create a filter to identify the document
    filter = {'_id': ObjectId('64a0b1e24df65a0ffc1e996d')}

    # Update the document using the specified filter and resume data
    mongo.db.about_me_page.update_one(
        filter,
        {
            '$set': {
                'resume': {
                    'data': resume_data_binary,
                    'mimetype': 'application/pdf'  # Change the mimetype if needed
                }
            }
        }
    )

    return 'Resume updated successfully!'


from flask import make_response

@edit_pages.route('/download_resume', methods=['GET'])
def download_resume():
    # Retrieve the resume data from MongoDB
    resume_document = mongo.db.about_me_page.find_one({'_id': ObjectId('64a0b1e24df65a0ffc1e996d')})
    resume_data = resume_document['resume']['data']

    # Create a file-like object from the resume data
    resume_file = io.BytesIO(resume_data)

    # Create a response object
    response = make_response(resume_file.getvalue())

    # Set the headers
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment', filename='resume.pdf')

    return response







@app.route('/edit_academic_table', methods=['POST'])
def edit_academic_table():
    table_data = json.loads(request.form['tableData'])
    image_folder = 'static/img'
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    collection = mongo.db['academic_projects_table']
    collection.delete_many({})
    original_image_paths = json.loads(request.form['originalImagePaths'])
    
    # Store the new image paths
    new_image_paths = []
    
    for row in table_data:
        name = row['Name']
        image_key = 'image-' + name
        image_file = request.files.get(image_key)
        original_image_path = original_image_paths.get(name)
        if image_file:
            filename = secure_filename(name + "_academic_projects_image." + image_file.filename.split('.')[-1])
            image_path = os.path.join(image_folder, filename)
            image_file.save(image_path)
            row['Image preview'] = '/' + image_path
            # Append the new image path
            new_image_paths.append(image_path)
        elif original_image_path:
            row['Image preview'] = original_image_path
            # Append the original image path if not updated
            new_image_paths.append(original_image_path[1:])
        collection.insert_one(row)
    
    # Delete images that are no longer needed
    for original_image_path in original_image_paths.values():
        if original_image_path[1:] not in new_image_paths:
            try:
                os.remove(original_image_path[1:])
            except FileNotFoundError:
                pass # The file might not exist, so we can simply ignore the error
    
    return jsonify({'message': 'Changes saved successfully'})



@app.route('/edit_personal_table', methods=['POST'])
def edit_personal_table():
    table_data = json.loads(request.form['tableData'])
    image_folder = 'static/img'
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    collection = mongo.db['personal_projects_table']
    collection.delete_many({})
    original_image_paths = json.loads(request.form['originalImagePaths'])
    
    # Store the new image paths
    new_image_paths = []
    
    for row in table_data:
        name = row['Name']
        image_key = 'image-' + name
        image_file = request.files.get(image_key)
        original_image_path = original_image_paths.get(name)
        if image_file:
            filename = secure_filename(name + "_personal_project_image." + image_file.filename.split('.')[-1])
            image_path = os.path.join(image_folder, filename)
            image_file.save(image_path)
            row['Image preview'] = '/' + image_path
            # Append the new image path
            new_image_paths.append(image_path)
        elif original_image_path:
            row['Image preview'] = original_image_path
            # Append the original image path if not updated
            new_image_paths.append(original_image_path[1:])
        collection.insert_one(row)
    
    # Delete images that are no longer needed
    for original_image_path in original_image_paths.values():
        if original_image_path[1:] not in new_image_paths:
            try:
                os.remove(original_image_path[1:])
            except FileNotFoundError:
                pass # The file might not exist, so we can simply ignore the error
    
    return jsonify({'message': 'Changes saved successfully'})


@app.route('/edit_story_writing_table', methods=['POST'])
def edit_story_writing_table():
    table_data = json.loads(request.form['tableData'])
    image_folder = 'static/img'
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    collection = mongo.db['story_writing_table']
    collection.delete_many({})
    original_image_paths = json.loads(request.form['originalImagePaths'])
    
    # Store the new image paths
    new_image_paths = []
    
    for row in table_data:
        name = row['Title']
        image_key = 'image-' + name
        image_file = request.files.get(image_key)
        original_image_path = original_image_paths.get(name)
        if image_file:
            filename = secure_filename(name + "_story_image." + image_file.filename.split('.')[-1])
            image_path = os.path.join(image_folder, filename)
            image_file.save(image_path)
            row['Image'] = '/' + image_path
            # Append the new image path
            new_image_paths.append(image_path)
        elif original_image_path:
            row['Image'] = original_image_path
            # Append the original image path if not updated
            new_image_paths.append(original_image_path[1:])
        collection.insert_one(row)
    
    # Delete images that are no longer needed
    for original_image_path in original_image_paths.values():
        if original_image_path[1:] not in new_image_paths:
            try:
                os.remove(original_image_path[1:])
            except FileNotFoundError:
                pass # The file might not exist, so we can simply ignore the error
    
    return jsonify({'message': 'Changes saved successfully'})



@app.route('/edit_game_dev_table', methods=['POST'])
def edit_game_dev_table():
    table_data = json.loads(request.form['tableData'])
    image_folder = 'static/img'
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    collection = mongo.db['game_dev_table']
    collection.delete_many({})
    original_image_paths = json.loads(request.form['originalImagePaths'])
    
    # Store the new image paths
    new_image_paths = []
    
    for row in table_data:
        name = row['Name']
        image_key = 'image-' + name
        image_file = request.files.get(image_key)
        original_image_path = original_image_paths.get(name)
        if image_file:
            filename = secure_filename(name + "_game_image." + image_file.filename.split('.')[-1])
            image_path = os.path.join(image_folder, filename)
            image_file.save(image_path)
            row['Image preview'] = '/' + image_path
            # Append the new image path
            new_image_paths.append(image_path)
        elif original_image_path:
            row['Image preview'] = original_image_path
            # Append the original image path if not updated
            new_image_paths.append(original_image_path[1:])
        collection.insert_one(row)
    
    # Delete images that are no longer needed
    for original_image_path in original_image_paths.values():
        if original_image_path[1:] not in new_image_paths:
            try:
                os.remove(original_image_path[1:])
            except FileNotFoundError:
                pass # The file might not exist, so we can simply ignore the error
    
    return jsonify({'message': 'Changes saved successfully'})



@edit_pages.route('/edit_home', methods=['POST', 'GET'])
def edit_home():
    home_text = request.form.get('home_text')
    # Update the home page text in the database
    mongo.db.home_page.update_one({}, {'$set': {'text': home_text}}, upsert=True)
    return 'Home page text updated successfully!'





@edit_pages.route('/new_contact', methods=['POST'])
def new_contact():
    # Get the type, value, and image from the form data
    contact_type = request.form.get('type')
    contact_value = request.form.get('value')
    contact_image_file = request.files['image']
    
    # Create the image folder if it doesn't exist
    image_folder = 'static/img/contact_images'
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # Secure the filename and save the file to the server
    filename = secure_filename('contact_image_' + contact_image_file.filename)
    image_path = os.path.join(image_folder, filename)
    contact_image_file.save(image_path)

    # Construct the new contact with the path to the image
    new_contact = {
        'type': contact_type,
        'value': contact_value,
        'image_path': '/' + image_path
    }

    # Insert the new contact into the database
    mongo.db.contacts.insert_one(new_contact)

    return jsonify(success=True, message='Contact added successfully!')

@app.route('/delete_contact', methods=['POST'])
def delete_contact():
    contact_data = request.json
    type = contact_data['type']
    value = contact_data['value']
    print(type)
    print(value)
    # Delete the contact based on the type and value
    # Assuming you have a field named 'value' in your documents
    mongo.db.contacts.delete_one({'type': type, 'value': value})

    return jsonify({'status': 'success'})

@edit_pages.route('/edit_personal_projects', methods=['POST', 'GET'])
def edit_personal_projects():
    personal_projects_text = request.form.get('personal_projects_text')
    # Update the personal projects main page text in the database
    mongo.db.personal_projects_main_page.update_one({}, {'$set': {'text': personal_projects_text}}, upsert=True)
    return 'Personal projects main page text updated successfully!'

@edit_pages.route('/edit_academic_page_text', methods=['POST', 'GET'])
def edit_academic_projects():
    
    academic_main_title = request.form.get('academic_main_title')
    academic_projects_introduction=request.form.get('academic_projects_introduction')
    print(academic_main_title)
    print(academic_projects_introduction)
    # Update the academic projects main page text in the database
    filter = {'_id': ObjectId('64a1c451b8eedcc8f01f326e')}  # You need to specify the filter criteria to update the correct document
    # Update the document using the specified filter and form fields
    mongo.db.academic_projects_main_page.update_one(
        filter,
        {
            '$set': {
                'academic_main_title': academic_main_title,
                'academic_projects_introduction': academic_projects_introduction,
            }
        },
        upsert=True
    )

    return 'Academic projects main page text updated successfully!'

@edit_pages.route('/edit_personal_projects_page_text', methods=['POST', 'GET'])
def edit_personal_projects_page_text():
    
    personal_projects_main_title = request.form.get('personal_projects_main_title')
    personal_projects_main_intro=request.form.get('personal_projects_main_intro')
    print(personal_projects_main_title)
    print(personal_projects_main_intro)
    # Update the academic projects main page text in the database
    filter = {'_id': ObjectId('64a787e80af6a3f5c9492507')}  # You need to specify the filter criteria to update the correct document
    # Update the document using the specified filter and form fields
    mongo.db.personal_projects_main_page.update_one(
        filter,
        {
            '$set': {
                'personal_projects_main_title': personal_projects_main_title,
                'personal_projects_main_intro': personal_projects_main_intro,
            }
        },
        upsert=True
    )

    return 'Personal projects main page text updated successfully!'


@edit_pages.route('/edit_game_dev_page_text', methods=['POST', 'GET'])
def edit_game_dev_page_text():
    game_dev_main_title=request.form.get('game_dev_main_title')
    game_dev_main_intro=request.form.get('game_dev_main_intro')
    print(game_dev_main_title)
    print(game_dev_main_intro)
    # Update the academic projects main page text in the database
    filter = {'_id': ObjectId('64a788e90af6a3f5c949250a')}  # You need to specify the filter criteria to update the correct document
    # Update the document using the specified filter and form fields
    mongo.db.game_dev_main_page.update_one(
        filter,
        {
            '$set': {
                'game_dev_main_title': game_dev_main_title,
                'game_dev_main_intro': game_dev_main_intro,
            }
        },
        upsert=True
    )
    return 'Game development main page text updated successfully!'

@edit_pages.route('/edit_outdoor_page_text', methods=['POST', 'GET'])
def edit_outdoor_page_text():
    
    outdoor_title = request.form.get('outdoor_title')
    outdoor_introduction=request.form.get('outdoor_introduction')
    map_title=request.form.get('map_title')
    print(outdoor_title)
    print(outdoor_introduction)
    # Update the academic projects main page text in the database
    filter = {'_id': ObjectId('64a788640af6a3f5c9492509')}  # You need to specify the filter criteria to update the correct document
    # Update the document using the specified filter and form fields
    mongo.db.exploring_the_outdoor_page.update_one(
        filter,
        {
            '$set': {
                'outdoor_title': outdoor_title,
                'outdoor_introduction': outdoor_introduction,
                'map_title': map_title,
            }
        },
        upsert=True
    )

    return 'Outdoor main page text updated successfully!'



@edit_pages.route('/edit_stories_main_page_text', methods=['POST', 'GET'])
def edit_stories_main_page_text():
    story_writing_main_title = request.form.get('story_writing_main_title')
    story_writing_main_intro=request.form.get('story_writing_main_intro')
    print(story_writing_main_title)
    print(story_writing_main_intro)
    # Update the academic projects main page text in the database
    filter = {'_id': ObjectId('64a7882a0af6a3f5c9492508')}  # You need to specify the filter criteria to update the correct document
    # Update the document using the specified filter and form fields
    mongo.db.story_writing_main_page.update_one(
        filter,
        {
            '$set': {
                'story_writing_main_title': story_writing_main_title,
                'story_writing_main_intro': story_writing_main_intro,
            }
        },
        upsert=True
    )
    return 'Stories page text updated successfully!'
@edit_pages.route('/handle_map_marker', methods=['POST'])
def handle_map_marker():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    name=data.get('name')
    action = data.get('action')
    print('hello')
    print(action)
    print(latitude)
    print(longitude)
    map_coordinates = mongo.db.map_coordinates
    if action == 'addHikedPlace':
        # Add hiked place logic
        map_coordinates.insert_one({
            "type": "hiked place",
            "name": name,
            "Longitude": longitude,
            "Latitude": latitude
        })
    elif action == 'removeHikedPlace':
        # Remove hiked place logic
        map_coordinates.delete_one({
            "type": "hiked place",
            "Longitude": longitude,
            "Latitude": latitude
        })
    elif action == 'addPlaceToHike':
        # Add place to hike logic
        map_coordinates.insert_one({
            "type": "place to hike",
            "name": name,
            "Longitude": longitude,
            "Latitude": latitude
        })
    elif action == 'removePlaceToHike':
        # Remove place to hike logic
        map_coordinates.delete_one({
            "type": "place to hike",
            "Longitude": longitude,
            "Latitude": latitude
        })

    # Return a response
    return jsonify({"status": "success"})

@edit_pages.route('/edit_img_attrib_table', methods=['POST', 'GET'])
def edit_img_attrib_table():
    table_data = json.loads(request.form['tableData'])
    # Create the image folder if it doesn't exist
    image_folder = 'static/img/image_attributions'
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    collection = mongo.db['image_attribution_table']
    collection.delete_many({})
    original_image_paths = json.loads(request.form['originalImagePaths'])
    
    # Store the new image paths
    new_image_paths = []
    
    for row in table_data:
        name = row['Image Name']
        image_key = 'image-' + name
        image_file = request.files.get(image_key)
        original_image_path = original_image_paths.get(name)
        if image_file:
            filename = secure_filename(name + "_image." + image_file.filename.split('.')[-1])
            image_path = os.path.join(image_folder, filename)
            image_file.save(image_path)
            row['Image'] = '/' + image_path
            # Append the new image path
            new_image_paths.append(image_path)
        elif original_image_path:
            row['Image'] = original_image_path
            # Append the original image path if not updated
            new_image_paths.append(original_image_path[1:])
        collection.insert_one(row)
    
    # Delete images that are no longer needed
    for original_image_path in original_image_paths.values():
        if original_image_path[1:] not in new_image_paths:
            try:
                os.remove(original_image_path[1:])
            except FileNotFoundError:
                pass # The file might not exist, so we can simply ignore the error
    
    return jsonify({'message': 'Changes saved successfully'})


def sanitize_url(url):
    """
    Ensures that the URL starts with http:// or https:// and does not contain any JavaScript.
    """
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ['http', 'https']:
        return "http://" + url
    return url

@edit_pages.route('/edit_academic_projects_pages', methods=['POST', 'GET'])
def edit_academic_projects_pages():
    academic_projects_pages_text = request.form.get('academic_projects_pages_text')
    # Update the academic projects pages text in the database
    mongo.db.academic_projects_pages.update_one({}, {'$set': {'text': academic_projects_pages_text}}, upsert=True)
    return 'Academic projects pages text updated successfully!'

@edit_pages.route('/edit_personal_projects_pages', methods=['POST', 'GET'])
def edit_personal_projects_pages():
    personal_projects_pages_text = request.form.get('personal_projects_pages_text')
    # Update the personal projects pages text in the database
    mongo.db.personal_projects_pages.update_one({}, {'$set': {'text': personal_projects_pages_text}}, upsert=True)
    return 'Personal projects pages text updated successfully!'

@edit_pages.route('/edit_game_dev_main_pages', methods=['POST', 'GET'])
def edit_game_dev_main_pages():
    game_dev_main_pages_text = request.form.get('game_dev_main_pages_text')
    # Update the game development main pages text in the database
    mongo.db.game_dev_main_pages.update_one({}, {'$set': {'text': game_dev_main_pages_text}}, upsert=True)
    return 'Game development main pages text updated successfully!'

@edit_pages.route('/edit_games_pages', methods=['POST', 'GET'])
def edit_games_pages():
    games_pages_text = request.form.get('games_pages_text')
    # Update the games pages text in the database
    mongo.db.games_pages.update_one({}, {'$set': {'text': games_pages_text}}, upsert=True)
    return 'Games pages text updated successfully!'
