import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

# ==========================================
# 1. CONFIGURAÇÕES
# ==========================================

PASTA_DATASET = r"C:\Users\Smart Sensor Design\OneDrive\Documentos\analise_cnn\produtos_dataset"

TAMANHO_IMAGEM = (128, 128)
BATCH_SIZE = 16
EPOCAS = 20
# ==========================================
# 2. CARREGAR AS IMAGENS
# ==========================================

treino = tf.keras.utils.image_dataset_from_directory(
    PASTA_DATASET + "/train",
    image_size=TAMANHO_IMAGEM,
    batch_size=BATCH_SIZE,
    shuffle=True,
    seed=123
)

validacao = tf.keras.utils.image_dataset_from_directory(
    PASTA_DATASET + "/validation",
    image_size=TAMANHO_IMAGEM,
    batch_size=BATCH_SIZE,
    shuffle=False
)

teste = tf.keras.utils.image_dataset_from_directory(
    PASTA_DATASET + "/test",
    image_size=TAMANHO_IMAGEM,
    batch_size=BATCH_SIZE,
    shuffle=False
)

print("Classes:", treino.class_names)
# ==========================================
# 3. NORMALIZAÇÃO
# ==========================================

normalizacao = layers.Rescaling(1./255)

## ==========================================
# 4. DATA AUGMENTATION
# ==========================================

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1)
])


# ==========================================
# 5. CRIAR A CNN
# ==========================================

modelo = models.Sequential([

    data_augmentation,

    normalizacao,

    layers.Conv2D(32, (3, 3), activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(64, (3, 3), activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(128, (3, 3), activation="relu"),
    layers.MaxPooling2D(),

    layers.GlobalAveragePooling2D(),

    layers.Dense(64, activation="relu"),

    layers.Dropout(0.3),

    layers.Dense(1, activation="sigmoid")
])

# ==========================================
# 6. COMPILAR
# ==========================================

modelo.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

modelo.summary()

# # ==========================================
# 7. TREINAR
# ==========================================

historico = modelo.fit(
    treino,
    validation_data=validacao,
    epochs=EPOCAS
)


# ==========================================
# 8. AVALIAR NO TESTE
# ==========================================

resultado_teste = modelo.evaluate(teste)

print("Loss no teste:", resultado_teste[0])
print("Accuracy no teste:", resultado_teste[1])


# ==========================================
# 9. TESTAR UMA IMAGEM NOVA
# ==========================================

caminho_imagem = r"C:\Users\Smart Sensor Design\OneDrive\Documentos\analise_cnn\imagens_teste\produto1.jpeg"

imagem = tf.keras.utils.load_img(
    caminho_imagem,
    target_size=TAMANHO_IMAGEM
)

imagem = tf.keras.utils.img_to_array(imagem)

imagem = np.expand_dims(imagem, axis=0)

previsao = modelo.predict(imagem)[0][0]

prob_feio = previsao
prob_bonito = 1 - previsao

print(f"Probabilidade de BONITO: {prob_bonito:.2%}")
print(f"Probabilidade de FEIO: {prob_feio:.2%}")

if previsao >= 0.5:
    print("Resultado: FEIO")
else:
    print("Resultado: BONITO")