from flask import render_template, jsonify, render_template_string, request
from app import app, db

@app.context_processor
def show_admin_controls():
    from app.utils.profiles.login import check_admin
    return dict(is_admin=check_admin())


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
    content = Content.query.filter_by(key='welcome').first()
    return render_template('layout.html', page_content=content)


@app.route('/blog')
def blog():
    from app.models import Content
    content = Content.query.filter_by(key='test').first()
    return render_template('blog.html', page_content=content)


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
