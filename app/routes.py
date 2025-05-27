# app/routes.py

from flask import (
    Blueprint, render_template, request, session,
    redirect, url_for, jsonify, abort
)
from bson.objectid import ObjectId
from gridfs import GridFS
import bcrypt
from app.extensions import mongo

main_bp = Blueprint('main', __name__)

# Set up GridFS once
fs = GridFS(mongo.db)


def _ensure_guest(view_name):
    """
    Helper to redirect anonymous users into guest view.
    """
    logged_in = 'username' in session
    view_mode = request.args.get('view_mode')
    if not logged_in and view_mode != 'guest':
        return redirect(url_for(view_name, view_mode='guest'))
    return logged_in, view_mode


@main_bp.route('/')
def home():
    check = _ensure_guest('main.home')
    if isinstance(check, tuple):
        logged_in, view_mode = check
    else:
        return check

    return render_template('home.html',
                           logged_in=logged_in,
                           view_mode=view_mode)


@main_bp.route('/get_sentences')
def get_sentences():
    sentences = [doc.get('sentence', '') for doc in mongo.db.home_page.find()]
    return jsonify(sentences=sentences)


@main_bp.route('/get_circular_data')
def get_circular_data():
    data = []
    for item in mongo.db.home_circular_barplot.find():
        item.pop('_id', None)
        data.append(item)
    return jsonify(data)


@main_bp.route('/get_projects')
def get_projects():
    db = mongo.db
    categories = {
        "Machine Learning": [],
        "Cybersecurity": [],
        "Database Development": [],
        "Game Development": [],
        "Story Writing": [],
    }

    # Academic & Personal
    for coll in ('academic_projects_table', 'personal_projects_table'):
        for doc in db[coll].find():
            cat = doc.get('Category')
            if cat in categories:
                categories[cat].append({
                    'title': doc.get('Name'),
                    'description': doc.get('Description'),
                    'detailsURL': doc.get('Source Code'),
                    'imagePath': doc.get('Image preview')
                })

    # Game Dev
    for doc in db.game_dev_table.find():
        categories["Game Development"].append({
            'title': doc.get('Name'),
            'description': doc.get('Description'),
            'detailsURL': doc.get('Source Code'),
            'imagePath': doc.get('Image preview')
        })

    # Story Writing
    for doc in db.story_writing_table.find():
        categories["Story Writing"].append({
            'title': doc.get('Title'),
            'description': doc.get('Description'),
            'detailsURL': doc.get('Link to Story'),
            'imagePath': doc.get('Image')
        })

    return jsonify(categories)


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        users = mongo.db.users
        user = users.find_one({'name': request.form.get('username', '')})
        if user and bcrypt.checkpw(
                request.form.get('pass', '').encode('utf-8'),
                user.get('password', b'')
        ):
            session['username'] = user['name']
            return redirect(url_for('main.home'))
        return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


@main_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('main.login'))


@main_bp.route('/about_me')
def about_me():
    check = _ensure_guest('main.about_me')
    if not isinstance(check, tuple):
        return check
    logged_in, view_mode = check

    # Single lookup; replace with your real ObjectId
    about = mongo.db.about_me_page.find_one({'_id': ObjectId('6499aafb464debafe52af92d')})
    if not about:
        abort(404)

    profile_photo = about.get('profile_photo_path', '')
    # Flatten keys & defaults
    title       = about.get('about_me_title', '')
    text_title  = about.get('about_text_title', '')
    intro       = about.get('about_me_intro', '')
    content     = about.get('about_me_content', [])

    # Unpack nested content safely
    def _nest(ix, jx, default=''):
        try:
            return content[ix][jx]
        except Exception:
            return default

    technical_skills       = _nest(0, 0)
    softwares, softwares_t = _nest(0, 1), _nest(0, 1, ['',''])[1]
    coding_lang, coding_t  = _nest(0, 2), _nest(0, 2, ['',''])[1]
    frameworks, frames_t   = _nest(0, 3), _nest(0, 3, ['',''])[1]
    leadership_skills      = _nest(1, 0)
    quest_leader, quest_d  = _nest(1, 1), _nest(1, 1, ['',''])[1]
    ra_leader, ra_desc     = _nest(1, 2), _nest(1, 2, ['',''])[1]
    experience             = _nest(2, 0)
    exp_title              = _nest(2, 1)
    counts_exps = [
        (_nest(2, i*2), _nest(2, i*2+1))
        for i in range(1, 4)
    ]
    aspirations = [_nest(3, i) for i in range(5)]

    return render_template(
        'about_me.html',
        logged_in=logged_in, view_mode=view_mode,
        profile_photo=profile_photo,
        about_me_title=title,
        about_text_title=text_title,
        about_me_intro=intro,
        technical_skills=technical_skills,
        softwares=softwares, softwares_text=softwares_t,
        coding_lang=coding_lang, coding_lang_text=coding_t,
        frameworks=frameworks, frameworks_text=frames_t,
        leadership_skills=leadership_skills,
        quest_leader=quest_leader, quest_description=quest_d,
        resident_advisor=ra_leader,
        resident_advisor_description=ra_desc,
        experience=experience,
        experience_table_title=exp_title,
        count_1=counts_exps[0][0], exp_1=counts_exps[0][1],
        count_2=counts_exps[1][0], exp_2=counts_exps[1][1],
        count_3=counts_exps[2][0], exp_3=counts_exps[2][1],
        aspirations=aspirations[0],
        asp1=aspirations[1], asp2=aspirations[2],
        asp3=aspirations[3], asp4=aspirations[4]
    )


@main_bp.route('/academic')
def academic():
    check = _ensure_guest('main.academic')
    if not isinstance(check, tuple):
        return check
    logged_in, view_mode = check

    docs = list(mongo.db.academic_projects_table.find())
    meta = mongo.db.academic_projects_main_page.find_one(
        {'_id': ObjectId('64a1c451b8eedcc8f01f326e')}
    ) or {}
    title = meta.get('academic_main_title', '')
    intro = meta.get('academic_projects_introduction', '')

    return render_template(
        'academic.html',
        logged_in=logged_in, view_mode=view_mode,
        documents=docs,
        academic_main_title=title,
        academic_projects_introduction=intro
    )


@main_bp.route('/personal')
def personal():
    check = _ensure_guest('main.personal')
    if not isinstance(check, tuple):
        return check
    logged_in, view_mode = check

    docs = list(mongo.db.personal_projects_table.find())
    meta = mongo.db.personal_projects_main_page.find_one(
        {'_id': ObjectId('64a787e80af6a3f5c9492507')}
    ) or {}
    title = meta.get('personal_projects_main_title', '')
    intro = meta.get('personal_projects_main_intro', '')

    return render_template(
        'personal.html',
        logged_in=logged_in, view_mode=view_mode,
        documents=docs,
        personal_projects_main_title=title,
        personal_projects_main_intro=intro
    )


@main_bp.route('/story_writing')
def story_writing():
    check = _ensure_guest('main.story_writing')
    if not isinstance(check, tuple):
        return check
    logged_in, view_mode = check

    docs = list(mongo.db.story_writing_table.find())
    meta = mongo.db.story_writing_main_page.find_one(
        {'_id': ObjectId('64a7882a0af6a3f5c9492508')}
    ) or {}
    title = meta.get('story_writing_main_title', '')
    intro = meta.get('story_writing_main_intro', '')

    return render_template(
        'story_writing.html',
        logged_in=logged_in, view_mode=view_mode,
        documents=docs,
        story_writing_main_title=title,
        story_writing_main_intro=intro
    )


@main_bp.route('/exploring_the_outdoor')
def exploring_the_outdoor():
    check = _ensure_guest('main.exploring_the_outdoor')
    if not isinstance(check, tuple):
        return check
    logged_in, view_mode = check

    meta = mongo.db.exploring_the_outdoor_page.find_one(
        {'_id': ObjectId('64a788640af6a3f5c9492509')}
    ) or {}
    title = meta.get('outdoor_title', '')
    intro = meta.get('outdoor_introduction', '')
    map_title = meta.get('map_title', '')

    hiked, desired = [], []
    for coord in mongo.db.map_coordinates.find():
        entry = {
            'name': coord.get('name', ''),
            'coordinates': [coord.get('Longitude'), coord.get('Latitude')]
        }
        (hiked if coord.get('type') == 'hiked place' else desired).append(entry)

    return render_template(
        'exploring_the_outdoor.html',
        logged_in=logged_in, view_mode=view_mode,
        outdoor_title=title,
        outdoor_introduction=intro,
        map_title=map_title,
        hiked_locations=hiked,
        desired_hike_locations=desired
    )


@main_bp.route('/game_development')
def game_development():
    check = _ensure_guest('main.game_development')
    if not isinstance(check, tuple):
        return check
    logged_in, view_mode = check

    docs = list(mongo.db.game_dev_table.find())
    meta = mongo.db.game_dev_main_page.find_one(
        {'_id': ObjectId('64a788e90af6a3f5c949250a')}
    ) or {}
    title = meta.get('game_dev_main_title', '')
    intro = meta.get('game_dev_main_intro', '')

    return render_template(
        'game_development.html',
        logged_in=logged_in, view_mode=view_mode,
        documents=docs,
        game_dev_main_title=title,
        game_dev_main_intro=intro
    )


@main_bp.route('/contact')
def contact():
    check = _ensure_guest('main.contact')
    if not isinstance(check, tuple):
        return check
    logged_in, view_mode = check

    contacts = list(mongo.db.contacts.find({}))
    return render_template(
        'contact.html',
        logged_in=logged_in, view_mode=view_mode,
        contacts=contacts
    )


@main_bp.route('/image_attribution')
def image_attribution():
    check = _ensure_guest('main.image_attribution')
    if not isinstance(check, tuple):
        return check
    logged_in, view_mode = check

    documents = list(mongo.db.image_attribution_table.find())
    return render_template(
        'image_attribution.html',
        logged_in=logged_in, view_mode=view_mode,
        documents=documents
    )
