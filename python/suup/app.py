from flask import Flask, render_template, request
import requests
import os
import logging
from xml.etree import ElementTree
import csv
from io import StringIO
import folium
# 현재 파일의 디렉토리 경로를 가져옵니다.
current_dir = os.path.dirname(os.path.abspath(__file__))

# Flask 앱을 생성할 때 템플릿 폴더의 경로를 지정합니다.
app = Flask(__name__, template_folder=os.path.join(current_dir, 'templates'))
logging.basicConfig(level=logging.DEBUG)
servicekey = 'wKXVoZD3JTnajz7I2NG5STcdGGkG+9wYeT0RnnZnbFzOnVpgdv5oysBgCVdD3HomSPkHinfymX9QAYSjj2Vc1Q=='
base_url = 'http://apis.data.go.kr/B552657/ErmctInsttInfoInqireService'

@app.route('/', methods=['GET', 'POST'])
def index():
    app.logger.info('Index 라우트에 접근했습니다.')
    if request.method == 'POST':
        app.logger.info('POST 요청을 받았습니다.')
        city = request.form['city']
        district = request.form['district']
        pharmacy_name = request.form['pharmacy_name']
        
        url = f'{base_url}/getParmacyListInfoInqire'
        params = {
            'serviceKey': servicekey,
            'Q0': city,
            'Q1': district,
            'QN': pharmacy_name,
            'ORD': 'NAME',
            'pageNo': '1',
            'numOfRows': '10'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            app.logger.info(f'API 응답 상태 코드: {response.status_code}')
            
            root = ElementTree.fromstring(response.content)
            items = root.findall('.//item')
            
            pharmacies = []
            for item in items:
                pharmacy = {
                    'hpid': item.find('hpid').text if item.find('hpid') is not None else '',
                    'dutyName': item.find('dutyName').text if item.find('dutyName') is not None else '',
                    'dutyAddr': item.find('dutyAddr').text if item.find('dutyAddr') is not None else '',
                    'dutyTel1': item.find('dutyTel1').text if item.find('dutyTel1') is not None else ''
                }
                pharmacies.append(pharmacy)
            
            app.logger.info(f'파싱된 약국 정보: {pharmacies}')
            return render_template('results.html', pharmacies=pharmacies)
        except Exception as e:
            app.logger.error(f'오류 발생: {str(e)}')
            return render_template('error.html', error='데이터 처리 중 오류가 발생했습니다.')
    
    return render_template('index.html')

@app.route('/pharmacy/<hpid>')
def pharmacy_detail(hpid):
    url = f'{base_url}/getParmacyBasisList'
    params = {
        'serviceKey': servicekey,
        'HPID': hpid
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        app.logger.info(f'API 응답: {response.text}')
        
        root = ElementTree.fromstring(response.content)
        item = root.find('.//item')
        
        if item is not None:
            pharmacy_detail = {}
            for elem in item:
                pharmacy_detail[elem.tag] = elem.text
            
            app.logger.info(f'파싱된 약국 정보: {pharmacy_detail}')
            
            # 운영 시간 정보 처리
            days = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
            operating_hours = []
            for i, day in enumerate(days, 1):
                start_time = pharmacy_detail.get(f'dutyTime{i}s', '')
                close_time = pharmacy_detail.get(f'dutyTime{i}c', '')
                if start_time and close_time:
                    start_time = f'{start_time[:2]}:{start_time[2:]}'
                    close_time = f'{close_time[:2]}:{close_time[2:]}'
                    operating_hours.append(f'{day}: {start_time} - {close_time}')
                else:
                    operating_hours.append(f'{day}: 휴무')
            
            pharmacy_detail['operating_hours'] = operating_hours
            
            app.logger.info(f'운영 시간: {operating_hours}')
            
            # Folium 지도 생성
            try:
                lat = float(pharmacy_detail['wgs84Lat'])
                lon = float(pharmacy_detail['wgs84Lon'])
                map = folium.Map(location=[lat, lon], zoom_start=15)
                folium.Marker(
                    [lat, lon], 
                    popup=pharmacy_detail['dutyName'],
                    tooltip=pharmacy_detail['dutyName']
                ).add_to(map)
                map_html = map._repr_html_()
                app.logger.info('지도 생성 완료')
            except Exception as e:
                app.logger.error(f'지도 생성 오류: {str(e)}')
                map_html = '<p>지도를 불러올 수 없습니다.</p>'
            
            return render_template('pharmacy_detail.html', pharmacy=pharmacy_detail, map_html=map_html)
        else:
            app.logger.warning(f'약국 상세 정보를 찾을 수 없습니다. HPID: {hpid}')
            return render_template('error.html', error='약국 상세 정보를 찾을 수 없습니다.')
    except Exception as e:
        app.logger.error(f'오류 발생: {str(e)}')
        return render_template('error.html', error='데이터 처리 중 오류가 발생했습니다.')



@app.route('/download_full_data')
def download_full_data():
    url = f'{base_url}/getParmacyFullDown'
    params = {
        'serviceKey': servicekey,
        'pageNo': '1',
        'numOfRows': '1000'  # 조정 가능한 숫자
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        root = ElementTree.fromstring(response.content)
        items = root.findall('.//item')
        
        csv_data = StringIO()
        csv_writer = csv.writer(csv_data)
        
        # CSV 헤더 작성
        if items:
            headers = [elem.tag for elem in items[0]]
            csv_writer.writerow(headers)
        
        # 데이터 작성
        for item in items:
            row = [elem.text for elem in item]
            csv_writer.writerow(row)
        
        csv_data.seek(0)
        return send_file(csv_data,
                         mimetype='text/csv',
                         as_attachment=True,
                         attachment_filename='pharmacy_full_data.csv')
    except Exception as e:
        app.logger.error(f'오류 발생: {str(e)}')
        return render_template('error.html', error='데이터 다운로드 중 오류가 발생했습니다.')

if __name__ == '__main__':
    app.run(debug=True)