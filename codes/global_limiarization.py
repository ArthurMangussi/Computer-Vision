"""
# Limiarização Global - Algoritmo
1. Escolher um limiar inicial T.
2. Segmentar a imagem pelo limiar T, gerando dois conjuntos de pixels G1 e G2.
3. Calcular as médias de intensidade m1 e m2 dos grupos G1 e G2 na imagem original.
4. Atualizar o valor de T = 0.5(m1+m2)
5. Repetir os passos 2. a 4. até que o valor de T não varie mais que um delta.

"""
import numpy as np

def global_limirization(image:np.ndarray,
                       init_threshold:int,
                       delta: float)->np.ndarray:
  """
  Algoritmo de Limiarização Global.

  Args:
    image: Imagem a ser limiarizada.
    threshold: Limiar inicial.
    delta: Tolerância para a variação do threshold.

  Returns:
    mask: Imagem binária.
  """
  while  True:
    # Segmentando imagem pelo limiar,
    # gerando dois conjuntos de pixels G1 e G2
    g1 = image[image < init_threshold]
    g2 = image[image >= init_threshold]

    # Médias de intensidades
    mean_g1 = np.mean(g1)
    mean_g2 = np.mean(g2)

    threshold = 0.5 * (mean_g1 + mean_g2)

    if threshold - init_threshold < delta:
      break
    else:
      init_threshold = threshold

  # Aplica o threshold e cria a imagem binária
  mask = np.where(image > threshold, 255, 0).astype(np.uint8)
  return mask