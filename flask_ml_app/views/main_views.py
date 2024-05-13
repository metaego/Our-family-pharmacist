from flask import Blueprint, url_for # render_template
# from werkzeug.utils import redirect
from flask import redirect, request, jsonify
# from dotenv import load_dotenv  ####################################### 여기 주석해주세요!
import os

# load_dotenv()    ##################################################### 여기도 주석해주세요!!!
bp = Blueprint('main', __name__, url_prefix='/')
@bp.route('/', methods=['get', 'post'])
def flask_index():
    data = request.get_json()
    print(f'flask에서 받은 data 출력: {data}')
    
    # db에서 필요한 데이터 불러오기
    # ai 추천 모델 실행
    # 실행 결과 db insert
    # 필요한 내용 장고에 return
    response_data = {
        'message' : '응답성공!',
        'profileid' : data.get('profile_id'),
        'surveyid' : data.get('survey_id')
    }
    return jsonify(response_data)
    # return redirect( 'http://' + os.environ.get('AWS_PUBLIC_IP') + ':8000/')
    # return redirect(url_for('question._list'))

    # question = Question.query.get_or_404(question_id)
#     return render_template('question/question_detail.html', question=question)