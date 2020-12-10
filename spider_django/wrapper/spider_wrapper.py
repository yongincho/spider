import cv2
#from matplotlib import pyplot as plt

class SpiderWrapper(object):

    def __init__(self, xml):
        self.xml = xml


    def recognize(self, image_path):
        image = cv2.imread(image_path)
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier(self.xml)

        faces = face_cascade.detectMultiScale(grayImage, 1.03, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        cv2.rectangle(image, ((0, image.shape[0] -25)),
            (270, image.shape[0]), (255,255,255), -1);
        cv2.putText(image, "PinkWink test", (0, image.shape[0] -10),
            cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0,0,0), 1);
        
        #plt.figure(figsize=(12,12))
        #plt.imshow(image, cmap='gray')
        #plt.xticks([]), plt.yticks([])
        #plt.show()

        cv2.imwrite(image_path, image)

        return image_path

if __name__ == "__main__":
    xml = '../storage/haarcascade_frontalface_default.xml'
    spi = SpiderWrapper(xml)
    recognized_image = spi.recognize("../storage/3.jpg")
    print(recognized_image)
