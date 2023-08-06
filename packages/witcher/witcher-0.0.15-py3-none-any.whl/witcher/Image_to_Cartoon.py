############################################
#### Date   : 2021-01-17              ######
#### Author : Babak Emami             ######
#### Model  : Image_To_Cartoon        ######
############################################

###### import requirments ##################

import cv2
import numpy as np



############################################
def cv2_imshow(image):
    """
        input : image vectore : from filechooser
        output : image plot 


        example :
        cv2_imshow(image)
    """
    
    cv2.imshow("window_name", image) 
    #waits for user to press any key  
    #(this is necessary to avoid Python kernel form crashing) 
    cv2.waitKey(0)  
    #closing all open windows  
    cv2.destroyAllWindows()
    
###################################################################################

def read_file(filename):
    """
        input : image path 
        output : image vector 

        example:

        read_file("c:/image/a.png")
    """
    img = cv2.imread(filename)
    cv2_imshow(img)
    #cv2.imshow("window_name", img) 

    #waits for user to press any key  
    #(this is necessary to avoid Python kernel form crashing) 
    cv2.waitKey(0)  

    #closing all open windows  
    cv2.destroyAllWindows() 
    return img
###################################################################################

def color_quantization(img, total_color=9, report= True):
    """
        input: image vector, number of the required colour

        output decolorized image + decolorized image vector


        example: 
        color_quantization(img, total_color=9, report= False/True )
        report= True  :> return the vector
        report= False :> will not return the vector image
    """  
    # Transform the image
    data = np.float32(img).reshape((-1, 3))
    # Determine criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    # Implementing K-Means
    ret, label, center = cv2.kmeans(data, total_color, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(img.shape)
    cv2_imshow(result)
    if report != False :
        return result
###################################################################################
def edge_mask(img, line_size=7, blur_value=7, report=True):
    """
        input :image vector , size of lines(int) , size of blur valu (int), report True/False 
        output : detected image edge , and plot the edges
        report =: True :> return the vector edges
    """    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, blur_value)
    edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)
    cv2_imshow(edges)
    
    if report != False :
        return edges


################################################################################
def Blurred(img,d=10,sigmaColor=200,sigmaSpace=200):
    """ 
        input : image vector, d=int ( degree of blur value) output blurred 
        image + blurred image vector 
    """
    
    
    blurred=cv2.bilateralFilter(img, d=d, sigmaColor=sigmaColor,sigmaSpace=sigmaSpace)
    cv2_imshow(blurred)
    return Blured
    

###################################################################################
def Cartoon(bluured=0,mask=0):
    """ 
        input : image bluured vector, mask=inage edgs vector
        image + blurred image vector 
    """
    Cartoon=cv2.bitwise_and(bluured,bluured , mask=edges)
    cv2_imshow(Cartoon)
    return Cartoon
      
###################################################################################


###################################################################################


###################################################################################

    
    
    
    
