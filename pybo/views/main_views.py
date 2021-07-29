from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main',__name__, url_prefix = '/')
# 이름, 모듈명, 프리픽스

@bp.route('/hello')
def hello_pybo():
    return 'Hello, pybo!'

@bp.route('/')
def index():
    return redirect(url_for('question._list'))
    # question은 블루프린트 이름, _list는 그 안의 라우팅 함수 이름
    # url_for로 불러온 url을 redirect하는 것 