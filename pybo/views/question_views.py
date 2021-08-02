from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from datetime import datetime

from pybo.views.auth_views import login_required
from pybo.models import Question, Answer, User
from pybo.forms import QuestionForm, AnswerForm
from pybo import db

bp = Blueprint('question',__name__, url_prefix='/question')

@bp.route('/list')
def _list():
    # 입력 파라미터
    page = request.args.get('page',type=int, default=1) 
    kw = request.args.get('kw', type=str, default='')
    
    #url에서 페이지 파라미터 가져오기 - 조회
    question_list = Question.query.order_by(Question.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).sbuquery()
        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) |
                    Question.content.ilike(search) |
                    User.username.ilike(search) |
                    sub_query.c.content.ilike(search) |
                    sub_query.c.username.ilike(search)
                    ) \
            .distinct()

    question_list = question_list.paginate(page, per_page=10)
    # pagination 객체로 만들기. 위 설정에서는 page 변수를 시작으로 10개씩 끊어줌.
    return render_template('question/question_list.html', question_list = question_list, page=page, kw=kw)

@bp.route('/detail/<int:question_id>')
def detail(question_id):
    form = AnswerForm()
    
    question = Question.query.get(question_id)
    return render_template('question/question_detail.html', question = question, form=form)

@bp.route('/create/', methods=('GET','POST'))
@login_required
def create():
    form = QuestionForm()

    if request.method == 'POST' and form.validate_on_submit():
        #해당 라우팅에 요청 method가 post고 validator에 이상 없을 때
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user = g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    # 평상시에는 위 조건문이 실행이 안되겠지. get 방식으로 create에 요청이 오니깐.

    return render_template('question/question_form.html', form=form)

@bp.route('/modify/<int:question_id>', methods=('GET','POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        # 로그인 여부로 수정 가능 권한 확인하기 
        flash('수정 권한이 없습니다!')
        return redirect(url_for('question.detail', question_id = question_id))
    if request.method == 'POST':
        # modify 라우트에서 post 방식으로 폼을 제출할 때
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            # 이 경우, subject와 content 
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id = question.id))
    else:
        #get 방식으로 modify 라우트로 연결될 때 
        form = QuestionForm(obj=question)
        # 해당 폼에 미리 db에서 조회한 데이터를 넣어놓기, 이 경우엔 subject, content
    return render_template('question/question_form.html', form = form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))
    