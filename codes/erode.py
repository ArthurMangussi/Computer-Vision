import cv2
import numpy as np

def erode(image:cv2.imread, filter:np.ndarray)->np.ndarray:
    """
    Função de Morfologia Matemática: Erosão

    Args:
        image (cv2.imread): A imagem que desejar erodir
        filter (np.ndarray): O kernel para erosão
    
    Return:
        output (np.ndarray): A imagem erodida
    """
    output = np.zeros(image.shape, dtype=np.uint8)
    filter_size = filter.shape
    image_size = image.shape

    for x in range(image_size[1]-filter_size[1]+1):
        for y in range(image_size[0]-filter_size[0]+1):
            roi = image[y:y+filter_size[1], x:x+filter_size[0]]
            valor = np.min(roi)
            output[y+int(filter_size[1]/2), x+int(filter_size[0]/2)] = valor

    return output

if __name__ == "__main__":

    path_image = "./images/shapes.png"
    image = cv2.imread(path_image, cv2.IMREAD_GRAYSCALE)
    filter = np.ones((3,3))

    img_erosion = erode(image=image, filter=filter)

    cv2.imshow("Resultado", img_erosion)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
