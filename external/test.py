import cv2

def main():
    # Создаем объект VideoCapture для захвата видеопотока с камеры (по умолчанию используется первая доступная камера)
    cap = cv2.VideoCapture(0)

    while True:
        # Захватываем кадр с камеры
        ret, frame = cap.read()

        # Проверяем успешность захвата кадра
        if not ret:
            print("Не удалось получить кадр с камеры.")
            break

        # Отображаем кадр в окне с именем "Camera"
        cv2.imshow("Camera", frame)

        # Проверяем нажатие клавиши "q" для выхода из цикла
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Освобождаем ресурсы
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
