<<<<<<< HEAD
* DeepFace 기반 AI 집중도 감지 시스템 * 
ㄴ Flask + DeepFace를 이용하여 사용자의 표정과 성별을 분석하고, 집중도를 시각화하는 웹 서비스

* 개요 * 
이 프로젝트는 DeepFace 딥러닝 모델을 활용하여 사용자의 얼굴 이미지를 분석하고 감정과 성별을 예측한 뒤, 해당 감정에 따라 집중도를 계산 및 시각화하는 Flask 기반 AI 웹 서비스

* 프로젝트 목표 *
1. 딥러닝 모델(DeepFace)을 이용한 감정 인식 및 집중도 분석 구현  
2. Flask를 통한 웹 기반 서비스 개발  
3. SQLite3를 이용한 분석 결과 저장  
4. 사용자 이미지 입력 기반의 직관적 결과 시각화

* 기술 스택 *
언어 : Python 3.11
프레임워크 : Flask 
딥러닝 모델 : DeepFace (VGG-Face 기반)
라이브러리 : TensorFlow, OpenCV, Pandas, Matplotlib
데이터베이스 : SQLite3 
UI : HTML5, CSS3, JavaScript

* 폴더 구조 * 
ai_focus_detector/
    app.py : Flask 메인 서버 코드
    requirements.txt : 환경 설정 (라이브러리 버전)

    templates/
        index.html : 메인 페이지 (이미지 업로드)
        result.html : 분석 결과 페이지
    
    static/
        uploads/ : 업로드된 이미지 저장 폴더

    README.md : 프로젝트 설명 문서

* 시스템 구성도 *
사용자 이미지 입력 -> Flask Front-End -> DeepFace 모델 분석 -> 집중도 계산 + MongoDB 저장 -> 웹 UI 결과 표시

* 주요 기능 *
얼굴 감정 분석 : DeepFace를 사용하여 표정('happy', 'sad', 'neutral', 'angry' 등)을 분석 
성별 예측 : 남성/여성 확률 기반 성별 분류
집중도 산출 : 감정별 집중도 점수 계산 (0~100%)
상태 분류 : 집중도에 따라 ‘집중 / 보통 / 집중안됨’으로 분류
결과 시각화 : 분석 결과를 HTML 페이지로 시각화
DB 저장 : MongoDB에 감정 분석 로그 자동 저장

* 집중도 계산 기준 *
감정            집중도 범위(%)          의미
happy           80 ~ 95         긍정적 안정 → 높은 집중 가능성
neutral         60 ~ 85         감정이 평온 → 안정적 집중 상태
surprise        50 ~ 70         순간 자극 반응 → 일시적 집중 또는 반응
sad             30 ~ 60         감정 저하로 인한 집중력 저하 가능
angry           40 ~ 80         목표 지향적 분노일 경우 집중 가능 (예: 경쟁, 몰입)
fear            20 ~ 50         불안, 긴장으로 집중 유지 어려움
disgust         10 ~ 40         거부, 피로감 → 집중 유지 어려움

* 주요 코드 설명 *
감정 및 집중도 분석 (DeepFace)
<python>
result = DeepFace.analyze(img_path=img, actions=['emotion', 'gender'], enforce_detection=False)
emotion = result[0]['dominant_emotion']
gender = result[0]['dominant_gender']

focus_map = {
    'happy': 90, 'neutral': 70, 'sad': 40,
    'angry': 30, 'fear': 20, 'disgust': 10, 'surprise': 60
}
focus = focus_map.get(emotion, 50)
status = "집중" if focus >= 70 else ("보통" if focus >= 40 else "집중안됨")

* MongoDB 저장 로직 *
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['focus_detector']
collection = db['analysis_log']

data = {
    "filename": safe_filename,
    "gender": gender,
    "emotion": emotion,
    "focus": focus,
    "status": status,
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}
collection.insert_one(data)

실행 방법
1, 가상환경 생성
python -m venv venv
venv\Scripts\activate
2. 라이브러리 설치
pip install -r requirements.txt
3. MongoDB 서버 실행
로컬 MongoDB 실행
(기본 포트: 27017)
4. Flask 서버 실행
python app.py
5. 브라우저 접속
http://127.0.0.1:5000
이미지 업로드 → DeepFace 감정 분석 → MongoDB에 결과 저장

* requirements.txt * 
Python 프로젝트의 필수 라이브러리 목록을 적어둔 파일. 이 파일만 있으면, 코드 전체를 실행할 때 아래 한 줄로 동일한 환경을 자동으로 세팅
ㄴ pip install -r requirements.txt

flask==3.1.2 (웹 프레임워크) : 웹 서버 및 HTML 렌더링 담당
deepface==0.0.95 (얼굴 인식 및 감정 분석 모델) : Deep Learning 기반 감정·성별 분석 수행
opencv-python==4.9.0.80 (이미지 처리 도구) : 업로드된 이미지 처리, 프레임 저장 등
tensorflow-cpu==2.19.0 (딥러닝 백엔드) : DeepFace 내부 모델 구동용
tf-keras==2.19.0 (TensorFlow용 Keras 호환 모듈) : DeepFace에서 요구됨
pandas==2.2.2 (데이터 관리) : 분석 로그(DB 내 결과 관리)
numpy==1.26.4 (수치 연산) : 이미지 및 모델 수치 연산 처리
matplotlib==3.10.7 (시각화 도구) : 결과 그래프나 통계 시각화용

* 데이터베이스(MongoDB) *
_id : MongoDB 자동 생성 ID
filename : 업로드된 이미지 파일명
gender : 성별 예측 결과
emotion : 주요 감정
focus : 집중도(%)
status : 집중 상태(집중/보통/집중안됨)
timestamp : 분석 시각


* 참고 자료 *
DeepFace: https://github.com/serengil/deepface
Flask 공식 문서: https://flask.palletsprojects.com
TensorFlow: https://www.tensorflow.org
MongoDB: https://www.mongodb.com
OpenCV: https://opencv.org


* 제작자 *
한양여자대학교 소프트웨어윱합학과 4학년 권현경
2025년도 딥러닝 중간 프로젝트
=======
# ai-focus-detector
AI Focus Detector | Flask + DeepFace 기반 사용자 표정·성별 분석 및 집중도 시각화 웹 서비스
>>>>>>> 1d3850395b03f82489e9e68da265d342f3b53dd7
