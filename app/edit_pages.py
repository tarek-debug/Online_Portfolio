# app/edit_pages.py

import os
import io
import json
import base64
from urllib.parse import urlparse
from bson.objectid import ObjectId
from flask import (
    Blueprint, request, jsonify, send_file, abort
)
from werkzeug.utils import secure_filename
from gridfs import GridFS
from app.extensions import mongo

edit_pages = Blueprint('edit_pages', __name__)
fs = GridFS(mongo.db)


def _make_folder(path: str):
    os.makedirs(path, exist_ok=True)


def _build_update_dict(mappings: dict) -> dict:
    upd = {}
    for form_key, doc_key in mappings.items():
        val = request.form.get(form_key)
        if val is not None and val != '':
            upd[doc_key] = val
    return upd


def _edit_table(
    collection_name: str,
    table_field: str,
    original_paths_field: str,
    row_key: str,
    image_field: str,
    image_folder: str,
    filename_tpl: str
):
    table_data = json.loads(request.form[table_field])
    originals = json.loads(request.form.get(original_paths_field, '{}'))
    new_paths = []
    _make_folder(image_folder)
    coll = mongo.db[collection_name]
    coll.delete_many({})

    for row in table_data:
        key = row[row_key]
        file = request.files.get(f'image-{key}')
        orig = originals.get(key)
        if file:
            ext = file.filename.rsplit('.', 1)[-1]
            fname = secure_filename(filename_tpl.format(key=key, ext=ext))
            path = os.path.join(image_folder, fname)
            file.save(path)
            row[image_field] = '/' + path
            new_paths.append(path)
        elif orig:
            row[image_field] = orig
            new_paths.append(orig.lstrip('/'))
        coll.insert_one(row)

    for orig in originals.values():
        p = orig.lstrip('/')
        if p not in new_paths:
            try:
                os.remove(p)
            except FileNotFoundError:
                pass


@edit_pages.route('/add_or_update_sentence', methods=['POST'])
def add_or_update_sentence():
    sentence = request.form.get('sentence', '').strip()
    if sentence:
        mongo.db.home_page.insert_one({'sentence': sentence})
        return jsonify(success=True)
    return jsonify(success=False, error='Empty sentence'), 400


@edit_pages.route('/delete_sentence', methods=['POST'])
def delete_sentence():
    data = request.get_json() or {}
    sent = data.get('sentence')
    if not sent:
        return jsonify(success=False), 400
    res = mongo.db.home_page.delete_one({'sentence': sent})
    return jsonify(success=(res.deleted_count > 0))


@edit_pages.route('/add_bar', methods=['POST'])
def add_bar():
    data = request.get_json() or {}
    if 'Category' in data:
        mongo.db.home_circular_barplot.insert_one(data)
        return jsonify(status='success')
    return jsonify(status='error'), 400


@edit_pages.route('/edit_bar', methods=['POST'])
def edit_bar():
    data = request.get_json() or {}
    cat = data.get('Category')
    if not cat:
        return jsonify(status='error'), 400
    update = {k: data[k] for k in ('Value', 'InnerValue') if k in data}
    mongo.db.home_circular_barplot.update_one({'Category': cat}, {'$set': update})
    return jsonify(status='success')


@edit_pages.route('/remove_bar', methods=['POST'])
def remove_bar():
    data = request.get_json() or {}
    cat = data.get('Category')
    if not cat:
        return jsonify(status='error'), 400
    mongo.db.home_circular_barplot.delete_one({'Category': cat})
    return jsonify(status='success')


@edit_pages.route('/edit_about', methods=['POST'])
def edit_about():
    mappings = {
        'about_me_title':         'about_me_title',
        'about_text_title':       'about_text_title',
        'about_me_intro':         'about_me_intro',
        'technical_skills':       'about_me_content.0.0',
        'softwares':              'about_me_content.0.1.0',
        'softwares_text':         'about_me_content.0.1.1',
        'coding_lang':            'about_me_content.0.2.0',
        'coding_lang_text':       'about_me_content.0.2.1',
        'frameworks':             'about_me_content.0.3.0',
        'frameworks_text':        'about_me_content.0.3.1',
        'experience':             'about_me_content.2.0',
        'experience_table_title': 'about_me_content.2.1',
        'count_1':                'about_me_content.2.2.0',
        'exp_1':                  'about_me_content.2.2.1',
        'count_2':                'about_me_content.2.3.0',
        'exp_2':                  'about_me_content.2.3.1',
        'count_3':                'about_me_content.2.4.0',
        'exp_3':                  'about_me_content.2.4.1',
        'aspirations':            'about_me_content.3.0',
        'asp1':                   'about_me_content.3.1',
        'asp2':                   'about_me_content.3.2',
        'asp3':                   'about_me_content.3.3',
        'asp4':                   'about_me_content.3.4',
        'profile_photo':          'profile_photo_path'
    }
    upd = _build_update_dict(mappings)
    if upd:
        mongo.db.about_me_page.update_one(
            {'_id': ObjectId('6499aafb464debafe52af92d')},
            {'$set': upd}, upsert=True
        )
    return jsonify(success=True)


@edit_pages.route('/edit_about_me_photo', methods=['POST'])
def edit_about_me_photo():
    file = request.files.get('profile_photo')
    if not file:
        return jsonify(error='No file'), 400
    folder = 'static/img'
    _make_folder(folder)
    ext = file.filename.rsplit('.', 1)[-1]
    fname = secure_filename(f"profile_photo.{ext}")
    path = os.path.join(folder, fname)
    file.save(path)
    mongo.db.about_me_page.update_one(
        {'_id': ObjectId('64a09cee4df65a0ffc1e996c')},
        {'$set': {'profile_photo_path': '/' + path}}
    )
    return jsonify(newPath='/' + path)


@edit_pages.route('/edit_resume', methods=['POST'])
def edit_resume():
    data = request.form.get('resumeData', '')
    if not data.startswith('data:'):
        return jsonify(error='Invalid format'), 400
    b64 = data.split(',', 1)[1]
    binary = base64.b64decode(b64)
    fs.put(binary, filename='resume.pdf', content_type='application/pdf')
    return jsonify(success=True)


@edit_pages.route('/download_resume', methods=['GET'])
def download_resume():
    file = fs.find_one(sort=[('_id', -1)])
    if not file:
        abort(404)
    return send_file(
        io.BytesIO(file.read()),
        mimetype=file.content_type,
        as_attachment=True,
        attachment_filename=file.filename
    )


@edit_pages.route('/edit_academic_table', methods=['POST'])
def edit_academic_table():
    _edit_table(
        'academic_projects_table', 'tableData', 'originalImagePaths',
        'Name', 'Image preview', 'static/img',
        '{key}_academic.{ext}'
    )
    return jsonify(success=True)


def _single_field_update(mapping: dict, collection, filter: dict) -> bool:
    """
    Build a {"$set": {...}} only for form fields whose .strip() is non‐empty.
    Returns True if we actually did an update, False otherwise.
    """
    upd = {}
    for form_key, doc_key in mapping.items():
        val = request.form.get(form_key, '').strip()
        if val:
            upd[doc_key] = val
    if upd:
        collection.update_one(filter, {'$set': upd}, upsert=True)
        return True
    return False

@edit_pages.route('/edit_academic_page_text', methods=['POST', 'GET'])
def edit_academic_projects():
    mapping = {
        'academic_main_title':              'academic_main_title',
        'academic_projects_introduction':   'academic_projects_introduction',
    }
    filter = {'_id': ObjectId('64a1c451b8eedcc8f01f326e')}
    if _single_field_update(mapping, mongo.db.academic_projects_main_page, filter):
        return jsonify(success=True, message="Academic projects main page text updated successfully!")
    return jsonify(success=False, error="No non‐empty fields provided."), 400

@edit_pages.route('/edit_personal_projects_page_text', methods=['POST', 'GET'])
def edit_personal_projects_page_text():
    mapping = {
        'personal_projects_main_title': 'personal_projects_main_title',
        'personal_projects_main_intro': 'personal_projects_main_intro',
    }
    filter = {'_id': ObjectId('64a787e80af6a3f5c9492507')}
    if _single_field_update(mapping, mongo.db.personal_projects_main_page, filter):
        return jsonify(success=True, message="Personal projects page text updated successfully!")
    return jsonify(success=False, error="No non‐empty fields provided."), 400

@edit_pages.route('/edit_game_dev_page_text', methods=['POST', 'GET'])
def edit_game_dev_page_text():
    mapping = {
        'game_dev_main_title': 'game_dev_main_title',
        'game_dev_main_intro': 'game_dev_main_intro',
    }
    filter = {'_id': ObjectId('64a788e90af6a3f5c949250a')}
    if _single_field_update(mapping, mongo.db.game_dev_main_page, filter):
        return jsonify(success=True, message="Game development page text updated successfully!")
    return jsonify(success=False, error="No non‐empty fields provided."), 400

@edit_pages.route('/edit_outdoor_page_text', methods=['POST', 'GET'])
def edit_outdoor_page_text():
    mapping = {
        'outdoor_title':        'outdoor_title',
        'outdoor_introduction': 'outdoor_introduction',
        'map_title':            'map_title',
    }
    filter = {'_id': ObjectId('64a788640af6a3f5c9492509')}
    if _single_field_update(mapping, mongo.db.exploring_the_outdoor_page, filter):
        return jsonify(success=True, message="Outdoor page text updated successfully!")
    return jsonify(success=False, error="No non‐empty fields provided."), 400

@edit_pages.route('/edit_stories_main_page_text', methods=['POST', 'GET'])
def edit_stories_main_page_text():
    mapping = {
        'story_writing_main_title': 'story_writing_main_title',
        'story_writing_main_intro': 'story_writing_main_intro',
    }
    filter = {'_id': ObjectId('64a7882a0af6a3f5c9492508')}
    if _single_field_update(mapping, mongo.db.story_writing_main_page, filter):
        return jsonify(success=True, message="Stories page text updated successfully!")
    return jsonify(success=False, error="No non‐empty fields provided."), 400

@edit_pages.route('/edit_home', methods=['POST'])
def edit_home():
    text = request.form.get('home_text', '').strip()
    if text:
        mongo.db.home_page.update_one({}, {'$set': {'text': text}}, upsert=True)
        return jsonify(success=True)
    return jsonify(success=False, error="No content provided."), 400


@edit_pages.route('/new_contact', methods=['POST'])
def new_contact():
    t, v = request.form.get('type'), request.form.get('value')
    file = request.files.get('image')
    if not (t and v and file):
        return jsonify(error='Missing'), 400
    folder = 'static/img/contact_images'
    _make_folder(folder)
    fname = secure_filename(f"{t}_{file.filename}")
    path = os.path.join(folder, fname)
    file.save(path)
    mongo.db.contacts.insert_one({
        'type': t, 'value': v, 'image_path': '/' + path
    })
    return jsonify(success=True)


@edit_pages.route('/delete_contact', methods=['POST'])
def delete_contact():
    data = request.get_json() or {}
    typ, val = data.get('type'), data.get('value')
    if typ and val:
        mongo.db.contacts.delete_one({'type': typ, 'value': val})
        return jsonify(success=True)
    return jsonify(success=False), 400


@edit_pages.route('/handle_map_marker', methods=['POST'])
def handle_map_marker():
    data = request.get_json() or {}
    lat, lng, name, action = (
        data.get('latitude'),
        data.get('longitude'),
        data.get('name'),
        data.get('action')
    )
    if None in (lat, lng, name, action):
        return jsonify(error='Missing'), 400

    coll = mongo.db.map_coordinates
    tpl = {"name": name, "Longitude": lng, "Latitude": lat}
    if action == 'addHikedPlace':
        tpl['type'] = 'hiked place';  coll.insert_one(tpl)
    elif action == 'removeHikedPlace':
        coll.delete_one({**tpl, 'type': 'hiked place'})
    elif action == 'addPlaceToHike':
        tpl['type'] = 'place to hike'; coll.insert_one(tpl)
    elif action == 'removePlaceToHike':
        coll.delete_one({**tpl, 'type': 'place to hike'})
    else:
        return jsonify(error='Unknown action'), 400

    return jsonify(status='success')


@edit_pages.route('/edit_img_attrib_table', methods=['POST'])
def edit_img_attrib_table():
    _edit_table(
        'image_attribution_table', 'tableData', 'originalImagePaths',
        'Image Name', 'Image', 'static/img/image_attributions',
        '{key}_attrib.{ext}'
    )
    return jsonify(success=True)

