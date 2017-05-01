import os
from flask import render_template, request, redirect, url_for
from flask import send_from_directory, abort
from werkzeug.utils import secure_filename
from app import app, db
from app.utils.profiles.login import check_admin, get_user_id


@app.context_processor
def universal_html_data():
    dictionary = dict()

    dictionary['is_admin'] = check_admin()

    from app.models import Banners
    from app.utils.convert import banners_objectlist_to_urllist
    banners = Banners.query.all()
    dictionary['banners_list'] = banners_objectlist_to_urllist(banners)

    from app.models import Quotes
    from app.utils.convert import quotes_objectlist_to_quotelist
    quotes = Quotes.query.all()
    dictionary['quotes_list'] = quotes_objectlist_to_quotelist(quotes)
    return dictionary


@app.route('/ajax', methods=['POST'])
def login():
    from app.utils.convert import user_data_to_json
    user_json = user_data_to_json(request.data)

    from app.utils.profiles.login import get_profile
    get_profile(db, user_json)

    return str(user_json['id'])


@app.route('/')
def index():
    from app.models import Content
    content = Content.query.filter_by(key='index').first()
    return render_template('layout.html', page_content=content)


@app.route('/about')
def about():
    from app.models import Content
    content = Content.query.filter_by(key='about').first()
    return render_template('default.html', page_content=content)


@app.route('/contact')
def contact():
    from app.models import Content
    content = Content.query.filter_by(key='contact').first()
    return render_template('default.html', page_content=content)


@app.route('/join')
def join():
    from app.models import Content
    content = Content.query.filter_by(key='join').first()
    return render_template('default.html', page_content=content)


@app.route('/blog/<filter>')
def blog(filter):
    from app.models import UserBlogPosts
    posts_list = UserBlogPosts.query.all()
    return render_template('blog.html', all_posts=posts_list,
                           filter=filter)


@app.route('/blog_post/<id>')
def blog_post(id):
    from app.models import UserBlogPosts
    post = UserBlogPosts.query.filter_by(id=int(id)).first()
    return render_template('post.html', post=post)


@app.route('/new_post')
def new_blog_post():
    if not get_user_id():
        abort(403)
    return render_template('editors/new_post.html')


@app.route('/save_post', methods=['POST'])
def post_data_handler():
    from app.utils.profiles.login import get_user_id
    if not get_user_id():
        abort(403)
    from app.models import UserBlogPosts
    request_form = request.form
    title = request_form.getlist('title')[0]
    text = request_form.getlist('text')[0]
    text = text.replace('\n', '<br />')
    filter = request_form.getlist('filter')[0]

    from app.utils.profiles.login import get_user_name
    user = get_user_name()

    from app.utils.profiles.login import get_user_id
    user_id = get_user_id()

    img_url = None
    while True:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                break
            file = request.files['file']
            # if user does not select file, browser also submits
            # an empty part without filename
            if file.filename == '':
                break
            from werkzeug.utils import secure_filename
            from app.utils.upload import allowed_file
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                       filename))
                img_url = file.filename
            break

    if img_url is not None:
        img_url = 'img/uploads/' + img_url

    new_post = UserBlogPosts(title, text, img_url, filter, user, user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('blog', filter='ALL') + '#top')


@app.route('/freshers_trip')
def freshers_trip():
    from app.models import Content
    content = Content.query.filter_by(key='freshers_trip').first()
    return render_template('default.html', page_content=content)


@app.route('/spain_trip')
def spain_trip():
    from app.models import Content
    content = Content.query.filter_by(key='spain_trip').first()
    return render_template('default.html', page_content=content)


@app.route('/donegal_trip')
def donegal_trip():
    from app.models import Content
    content = Content.query.filter_by(key='donegal_trip').first()
    return render_template('default.html', page_content=content)


@app.route('/wicklow_trip')
def wicklow_trip():
    from app.models import Content
    content = Content.query.filter_by(key='wicklow_trip').first()
    return render_template('default.html', page_content=content)


@app.route('/scotland_trip')
def scotland_trip():
    from app.models import Content
    content = Content.query.filter_by(key='scotland_trip').first()
    return render_template('default.html', page_content=content)


@app.route('/trad_trip')
def trad_trip():
    from app.models import Content
    content = Content.query.filter_by(key='trad_trip').first()
    return render_template('default.html', page_content=content)


@app.route('/gola_trip')
def gola_trip():
    from app.models import Content
    content = Content.query.filter_by(key='gola_trip').first()
    return render_template('default.html', page_content=content)


@app.route('/committee')
def committee():
    from app.models import Committee
    committee_list = Committee.query.all()
    return render_template('committee.html', committee=committee_list)


@app.route('/committee_edit/<role>')
def committee_editor(role):
    if not check_admin():
        abort(403)
    from app.models import Committee
    committee_member = Committee.query.filter_by(role=role).first()
    committee_member = Committee.query.get(committee_member.id)
    return render_template('editors/committee_deets.html',
                           role=committee_member)


@app.route('/committee_save/<role>', methods=['POST'])
def committee_data_handler(role):
    if not check_admin():
        abort(403)
    from app.models import Committee
    request_form = request.form
    role = role
    name = request_form.getlist('name')[0]
    text = request_form.getlist('text')[0]
    committee_member = Committee.query.filter_by(role=role).first()
    committee_member = Committee.query.get(committee_member.id)
    committee_member.name = name
    committee_member.text = text

    img_url = None
    while True:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                break
            file = request.files['file']
            # if user does not select file, browser also submits
            # an empty part without filename
            if file.filename == '':
                break
            from werkzeug.utils import secure_filename
            from app.utils.upload import allowed_file
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                       filename))
                img_url = file.filename
            break

    if img_url is not None:
        committee_member.photo = 'img/uploads/' + img_url

    db.session.commit()
    return redirect(url_for('committee'))


@app.route('/content_edit/<page>')
def content_editor(page):
    if not check_admin():
        abort(403)
    from app.models import Content
    content = Content.query.filter_by(key=page).first()
    return render_template('editors/content.html', page=page, page_content=content)


@app.route('/content_save/<page>', methods=['POST'])
def content_data_handler(page):
    if not check_admin():
        abort(403)
    from app.models import Content
    request_form = request.form
    title = request_form.getlist('content_title')[0]
    text = request_form.getlist('content_text')[0]
    content = Content.query.filter_by(key=page).first()
    content = Content.query.get(content.id)
    content.title = title
    content.content = text

    img_url = ''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            img_url = ''
        file = request.files['file']
        # if user does not select file, browser also submits
        # an empty part without filename
        if file.filename == '':
            img_url = ''
        from werkzeug.utils import secure_filename
        from app.utils.upload import allowed_file
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                   filename))
            img_url = file.filename

    if img_url != '':
        content.image_url = 'img/uploads/' + img_url

    db.session.commit()
    return redirect(url_for(page, page_content=content))


@app.route('/banner_edit')
def add_banner():
    if not check_admin():
        abort(403)
    return render_template('editors/add_banner.html')


@app.route('/banner_edit', methods=['POST'])
def banner_data_handler():
    if not check_admin():
        abort(403)

    from app.models import Banners
    img_url = ''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            img_url = ''
        file = request.files['file']
        # if user does not select file, browser also submits
        # an empty part without filename
        if file.filename == '':
            img_url = ''
        from werkzeug.utils import secure_filename
        from app.utils.upload import allowed_file
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                   filename))
            img_url = url_for('static', filename='img/uploads/' + file.filename)

    if img_url != '':
        banner = Banners(img_url)
        db.session.add(banner)
        db.session.commit()
    return redirect(url_for('index'))


@app.errorhandler(403)
def forbidden(e):
    return render_template('error.html', message='403 forbidden'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message='404 not found'), 404


@app.errorhandler(410)
def gone(e):
    return render_template('error.html', message='410 gone'), 410


@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html', message='500 internal error'), 500
