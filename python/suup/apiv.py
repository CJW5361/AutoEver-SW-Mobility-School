# Python3 샘플 코드 #


import requests
servicekey='wKXVoZD3JTnajz7I2NG5STcdGGkG+9wYeT0RnnZnbFzOnVpgdv5oysBgCVdD3HomSPkHinfymX9QAYSjj2Vc1Q=='
url = 'http://apis.data.go.kr/B552657/ErmctInsttInfoInqireService/getParmacyListInfoInqire'
params ={f'serviceKey' : {servicekey}, 'Q0' : '서울특별시', 'Q1' : '강남구', 'QT' : '1', 'QN' : '삼성약국', 'ORD' : 'NAME', 'pageNo' : '1', 'numOfRows' : '10' }

response = requests.get(url, params=params)
print(response.content)