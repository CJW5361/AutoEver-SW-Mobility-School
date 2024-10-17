import openai
import pandas as pd
import numpy as np

# OpenAI API 키 설정
openai.api_key = ''

# 시스템 프롬프트 설정
system_prompt = """당신은 다국어 데이터셋의 각 항목이 자동차 또는 교통과 관련되어 있는지 분류하는 전문가입니다. 아래의 지침을 따라 각 데이터 항목을 신중히 분석하고 분류해주세요.

1. 데이터 형식:
   - ID: 고유 식별자
   - lang: 언어 코드 (en, kr, de, es, jp, cn 등)
   - title: 데이터셋의 제목
   - notes: 데이터셋에 대한 추가 설명 (일부 항목은 비어있을 수 있음)

2. 분류 기준:
   a) 키워드 포함:
      - 영어: car, vehicle, traffic, road, highway, drive, automotive, truck, transport, bus, taxi, parking, accident, safety
      - 한국어: 자동차, 차량, 교통, 도로, 고속도로, 운전, 트럭, 운송, 버스, 택시, 주차, 사고, 안전
      - 독일어: Auto, Fahrzeug, Verkehr, Straße, Autobahn, fahren, LKW, Transport, Bus, Taxi, Parken, Unfall, Sicherheit
      - 스페인어: coche, vehículo, tráfico, carretera, autopista, conducir, camión, transporte, autobús, taxi, estacionamiento, accidente, seguridad
      - 일본어: 自動車, 車両, 交通, 道路, 高速道路, 運転, トラック, 輸送, バス, タクシー, 駐車, 事故, 安全
      - 중국어: 汽车, 车辆, 交通, 道路, 高速公路, 驾驶, 卡车, 运输, 公交车, 出租车, 停车, 事故, 安全

   b) 관련 주제:
      - 교통 안전, 사고 데이터
      - 차량 등록 정보
      - 도로 인프라 (충전소, CCTV, 신호등, 도로 폭, 차선 수)
      - 교통량, 통행량 데이터
      - 차량 관련 규제 또는 정책
      - 주차 정보
      - 대중교통 (버스, 택시, 지하철 등)
      - 교통 카드 사용 데이터
      - 차량 연료 (가솔린, 디젤, 전기, 수소 등)
      - 운전 면허 관련 정보
      - 차량 보험 데이터
      - 자율주행 기술

   c) 관련 기관 또는 출처:
      - 교통부, 도로공사, 자동차 제조업체, 교통 안전 공단 등

   d) 데이터 유형:
      - GPS 데이터, 차량 움직임 관련 데이터
      - 도로 네트워크 데이터
      - 실시간 교통 흐름 데이터

   e) 간접적 관련성:
      - 도시 계획이나 지역 개발 데이터 중 교통 인프라와 관련된 내용
      - 환경 데이터 중 차량 배출가스나 교통 관련 오염과 관련된 내용

3. 제외 기준:
   - 명확히 다른 주제에 관한 데이터 (인구 통계, 교육, 의료, 농업, 해양 등)는 자동차나 교통과 관련 없음으로 분류
   - 단, 이러한 주제라도 교통이나 차량과 직접적으로 연관된 내용이 있다면 관련 있음으로 분류 가능

4. 분류 방법:
   - 'title'과 'notes'를 주의 깊게 읽고 분석
   - 자동차/교통 관련: 1, 비관련: 0으로 표시

5. 주의사항:
   - 언어와 상관없이 일관된 기준 적용
   - 모호한 경우, 데이터의 주요 목적을 기준으로 판단

각 항목에 대해 0 또는 1로 응답해주세요."""

def create_user_prompt(data):
    user_prompt = f"다음 {len(data)}개의 데이터들이 자동차 관련 데이터인지 판별해주세요:\n\n"
    for _, row in data.iterrows():
        user_prompt += f"ID: {row['ID']}\n"
        user_prompt += f"lang: {row['lang']}\n"
        user_prompt += f"title: {row['title']}\n"
        user_prompt += f"notes: {row['notes']}\n\n"
    user_prompt += f"총 {len(data)}개의 데이터에 대해 각각 0 또는 1로 답변해주세요."
    # print(len(data))
    return user_prompt

def get_model_predictions(prompt, expected_count):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    
    result = response.choices[0].message['content'].strip().split('\n')
    # print(len(result))
    if len(result) != expected_count:
        print(f"경고: 예상된 응답 개수({expected_count})와 실제 응답 개수({len(result)})가 다릅니다.")
        print("API 응답:", response.choices[0].message['content'])
    # print(result)
    def clean_result(r):
        # 숫자만 추출합니다
        return ''.join(filter(str.isdigit, r))
    
    return [int(clean_result(r)) for r in result]
    # return [int(r) for r in result]

# Train 데이터 로드 및 테스트
train_data = pd.read_csv('train.csv')
train_prompt = create_user_prompt(train_data)
train_predictions = get_model_predictions(train_prompt,len(train_data))

# 정확도 계산
accuracy = np.mean(train_data['target'] == train_predictions)
print("예측값:", train_predictions)
print("실제값:", train_data['target'].tolist())
print(f"Train 데이터 정확도: {accuracy:.2f}")

# Test 데이터 로드
test_data = pd.read_csv('test.csv')

# User 프롬프트 생성
user_prompt = create_user_prompt(test_data)
test_predictions=get_model_predictions(user_prompt,len(test_data))
# print("예측값:", test_predictions)
print('길이',len(test_predictions))
# 최종 제출 파일 생성
submission = pd.DataFrame({
    'system': [system_prompt],
    'user': [user_prompt]
})

# submission.csv 파일로 저장
submission.to_csv('submission.csv', index=False)

print("제출 파일이 생성되었습니다: submission.csv")
