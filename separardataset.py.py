import os
import shutil
import random

# ==========================================
# CONFIGURAÇÕES
# ==========================================

ORIGEM = r"C:\Users\Smart Sensor Design\OneDrive\Documentos\analise_cnn\produtos"

DESTINO = r"C:\Users\Smart Sensor Design\OneDrive\Documentos\analise_cnn\produtos_dataset"

CLASSES = ["bonitos", "feios"]

PROPORCAO_TREINO = 0.70
PROPORCAO_VALIDACAO = 0.15
PROPORCAO_TESTE = 0.15

random.seed(123)


# ==========================================
# 1. APAGAR DATASET ANTIGO
# ==========================================

if os.path.exists(DESTINO):
    shutil.rmtree(DESTINO)

print("Dataset antigo removido.")


# ==========================================
# 2. CRIAR NOVAS PASTAS
# ==========================================

for conjunto in ["train", "validation", "test"]:

    for classe in CLASSES:

        pasta = os.path.join(
            DESTINO,
            conjunto,
            classe
        )

        os.makedirs(pasta, exist_ok=True)


# ==========================================
# 3. SEPARAR AS IMAGENS
# ==========================================

for classe in CLASSES:

    pasta_origem = os.path.join(
        ORIGEM,
        classe
    )

    imagens = [
        arquivo
        for arquivo in os.listdir(pasta_origem)
        if arquivo.lower().endswith(
            (".jpg", ".jpeg", ".png", ".webp")
        )
    ]

    random.shuffle(imagens)

    total = len(imagens)

    quantidade_treino = int(
        total * PROPORCAO_TREINO
    )

    quantidade_validacao = int(
        total * PROPORCAO_VALIDACAO
    )

    treino = imagens[:quantidade_treino]

    validacao = imagens[
        quantidade_treino:
        quantidade_treino + quantidade_validacao
    ]

    teste = imagens[
        quantidade_treino + quantidade_validacao:
    ]

    conjuntos = {
        "train": treino,
        "validation": validacao,
        "test": teste
    }


    # ==========================================
    # 4. COPIAR AS IMAGENS
    # ==========================================

    for nome_conjunto, lista_imagens in conjuntos.items():

        for imagem in lista_imagens:

            origem = os.path.join(
                pasta_origem,
                imagem
            )

            destino = os.path.join(
                DESTINO,
                nome_conjunto,
                classe,
                imagem
            )

            shutil.copy2(
                origem,
                destino
            )


    # ==========================================
    # 5. MOSTRAR RESULTADOS
    # ==========================================

    print()
    print("Classe:", classe)
    print("Total:", total)
    print("Treino:", len(treino))
    print("Validação:", len(validacao))
    print("Teste:", len(teste))


print()
print("==========================================")
print("DATASET SEPARADO COM SUCESSO!")
print("==========================================")