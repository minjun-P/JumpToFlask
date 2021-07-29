from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms.widgets.core import TextArea

class QuestionForm(FlaskForm):
    # question, answer 모델과 구성이 유사
    subject = StringField('제목',validators=[DataRequired('제목은 필수입력 항목입니다.')])
    # 인자-> 라벨, 유효자(필수로 하는 데이터의 속성 표시)
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired("값 입력 필요"), Length(min=3,max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired("값입력필요"), EqualTo('password2', '비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired("값입력필요")])
    email = EmailField('이메일', validators=[DataRequired("값입력필요"), Email()])

class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

class CommentForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired()])