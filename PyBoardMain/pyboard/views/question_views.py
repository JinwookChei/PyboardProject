from datetime import datetime

import requests
from flask import flash

from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from pyboard import db
from pyboard.forms import QuestionForm, AnswerForm
from pyboard.models import Question

bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/list/')
def _list():
    question_list = Question.query.order_by(Question.create_date.desc())
    return render_template('question/question_list.html', question_list=question_list)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)


@bp.route('/create/', methods=('GET', 'POST'))
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        title = form.subject.data
        content = form.content.data
        try:
            spam_check_response = requests.post(
                'http://pyboard-spam-service:5001/check',
                #'http://pyboard-spam:5001/check',  # 스팸 체크 서버 URL
                #'http://localhost:5001/check',
                json={'content': title + ' ' + content},  # 제목과 내용 결합하여 체크
                timeout=3  # 타임아웃 설정
            )
            spam_check_response.raise_for_status()
            result = spam_check_response.json()
        except requests.RequestException:
            flash('스팸 체크 서버에 연결할 수 없습니다. 잠시 후 다시 시도해주세요.')
            return render_template('question/question_form.html', form=form)

        if result.get('is_spam'):
            flash('스팸 또는 부적절한 내용이 포함되어 질문을 등록할 수 없습니다.')
            return render_template('question/question_form.html', form=form)
        
        
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)