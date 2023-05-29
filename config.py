class Config(object):
    SECRET_KEY = '6436d28a1fdc45d1aff4c2b429ad120f'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    UPLOAD_FOLDER = 'static/pdf_preview'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
