from flask import session
from app.models import User


def get_profile(db, user_json):
    if user_json['id'] == 'logouttoken':
        session.pop('id', None)
        session.pop('name', None)
        return

    from app.models import User
    existing = User.query.filter_by(id=user_json['id']).first()
    if existing is None:
        new = User(user_json['id'], user_json['name'])
        db.session.add(new)
        db.session.commit()
        print("NEW: id [" + str(new.get_id())
              + "] name [" + str(new.get_name()) + "]")
    else:
        print("EXISTING: id [" + str(user_json['id'])
              + "] name [" + str(user_json['name']) + "]")
    session['id'] = user_json['id']
    session['name'] = user_json['name']


def check_admin():
    try:
        existing = User.query.filter_by(id=session['id']).first()
        if existing is not None:
            if existing.get_admin() is True:
                return True
    except KeyError:
        pass
    return False
