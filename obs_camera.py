import cv2
import pyvirtualcam
import numpy as np
from yaml import load
from yaml import FullLoader
import time

def load_config(config_file):
    with open(config_file) as f:
        return load(f, Loader=FullLoader)
    

def main():
    config = load_config(f'external/config.yaml')

    camara_port = config['camera_port']
    width_conf = config['width']
    height_conf = config['height']
    fps_conf = config['fps']
    # Создание объекта VideoCapture для захвата видео с вебкамеры
    capture = cv2.VideoCapture(camara_port)  # 0 указывает на выбор первой доступной вебкамеры
    

    # Установка разрешения видео
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width_conf)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height_conf)

    # Создание объекта VirtualCamera
    with pyvirtualcam.Camera(width=width_conf, height=height_conf, fps=fps_conf) as virtual_cam:
        while True:
            # Захват кадра с вебкамеры
            ret, frame = capture.read()

            # Проверка успешности захвата кадра
            if not ret:
                print("Не удалось получить кадр с вебкамеры.")
                break

            # Преобразование цветового пространства кадра (если требуется)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # frame_rgb = np.expand_dims(frame, axis=2)
            # gray_frame = cv2.cvtColor(frame_rgb, cv2.COLOR_BGR2GRAY)
            smoothed_frame = cv2.GaussianBlur(frame, (5, 5), 0)

            # Отображение кадра в виртуальной камере
            virtual_cam.send(smoothed_frame)

            # Обновление виртуальной камеры
            virtual_cam.sleep_until_next_frame()

            # Отображение кадра (для отладки)
            cv2.imshow("Webcam", smoothed_frame)

            # Обработка нажатия клавиши "q" для выхода из цикла
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    # Освобождение ресурсов
    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
