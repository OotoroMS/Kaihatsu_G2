### �G�b�W���o�Ŕ��ʂ���v���O���� ###
import cv2
import numpy as np

class EdgeDetection:
    def __init__(self, threshold1=50, threshold2=150):
        self.threshold1 = threshold1
        self.threshold2 = threshold2

    def detect_edges(self, image):
        # �G�b�W���o�����s
        edges = cv2.Canny(image, self.threshold1, self.threshold2)
        return edges

    def find_defects(self, image):
        # �G�b�W���o
        edges = self.detect_edges(image)
        
        # �֊s��������
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        defects = []
        for contour in contours:
            # �ʐς����ȏ�̗֊s�����ƌ��Ȃ�
            area = cv2.contourArea(contour)
            if area > 100:  # ����臒l�͒������K�v
                defects.append(contour)

        return defects

    def draw_defects(self, image, defects):
        # ���̉摜�ɏ��̗֊s��`��
        result = cv2.drawContours(image.copy(), defects, -1, (0, 255, 0), 2)
        return result

# �e�X�g�R�[�h�i���ۂ̃��C���v���O�����ł͕ʓr�Ăяo���j
if __name__ == "__main__":
    # �T���v���摜��ǂݍ��݁i�����ł͐ԊO���J�����̃O���[�X�P�[���摜��z��j
    image = cv2.imread('/Images/Sample.jpg', cv2.IMREAD_GRAYSCALE)
    
    edge_detector = EdgeDetection()
    
    # ���̌��o
    defects = edge_detector.find_defects(image)
    
    # ���̕`��
    result_image = edge_detector.draw_defects(image, defects)
    
    # ���ʂ̕\��
    cv2.imshow('Detected Defects', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
