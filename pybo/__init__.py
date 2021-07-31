from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown


from sqlalchemy import MetaData

#루트 디렉토리에서 바로 config 파일 불러오기
import config

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

#전역 변수로 사용해서 타 모듈에서도 실행할 수 있도록
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

# 오류 페이지 구성
def page_not_found(e):
    return render_template('404.html'), 404
def server_error(e):
    return render_template('500.html'), 500

# 앱 팩토리 구성
def create_app():
    app = Flask(__name__)
    # 설정 파일을 app에 등록하기
    app.config.from_envvar('APP_CONFIG_FILE')

    # ORM - 데이터베이스 관리
    db.init_app(app)
    # - db 객체를 app과 연동해 초기화
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        migrate.init_app(app, db, render_as_batch = True)
    else:
        migrate.init_app(app, db)
    # - migrate 객체를 app과 db 연동해 초기화

    from . import models

    # 블루프린트 - 프론트엔드 관리 
    from .views import main_views, question_views, answer_views, auth_views, comment_views, vote_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(vote_views.bp)

    #오류 페이지 관리
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)

    # 필터
    from .filter import format_datetime
        #앱에 적용될 jinja 환경에 해당 함수를 필터로 추가한다.
    app.jinja_env.filters['datetime'] = format_datetime

    Markdown(app, extensions=['nl2br', 'fenced_code'])

    return app
