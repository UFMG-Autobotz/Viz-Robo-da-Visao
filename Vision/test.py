import cv2

# Abrir a webcam
cap = cv2.VideoCapture(2)

while True:
    # Capturar frame da câmera
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar frame da câmera!")
        break

    # Exibir o frame
    cv2.imshow('Camera', frame)

    # Parar o loop quando 'q' for pressionado
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Limpar e liberar a webcam
cap.release()
cv2.destroyAllWindows()
