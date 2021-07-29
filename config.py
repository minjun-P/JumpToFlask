import os

# 루트 디렉토리
BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
# 루트 디렉토리 주소에 pybo.db 생성하기 

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "dev"


