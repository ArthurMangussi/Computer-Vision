"""
# Algoritmo de Canny

1. Redução de ruído: Filtro Gaussiano
2. Gradientes de intensidade: derivada primeira
3. Suprresão de não-máximos: Descarte de pixels com vizinho de maior magnitude na direção do gradiente
4. Histerese
  - Limiar alto (marcados como arestas)
  - Limiar baixo (Potenciais areestas)
5. Conexidade
  - Marcar arestas fracas quando conectadas às fortes

"""
import numpy as np
import cv2
from codes.convolve import KERNEL_GAUSSIAN, convolution

class Canny():
  def __init__(self, image:np.ndarray,
               lower_threshold:int,
               upper_threshold:int) -> None:
     self.lower_threshold = lower_threshold
     self.upper_threshold = upper_threshold
     self.image = image

  @staticmethod
  def non_max_suppression(magnitude: np.ndarray, angle: np.ndarray) -> np.ndarray:
    """
    Aplica Non-Maximum Suppression em uma imagem de magnitude e ângulo de gradiente.

    Args:
        magnitude: imagem com a magnitude do gradiente (numpy.ndarray).
        angle: imagem com a direção do gradiente em graus (numpy.ndarray).

    Returns:
        nms: imagem após supressão de não-máximos.
    """

    # Cria imagem de saída zerada
    nms = np.zeros_like(magnitude)

    # Converte ângulo para entre 0 e 180
    angle = angle % 180

    # Pega o tamanho da imagem
    H, W = magnitude.shape

    for i in range(1, H-1):
        for j in range(1, W-1):
            q = 255
            r = 255

            # Verifica direção do ângulo
            if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                # Direção 0 graus (horizontal) → comparar com esquerda e direita
                q = magnitude[i, j+1]
                r = magnitude[i, j-1]

            elif (22.5 <= angle[i,j] < 67.5):
                # Direção 45 graus → comparar com superior direito e inferior esquerdo
                q = magnitude[i-1, j+1]
                r = magnitude[i+1, j-1]

            elif (67.5 <= angle[i,j] < 112.5):
                # Direção 90 graus (vertical) → comparar com cima e baixo
                q = magnitude[i-1, j]
                r = magnitude[i+1, j]

            elif (112.5 <= angle[i,j] < 157.5):
                # Direção 135 graus → comparar com superior esquerdo e inferior direito
                q = magnitude[i-1, j-1]
                r = magnitude[i+1, j+1]

            # Se o pixel for maior que os vizinhos, mantém, senão zera
            if (magnitude[i,j] >= q) and (magnitude[i,j] >= r):
                nms[i,j] = magnitude[i,j]
            else:
                nms[i,j] = 0

    return nms

  @staticmethod
  def double_threshold(img, low_threshold, high_threshold):
    """
    Aplica Double Threshold para bordas após Non-Maximum Suppression.

    Args:
        img: imagem após NMS (numpy.ndarray)
        low_threshold: limiar inferior
        high_threshold: limiar superior

    Returns:
        strong_edges: imagem com bordas fortes (valor 255)
        weak_edges: imagem com bordas fracas (valor 75)
    """
    # Cria imagem de saída zerada
    res = np.zeros_like(img, dtype=np.uint8)

    strong_pixel = 250
    weak_pixel = 50

    # Bordas fortes
    strong_i, strong_j = np.where(img >= high_threshold)
    res[strong_i, strong_j] = strong_pixel

    # Bordas fracas
    weak_i, weak_j = np.where((img >= low_threshold) & (img < high_threshold))
    res[weak_i, weak_j] = weak_pixel

    return res

  def connectedness(self,img):
    """
    Aplica Conexidade para conectar bordas fracas a fortes.

    Args:
        img: imagem depois do Double Threshold.

    Returns:
        final_edges: imagem final com bordas fortes conectadas.
    """
    H, W = img.shape
    strong_pixel = 250
    weak_pixel = 50

    # Copia da imagem de entrada
    final_edges = np.copy(img)

    for i in range(1, H-1):
        for j in range(1, W-1):
            # Se o pixel atual é fraco
            if final_edges[i, j] == weak_pixel:
                # Verifica se algum dos 8 vizinhos é forte
                if ((final_edges[i+1, j-1] == strong_pixel)
                    or (final_edges[i+1, j] == strong_pixel)
                    or (final_edges[i+1, j+1] == strong_pixel)
                    or (final_edges[i, j-1] == strong_pixel)
                    or (final_edges[i, j+1] == strong_pixel)
                    or (final_edges[i-1, j-1] == strong_pixel)
                    or (final_edges[i-1, j] == strong_pixel)
                    or (final_edges[i-1, j+1] == strong_pixel)):

                    # Se tem um forte vizinho, promove para forte
                    final_edges[i, j] = strong_pixel
                else:
                    # Se não, apaga
                    final_edges[i, j] = 0

    return final_edges

  def detect_edge(self):
    """
    Código principal para algoritmo de Canny
    """
    # Filtro gaussiano
    conv = convolution(image=self.image, kernel=KERNEL_GAUSSIAN)


    # Gradientes de intensidade
    sobelx = cv2.Sobel(conv, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(conv, cv2.CV_64F, 0, 1, ksize=3)

    magnitude_gradiente = np.sqrt(sobelx**2 + sobely**2)
    theta = np.rad2deg(np.arctan2(sobely, sobelx))

    # Supressão de não-máximos
    descarte_pixels = self.non_max_suppression(magnitude_gradiente, theta)

    histerese = self.double_threshold(descarte_pixels,
                                      self.lower_threshold,
                                      self.upper_threshold)

    end_img = self.connectedness(histerese)
    return end_img
