import os
import json
from datetime import datetime
from flask import Flask, render_template, request
from deepface import DeepFace
import cv2
import unicodedata

app = Flask(__name__)

# 업로드 폴더 설정
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# NoSQL 유사 JSON 로그 파일 경로
LOG_FILE = 'focus_log.json'

# 초기 로그 파일 생성 (없을 경우)
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=4)


# 감정 및 성별 분석 함수
def analyze_focus(img_path):
    try:
        result = DeepFace.analyze(img_path=img_path, actions=['emotion', 'gender'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        gender = result[0]['dominant_gender']

        # 감정별 집중도 매핑
        focus_map = {
            'happy': 90, 'neutral': 70, 'sad': 40,
            'angry': 30, 'fear': 20, 'disgust': 10, 'surprise': 60
        }
        focus = focus_map.get(emotion, 50)
        status = "집중" if focus >= 70 else ("보통" if focus >= 40 else "집중안됨")

        return emotion, gender, focus, status

    except Exception as e:
        print("❌ Analyze Error:", e)
        return None, None, None, None


# 메인 페이지
@app.route('/')
def index():
    return render_template('index.html')


# 이미지 업로드 및 분석
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return "파일이 업로드되지 않았습니다."

    file = request.files['file']
    if file.filename == '':
        return "파일명이 없습니다."

    # 파일명 한글 깨짐 방지
    safe_filename = unicodedata.normalize('NFKD', file.filename).encode('ascii', 'ignore').decode('ascii')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
    file.save(filepath)

    emotion, gender, focus, status = analyze_focus(filepath)
    if emotion is None:
        return "분석 중 오류가 발생했습니다."

    # JSON 로그 구조 (NoSQL 유사)
    log_entry = {
        "source": safe_filename,
        "gender": gender,
        "emotion": emotion,
        "focus": focus,
        "status": status,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # 로그 저장 (append)
    with open(LOG_FILE, 'r+', encoding='utf-8') as f:
        logs = json.load(f)
        logs.append(log_entry)
        f.seek(0)
        json.dump(logs, f, ensure_ascii=False, indent=4)

    # 결과 페이지 렌더링
    return render_template('result.html',
                           image_path=filepath,
                           emotion=emotion,
                           focus=focus,
                           status=status,
                           gender=gender,
                           time=log_entry["timestamp"])


if __name__ == '__main__':
    app.run(debug=True)
