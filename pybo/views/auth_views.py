from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods = ('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method=='POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # 입력된 user 값이 이미 있는 것인지 확인하기 
        if not user:
            user = User(username=form.username.data, password=generate_password_hash(form.password1.data), email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
            # 오류 발생시키기!
    return render_template('auth/signup.html', form=form) 

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    3/0
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다"
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            # 세션이란? 플라스크의 자동생성 변수 - 각종 정보 저장 가능
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

# 아래 에너테이션은 모든 라우팅 함수 이전에 실행됨
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
        # 플라스크가 제공하는 컨텍스트 변수임. 요청->응답 과정에서 알아서 값이 바뀔 수 있음. 
    else:
        g.user = User.query.get(user_id)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
