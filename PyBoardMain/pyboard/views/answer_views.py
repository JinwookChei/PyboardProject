from datetime import datetime

import requests
from flask import flash
from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect

from pyboard import db
from pyboard.forms import AnswerForm
from pyboard.models import Question, Answer

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>', methods=('POST',))
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = form.content.data

        # 스팸체크 서버로 요청 보내기
        try:
            spam_check_response = requests.post(
                'http://pyboard-spam-service:5001/check'
                #'http://pyboard-spam:5001/check',
                #'http://localhost:5001/check',
                json={'content': content},
                timeout=3  # 타임아웃도 걸어주는 게 좋아요
            )
            spam_check_response.raise_for_status()
            result = spam_check_response.json()
        except requests.RequestException:
            flash('스팸 체크 서버에 연결할 수 없습니다. 잠시 후 다시 시도해주세요.')
            return render_template('question/question_detail.html', question=question, form=form)

        if result.get('is_spam'):
            flash('스팸 또는 부적절한 내용이 포함되어 댓글을 등록할 수 없습니다.')
            return render_template('question/question_detail.html', question=question, form=form)

        # 스팸 아니면 저장
        answer = Answer(
            content=content,
            create_date=datetime.now(),
            question=question
        )
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))

    return render_template('question/question_detail.html', question=question, form=form)