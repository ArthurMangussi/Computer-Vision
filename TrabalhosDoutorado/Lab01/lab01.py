import cv2
import numpy as np

import argparse

class DetectaRetangulo:
  def __init__(self, path_image:str,
               lower_threshold:int,
               upper_threshold:int, 
               Lmin: int,
               Lmax: int,
               s: float) -> None:
     self.lower_threshold = lower_threshold
     self.upper_threshold = upper_threshold
     self.image = cv2.imread(path_image, cv2.IMREAD_GRAYSCALE)
     self.Lmin = Lmin
     self.Lmax = Lmax
     self.s = s
  
  def verifica_restricao_graus(self,approx:np.ndarray, s: float)->bool:
    """
    Função para verificar a tolerância para ±15° com a vertical e 
    horizontal, baseado em um parâmetro sensível

    Args:
        approx: As coordenadas dos pontos do retângulo
        s (float): O parâmetro sensível

    Returns:
        bool: True se as restrições forem satisfeitas, False caso contrário
    """
   
    pontos = approx.reshape(-1, 2)  # Formato mais conveniente (4,2)

    # Extrai os pontos
    p1, p2, p3, p4 = pontos

    # Calcula vetores para os lados
    lado_esquerdo = p4 - p1
    lado_superior = p2 - p1
    lado_direito = p3 - p2
    lado_inferior = p3 - p4

    # Verifica paralelismo (ângulo próximo a 0° ou 180° entre lados opostos)
    def verifica_paralelismo(v1, v2, tol_graus=s*15):
        angulo = np.degrees(np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))))
        return min(angulo, 180 - angulo) <= tol_graus

    # Verifica ortogonalidade (ângulo próximo a 90° entre lados adjacentes)
    def verifica_ortogonalidade(v1, v2, tol_graus=s*15):
        angulo = np.degrees(np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))))
        return abs(angulo - 90) <= tol_graus

    # Verifica se é retângulo dentro da tolerância
    paralelos_horizontais = verifica_paralelismo(lado_superior, lado_inferior)
    paralelos_verticais = verifica_paralelismo(lado_esquerdo, lado_direito)
    ortogonal = verifica_ortogonalidade(lado_superior, lado_esquerdo)

    if paralelos_horizontais and paralelos_verticais and ortogonal:
        return True
    else:
        return False
  
  def run(self):
    """
    Método Principal para Detectar Retângulos na imagem.
    """

    image_out = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)


    edges = cv2.Canny(self.image, 
                      self.lower_threshold, 
                      self.upper_threshold)

    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:

      peri = cv2.arcLength(c, True)

      approx = cv2.approxPolyDP(c, 0.015*peri, True)

      if len(approx) == 4:
            
            if self.verifica_restricao_graus(approx=approx, s = self.s):
              x,y,w,h = cv2.boundingRect(approx)

              # Filtrando pelos comprimentos dos lados
              if self.Lmin <= w <= self.Lmax:
                  cv2.rectangle(image_out, (x, y), (x + w, y + h), (0, 255, 255), 3)
    
    return image_out

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path", help="Caminho para a imagem de entrada")
    parser.add_argument("--lower", type=int, default=50, help="Limiar inferior para Canny")
    parser.add_argument("--upper", type=int, default=200, help="Limiar superior para Canny")
    parser.add_argument("--Lmin", type=int, default=100, help="Comprimento mínimo do lado")
    parser.add_argument("--Lmax", type=int, default=500, help="Comprimento máximo do lado")
    parser.add_argument("--s", type=float, default=0.5, help="Sensibilidade (0.0 a 1.0)")
    parser.add_argument("--output", help="Caminho para salvar a imagem de saída")
    
    args = parser.parse_args()
    
    detector = DetectaRetangulo(
        args.image_path,
        lower_threshold=args.lower,
        upper_threshold=args.upper,
        Lmin=args.Lmin,
        Lmax=args.Lmax,
        s=args.s
    )
    
    result = detector.run()
    
    if args.output:
        cv2.imwrite(args.output, result)
        print(f"Resultado salvo em: {args.output}")
    else:
        cv2.imshow("Resultado", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()