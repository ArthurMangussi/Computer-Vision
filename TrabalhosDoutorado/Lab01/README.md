# 🧪 Laboratório 01 - Detectar Retângulos

Trabalho prático desenvolvido para a disciplina de Visão Computacional no doutorado.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completo-brightgreen)

---

## 📋 Sumário

- [📁 Estrutura do diretório](#-estrutura-do-diretório)
- [▶️ Como executar](#️-como-executar)
- [🖼️ Output esperado](#️-output-esperado)
- [📦 Dependências](#-dependências)
- [🤖 Uso de Inteligência Artificial](#-uso-de-inteligência-artificial)

---

## 📁 Estrutura do diretório

A pasta `images` contém quatro imagens utilizadas para teste, incluindo:

- `carro.png`: imagem fornecida via Google Classroom.
- `x_shapes.png`, entre outras: imagens geradas com auxílio do ChatGPT contendo formas geométricas para testes adicionais.

---

## ▶️ Como executar

O script `lab01.py` deve ser executado via terminal. É necessário informar:

1. O caminho para o script Python.
2. O caminho para a imagem a ser processada.
3. (Opcional) Parâmetros customizados via linha de comando.

### ✅ Parâmetros padrão

- `--lower` (limite inferior Canny): `50`
- `--upper` (limite superior Canny): `200`
- `--Lmin` (comprimento mínimo do retângulo): `100`
- `--Lmax` (comprimento máximo do retângulo): `500`
- `--s` (sensibilidade angular): `0.5`

### 💻 Exemplos de uso

```bash
python C:\Users\Mult-e\Desktop\lab01_Arthur\lab01.py C:\Users\Mult-e\Desktop\lab01_Arthur\images\carro.png --s 0.8
```

```bash
python C:\Users\Mult-e\Desktop\lab01_Arthur\lab01.py C:\Users\Mult-e\Desktop\lab01_Arthur\images\x_shapes.png --Lmin 10 --Lmax 200 --s 1.0
```

### 🖼️ Output esperado
A execução do script abrirá uma nova janela com a imagem de entrada, agora contendo retângulos desenhados em amarelo sobre os objetos detectados.

### 📦 Dependências
Instale as bibliotecas necessárias com:
```bash 
pip install opencv-python numpy
```

### Uso de Inteligência Artificial
O ChatGPT foi utilizado como apoio no entendimento de funções da biblioteca OpenCV.

A função de detecção de bordas Canny utilizada é a versão otimizada do OpenCV.

Uma versão educacional do algoritmo Canny implementada em Python está disponível no [repositório do meu Github](https://github.com/ArthurMangussi/Computer-Vision/blob/main/codes/canny.py).