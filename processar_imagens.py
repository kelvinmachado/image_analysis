import os
import cv2
import numpy as np
import pandas as pd

# Diretórios
input_dir = "entrada"
output_dir = "saida"
os.makedirs(output_dir, exist_ok=True)

# Arquivos
imagens = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

dados = []

# Limiares para tons cinza-claro no HSV
lower_gray = np.array([0, 0, 150])     # H: baixa, S: baixa, V: alto
upper_gray = np.array([180, 50, 250])  # H: médio, S: baixo, V: alto

for img_nome in imagens:
    caminho = os.path.join(input_dir, img_nome)
    imagem = cv2.imread(caminho)
    imagem_hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)

    # Criar máscara para manchas cinza-claro (argamassa)
    mascara = cv2.inRange(imagem_hsv, lower_gray, upper_gray)

    # Pós-processamento
    kernel = np.ones((3, 3), np.uint8)
    mascara_limpa = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel, iterations=1)

    # Área de contato
    area_total = mascara.size
    area_contato = cv2.countNonZero(mascara_limpa)
    percentual = 100 * area_contato / area_total

    # Salvar imagem processada
    nome_saida = os.path.splitext(img_nome)[0] + "_mancha.png"
    cv2.imwrite(os.path.join(output_dir, nome_saida), mascara_limpa)

    # Dados
    dados.append({
        "imagem": img_nome,
        "area_contato_px": area_contato,
        "area_total_px": area_total,
        "percentual_contato": percentual
    })

    print(f"[OK] {img_nome}: {percentual:.2f}%")

# Exportar relatório CSV
df = pd.DataFrame(dados)
df.to_csv(os.path.join(output_dir, "resultado_contato.csv"), index=False)
