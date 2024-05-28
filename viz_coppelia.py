import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
from apriltag import Detector
from std_msgs.msg import Float32

class ImageProcessor(Node):
    def __init__(self):
        super().__init__('image_processor')
        self.subscription_rgb = self.create_subscription(Image, '/image_viz', self.callback_rgb, 10)
        self.publisher_left_motor = self.create_publisher(Float32, '/leftMotorSpeed', 10)
        self.publisher_right_motor = self.create_publisher(Float32, '/rightMotorSpeed', 10)

        self.bridge = CvBridge()
        self.detector = Detector()

        self.target_center = None
        self.tag_visible = False

    def callback_rgb(self, msg):
        frame_rgb = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        
        height, width, _ = frame_rgb.shape
        self.target_center = width * 2 / 3  # Define 2/3 da largura da imagem como a área alvo

        gray = cv2.cvtColor(frame_rgb, cv2.COLOR_BGR2GRAY)
        
        detections = self.detector.detect(gray)
        
        if detections:
            for detection in detections:
                rect = detection.corners.astype(int)
                tag_center = rect[:, 0].mean()  # Calcula o centro da tag
                self.tag_visible = True
                
                # Calcula a diferença entre o centro da tag e a área alvo
                diff = tag_center - self.target_center
                
                # Define a velocidade dos motores com base na diferença
                # Você pode ajustar os valores multiplicativos para obter um comportamento desejado
                left_speed = 0.01 - 0.01 * diff
                right_speed = 0.01 + 0.01 * diff
                
                # Publica as velocidades dos motores
                self.publisher_left_motor.publish(Float32(data=left_speed))
                self.publisher_right_motor.publish(Float32(data=right_speed))
                
                # Desenha uma linha na área alvo
                cv2.line(frame_rgb, (int(self.target_center), 0), (int(self.target_center), height), (0, 255, 0), 2)
                
                # Desenha o retângulo ao redor da tag
                cv2.polylines(frame_rgb, [rect], True, (0, 255, 0), 2)
                
                # Mostra o ID da tag no frame
                tag_id = detection.tag_id
                cv2.putText(frame_rgb, f"ID: {tag_id}", (rect[0][0], rect[0][1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Se a tag não estiver visível, mantenha as velocidades dos motores baixas para evitar movimentos desnecessários
        if not self.tag_visible:
            self.publisher_left_motor.publish(Float32(data=0.01))
            self.publisher_right_motor.publish(Float32(data=0.01))
        
        self.tag_visible = False  # Resetar a flag para a próxima iteração
        
        # Exibe o frame
        cv2.imshow('Camera RGB', frame_rgb)
        cv2.waitKey(1)  # Aguarda um pouco para atualizar a janela

def main(args=None):
    rclpy.init(args=args)
    image_processor = ImageProcessor()
    rclpy.spin(image_processor)
    image_processor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
