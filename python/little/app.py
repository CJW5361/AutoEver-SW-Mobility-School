# app.py
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
import random
from flask import Flask, render_template, request, jsonify, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.permanent_session_lifetime = timedelta(minutes=30)

class JejuDialectQuiz:
    def __init__(self):
        self.base_url = "http://www.jeju.go.kr/rest/JejuDialectService/getJejuDialectServiceList"
    
    def fetch_dialects(self, page=1, page_size=20):
        """API에서 제주도 방언 데이터를 가져옵니다."""
        params = {
            'page': page,
            'pageSize': page_size
        }
        url = f"{self.base_url}?{urllib.parse.urlencode(params)}"
        
        print(f"요청 URL: {url}")  # URL 출력
        
        try:
            with urllib.request.urlopen(url) as response:
                if response.getcode() == 200:
                    data = response.read()
                    print(f"응답 데이터: {data.decode('utf-8')}")  # 응답 데이터 출력
                    root = ET.fromstring(data)
                    items = root.findall('.//item')
                    if not items:
                        print("item을 찾을 수 없습니다.")
                    return [self.parse_item(item) for item in items if self.parse_item(item) is not None]
                else:
                    print(f"오류: HTTP {response.getcode()}")
                    return None
        except urllib.error.URLError as e:
            print(f"데이터 가져오기 오류: {e}")
            return None
        except ET.ParseError as e:
            print(f"XML 파싱 오류: {e}")
            return None
    def parse_item(self, item):
        """XML 아이템을 파싱하여 딕셔너리로 반환합니다."""
        try:
            name = item.find('name')  # 제주 방언 이름
            contents = item.find('contents')  # 표준 한국어
            sound_url = item.find('soundUrl')  # 음성 URL
            type_ = item.find('type')  # 타입
            
            # 각 필드의 값을 출력하여 확인
            print(f"name: {name.text if name is not None else '없음'}")
            print(f"contents: {contents.text if contents is not None else '없음'}")
            print(f"soundUrl: {sound_url.text if sound_url is not None else '없음'}")
            print(f"type: {type_.text if type_ is not None else '없음'}")
            
            if name is None or contents is None:
                print("필수 필드가 없습니다.")
                return None
            
            jeju_dialect = name.text.strip() if name is not None else ''
            std_korean = contents.text.strip() if contents is not None else ''
            
            # 한글만 존재하는지 확인
            if not (jeju_dialect.isalpha() and std_korean.isalpha() and 
                    all('가' <= c <= '힣' for c in jeju_dialect) and 
                    all('가' <= c <= '힣' for c in std_korean)):
                print("제주 방언 또는 표준 한국어에 한글이 아닌 문자가 포함되어 있습니다.")
                return None
            
            return {
                'jejuDialect': jeju_dialect,
                'stdKorean': std_korean,
                'soundUrl': sound_url.text.strip() if sound_url is not None and sound_url.text else '',
                'type': type_.text.strip() if type_ is not None and type_.text else ''
            }
        except AttributeError as e:
            print(f"아이템 파싱 오류: {e}")
            return None

    def get_quiz_data(self, num_questions=10):
        """퀴즈 데이터를 생성합니다."""
        all_dialects = []
        for _ in range(num_questions):
            random_page = random.randint(1, 358)  # 랜덤 페이지 선택
            data = self.fetch_dialects(page=random_page, page_size=20)
            if data:
                all_dialects.extend(data)
            else:
                print(f"페이지 {random_page}에서 유효한 데이터를 받지 못했습니다.")
        
        if not all_dialects:
            print("퀴즈 데이터를 가져오지 못했습니다.")
            return []

        return random.sample(all_dialects, min(num_questions, len(all_dialects)))



@app.route('/')
def index():
    """메인 페이지를 표시합니다."""
    return render_template('index.html')

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    """새로운 퀴즈를 시작합니다."""
    quiz = JejuDialectQuiz()
    questions = quiz.get_quiz_data(10)
    
    print(f"Fetched questions: {questions}")  # 디버깅을 위한 로그 추가
    
    if not questions:
        return jsonify({'error': '퀴즈 데이터를 가져올 수 없습니다.'}), 500
    
    # 세션에 퀴즈 데이터 저장
    session['questions'] = questions
    session['current_question'] = 0
    session['score'] = 0
    session.modified = True  # 세션 변경 사항을 명시적으로 저장
    
    first_question = format_question(questions[0])
    print(f"First question: {first_question}")  # 첫 번째 질문 로그 추가
    
    return jsonify({
        'success': True,
        'question': first_question,
        'total_questions': len(questions)
    })

@app.route('/check_answer', methods=['POST'])
def check_answer():
    """답변을 확인합니다."""
    data = request.get_json()
    answer = data.get('answer')
    used_hint = data.get('used_hint', False)
    
    questions = session.get('questions', [])
    current_question = session.get('current_question', 0)
    score = session.get('score', 0)
    
    if not questions or current_question >= len(questions):
        return jsonify({'error': '유효하지 않은 퀴즈 상태입니다.'})
    
    correct_answer = questions[current_question]['stdKorean']
    is_correct = answer.strip().lower() == correct_answer.strip().lower()
    
    if is_correct:
        score += 10 if not used_hint else 1
        session['score'] = score
    
    current_question += 1
    session['current_question'] = current_question
    
    response = {
        'is_correct': is_correct,
        'correct_answer': correct_answer,
        'score': score
    }
    
    if current_question < len(questions):
        response['next_question'] = format_question(questions[current_question])
    else:
        response['quiz_complete'] = True
        response['final_score'] = score
        response['max_score'] = len(questions) * 2
    
    print(f"Response: {response}")  # 디버깅을 위한 로그 추가
    
    return jsonify(response)

def format_question(question):
    """질문 데이터를 포맷팅합니다."""
    return {
        'dialect': question['jejuDialect'],
        'sound_url': question['soundUrl'],
        'type': question['type']
   
    
    }

if __name__ == '__main__':
    app.run(debug=True)
