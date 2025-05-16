import cv2
import numpy as np
from codes.erode import erode
from codes.dilate import dilation


def open(image:cv2.imread, filter:np.ndarray)->np.ndarray:
    """
    Função de Morfologia Matemática: Abertura

    Args:
        image (cv2.imread): A imagem que desejar 
        realizar a abertura
        filter (np.ndarray): O kernel para abertura
    
    Return:
        output (np.ndarray): A imagem aberta
    """
    ero = erode(image, filter)
    output = dilation(ero, filter)
    return output

def close(image:cv2.imread, filter:np.ndarray)->np.ndarray:
    """
    Função de Morfologia Matemática: Fechamento

    Args:
        image (cv2.imread): A imagem que desejar 
        realizar o fechamento
        filter (np.ndarray): O kernel para fechamento
    
    Return:
        output (np.ndarray): A imagem fechada
    """
    dil = dilation(image, filter)
    output = dilation(dil, filter)
    return output