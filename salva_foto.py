import os
import shutil

# Caminhos
pasta_mae = "imagens"
pasta_destino = "entrada"

# Criar a pasta de destino se não existir
os.makedirs(pasta_destino, exist_ok=True)

# Percorrer todas as subpastas da pasta mãe
for raiz, _, arquivos in os.walk(pasta_mae):
    for nome_arquivo in arquivos:
        if nome_arquivo.lower().endswith(".jpg"):
            caminho_origem = os.path.join(raiz, nome_arquivo)
            caminho_destino = os.path.join(pasta_destino, nome_arquivo)

            try:
                shutil.copy2(caminho_origem, caminho_destino)
            except shutil.SameFileError:
                pass  # Evita erro se tentar copiar o mesmo arquivo para ele mesmo
            except Exception as e:
                print(f"[!] Erro ao copiar {nome_arquivo}: {e}")

print(f"Imagens copiadas com sucesso para: {pasta_destino}")
