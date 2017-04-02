from app import app, db


def initdb():
    ''' Create the SQL database. '''
    print('Creating SQLAlchemy DB')
    db.create_all()


def dropdb():
    ''' Delete the SQL database. '''
    print('Deleting SQLAlchemy DB')
    db.drop_all()


if __name__ == '__main__':
    # dropdb()
    # initdb()
    app.debug = True
    app.run()
