from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))

SQLALCHEMY_TRACK_MODIFICATIONS = False 
SECRET_KEY = b'u\xa9\x04\xa0\x18P-\xact\x08\x9e\xc4\xb2{MN'
