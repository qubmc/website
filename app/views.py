from flask import render_template, jsonify, render_template_string, request
from app import app, db


@app.context_processor
def universal_html_data():
    dictionary = {}
    from app.utils.profiles.login import check_admin
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


# The Home page is accessible to anyone
@app.route('/')
def index():
    from app.models import Content
    content = Content.query.filter_by(key='layout').first()
    return render_template('layout.html', page_content=content)


@app.route('/blog')
def blog():
    from app.models import Content
    content = Content.query.filter_by(key='blog').first()
    return render_template('blog.html', page_content=content)


@app.route('/admin_edit/<page>')
def content_editor(page):
    from app.models import Content
    content = Content.query.filter_by(key=page).first()
    return render_template('content.html', page=page, page_content=content)


@app.route('/admin_save/<page>', methods=['POST'])
def content_data_handler(page):
    from app.models import Content
    request_form = request.form
    title = request_form.getlist('content_title')[0]
    text = request_form.getlist('content_text')[0]
    img_url = request_form.getlist('content_img_url')[0]
    content = Content.query.filter_by(key=page).first()
    content = Content.query.get(content.id)
    content.title = title
    content.content = text
    content.image_url = img_url
    db.session.commit()
    return render_template(page + '.html', page_content=content)


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
