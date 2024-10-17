import os
import streamlit as st
import googleapiclient.discovery

# YouTube API 키를 환경 변수에서 불러오기
api_key = os.getenv('YOUTUBE_API_KEY')

# 함수: 채널 핸들을 입력받아 채널 ID를 반환
def get_channel_id(handle):
    try:
        # YouTube API 클라이언트 생성
        youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)
        
        # 채널 검색 요청 생성
        request = youtube.search().list(
            part="snippet",
            q=handle,
            type="channel"
        )
        
        # API 요청 실행 및 응답 받기
        response = request.execute()
        
        # 응답에서 채널 ID 추출
        channel_id = response['items'][0]['snippet']['channelId']
        return channel_id
    except Exception as e:
        # 오류 발생 시 오류 메시지 반환
        return f"Error: {str(e)}"

# Streamlit 앱 제목 설정
st.title("YouTube 채널 ID 및 RSS 피드 생성기")

# 사용자로부터 YouTube 채널 핸들 입력 받기
handle = st.text_input("유튜브 채널 핸들을 입력하세요 (예: @3protv)")

# 채널 ID 확인 및 RSS 피드 생성 버튼
if st.button("채널 ID 및 RSS 피드 생성"):
    if handle:
        # 입력된 핸들로 채널 ID 가져오기
        channel_id = get_channel_id(handle)
        
        if "Error" in channel_id:
            # 오류 발생 시 오류 메시지 표시
            st.error(f"채널 ID를 가져오는 중 오류가 발생했습니다: {channel_id}")
        else:
            # 채널 ID 출력
            st.success(f"채널 ID: {channel_id}")
            
            # RSS 피드 URL 생성 및 출력
            rss_feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
            st.write(f"RSS 피드 URL: {rss_feed_url}")
            
            # RSS 피드 URL을 코드 형식으로 표시 (복사하기 쉽게)
            st.code(rss_feed_url, language='plaintext')
    else:
        # 핸들이 입력되지 않았을 때 경고 메시지 표시
        st.warning("유튜브 채널 핸들을 입력해주세요.")