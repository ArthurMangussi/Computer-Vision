import numpy as np 

# Kernels
KERNEL_LAPLACIAN = np.array([
    [0, 1,  0],
    [1, -4, 1],
    [0, 1,  0]
])

KERNEL_GAUSSIAN = np.array([
    [1, 2, 1],
    [2, 4, 2],
    [1, 2, 1]
]) / 16.0

KERNEL_MEAN = np.ones((3, 3)) / 9.0

KERNEL_MEDIAN = np.ones((3, 3))

def convolution(image:np.ndarray, kernel:np.ndarray)->np.ndarray:
  """
  Função para aplicar Convolução com soma na imagem.

  Args:
    image: Imagem a ser limiarizada.
    kernel: Kernel a ser aplicado na imagem.

  Returns:
    filtered: Imagem filtrada.
  """
  shape = image.shape
  filtered = np.zeros(shape, dtype=np.uint8)

  for i in range(1, shape[0] - 2):
    for j in range(1, shape[1] - 2):
      window = image[i:i + 3, j:j + 3]
      value = np.sum(window * kernel)
      filtered[i, j] = np.clip(value, 0, 255)

  return filtered