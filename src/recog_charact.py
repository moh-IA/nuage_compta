import cv2
import numpy as np
import operator
import os
import keras
import matplotlib.pyplot as plt



MIN_CONTOUR_AREA = 250

RESIZED_IMAGE_WIDTH = 28
RESIZED_IMAGE_HEIGHT = 28

class contourCharacter():

    npa_contour = None          
    bounding_rect = None, None, None, None       
    int_rect_x = 0                
    int_rect_y = 0                
    int_rect_width = 0            
    int_rect_height = 0          
    flt_area = 0.0  

    def calculat_rect (self):
        [int_x, int_y, int_witdh, int_height] = self.bounding_rect
        self.int_rec_x = int_x
        self.int_rec_y = int_y
        self.int_rect_width = int_witdh
        self.int_rect_height = int_height

    def valid_contour(self):
        if self.flt_area < MIN_CONTOUR_AREA:
            return False
        else:
            return True
    
#########################################################################################################################################
categories = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I":8, "J":9, "K":10, "L":11, "M":12, "N":13, "O":14, "P":15, "Q":16, "R":17, "S":18, "T":19, "U":20, "V":21, "W":22, "X":23, "Y":24, "Z":25}

def get_letter(n):
    for x, y in categories.items():
        if n == y:
            return x
def main():
    contours_data =[]
    contours_valid_data = []
    image_array= []

    image_path = '../data/predict/image_test.png'
    image_path1 = '../data/predict/'
    new_cnn_model =  keras.models.load_model('../cnn_model/cnn_model_v3.model') 

    # reading image using opencv
    image_test = cv2.imread(image_path)
   
    #converting image into gray scale image
    gray_image = cv2.cvtColor(image_test, cv2.COLOR_BGR2GRAY)

    blurred_image = cv2.GaussianBlur(gray_image, (5,5), 0)
    
    threshold_img = cv2.adaptiveThreshold(blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 11, 2)             


    threshold_img_copy = threshold_img.copy() 

 
    npa_contours, npa_hierarchy = cv2.findContours(threshold_img_copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    npa_contours_sorted = sorted(npa_contours, key=lambda ctr: cv2.boundingRect(ctr))

    for npa_contour in npa_contours_sorted:
        contour_data = contourCharacter()
        contour_data.npa_contour =npa_contour
        contour_data.bounding_rect = cv2.boundingRect(npa_contour)
        contour_data.calculat_rect()
        contour_data.flt_area = cv2.contourArea(npa_contour)
        contours_data.append(contour_data)

    for contour_data in contours_data:
        if contour_data.valid_contour():
            contours_valid_data.append(contour_data)

    
   
   
    text_result = ""
    x= 0
    for contour_data in contours_valid_data:
        cv2.rectangle( image_test, 
                      (contour_data.int_rec_x, contour_data.int_rec_y), 
                       (contour_data.int_rec_x + contour_data.int_rect_width, 
                       contour_data.int_rec_y + contour_data.int_rect_height),
                       (0,0,255),             
                        2)                        
        img_roi = threshold_img[contour_data.int_rec_y : contour_data.int_rec_y + contour_data.int_rect_height,
                                contour_data.int_rec_x : contour_data.int_rec_x + contour_data.int_rect_width]
        
        
        img_roi_resize = cv2.resize(img_roi, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))
        # cv2.imshow("imgROI", img_roi_resize) 
        # cv2.imwrite(os.path.join(image_path1, str(x) +'.png'),img_roi_resize) 
        image_array = np.array(img_roi_resize).reshape(-1,28,28,1)
        charact_pred = new_cnn_model.predict(image_array)
        if x != 12:
            text_result = text_result + get_letter(np.argmax(charact_pred ))
        x += 1
        
    print("Result : \t"+  text_result[:9] + " "+ text_result[9:13]+ " "+ text_result[13:])
       

    cv2.imshow("imgTest", image_test)      # show input image with green boxes drawn around found digits
    cv2.waitKey(0)                                          # wait for user key press

    cv2.destroyAllWindows()             # remove windows from memory

    return


###########################################################################################################################################
if __name__ == "__main__":
    main()
    