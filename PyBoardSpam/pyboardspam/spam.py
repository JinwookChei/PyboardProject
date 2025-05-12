from flask import Blueprint, request, jsonify

bp = Blueprint('spam_checker', __name__)

SPAM_KEYWORDS = ['스팸', '바보', '멍청이', '똥개', 'spam', '광고', '홍보']

@bp.route('/check', methods=['POST'])
def check_spam():
    data = request.get_json()
    content = data.get('content', '')

    is_spam = any(keyword in content.lower() for keyword in SPAM_KEYWORDS)

    return jsonify({'is_spam': is_spam})