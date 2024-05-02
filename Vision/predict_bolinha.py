from ultralytics import YOLO
import cv2
import os

# Carregar o modelo
model_path = os.path.join('.', 'runs', 'detect', 'train', 'weights', 'last.pt')
model = YOLO(model_path)  # Carregar um modelo personalizado

threshold = 0.5

# Abrir a webcam
cap = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar frame da câmera!")
        break

    # Detectar objetos
    results = model(frame)

    # Desenhar caixas delimitadoras e rótulos
    if isinstance(results, list) and results:
        for pred in results[0]:
            if pred[-1] == "ball" and pred[-2] > threshold:  # Assumindo que o nome da classe é "ball"
                box = pred[:4]
                x1, y1, x2, y2 = [int(i) for i in box]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, "ball", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Exibir o frame
    cv2.imshow('Camera', frame)

    # Parar o loop quando 'q' for pressionado
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Limpar e liberar a webcam
cap.release()
cv2.destroyAllWindows()
