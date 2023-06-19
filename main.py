import cv2
from flask import Flask, Response
#http://localhost:5000/video_feed

app = Flask(__name__)

camera = cv2.VideoCapture(0)  # Используйте 0 для основной камеры или 1, 2 и т. д. для других камер
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

def generate_frames():
    while True:
        success, frame = camera.read()  # Получаем следующий кадр с камеры

        if not success:
            break

        # Здесь вы можете производить дополнительную обработку кадра (если требуется)

        # Преобразовываем кадр в формат JPEG для передачи по сети
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Возвращаем кадр как видеопоток
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return "Добро пожаловать на IP-камеру!"

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)