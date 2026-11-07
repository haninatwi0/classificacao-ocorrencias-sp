from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf


# --------------------------------------------------
# CONFIGURAÇÃO
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "modelo"

MODEL_PATH = MODEL_DIR / "modelo_mlp_furto_roubo_compat.keras"
PREPROCESSOR_PATH = MODEL_DIR / "preprocessador_furto_roubo.joblib"

FEATURES = [
    "MES",
    "LATITUDE",
    "LONGITUDE",
    "CONDUTA",
    "NOME_DELEGACIA_CIRC",
]


# --------------------------------------------------
# CARREGAMENTO DO MODELO E DO PRÉ-PROCESSADOR
# --------------------------------------------------

@st.cache_resource
def carregar_recursos():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Modelo não encontrado: {MODEL_PATH}"
        )

    if not PREPROCESSOR_PATH.exists():
        raise FileNotFoundError(
            f"Pré-processador não encontrado: {PREPROCESSOR_PATH}"
        )

    modelo = tf.keras.models.load_model(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)

    return modelo, preprocessor


# --------------------------------------------------
# INTERFACE
# --------------------------------------------------

st.set_page_config(
    page_title="Classificação de Ocorrências - São Paulo",
    page_icon="🚨",
    layout="centered",
)

st.title("Classificação de Ocorrências em São Paulo")
st.write(
    "Sistema demonstrativo de classificação de ocorrências "
    "registradas como furto ou roubo, utilizando uma rede neural MLP."
)

st.divider()

try:
    modelo, preprocessor = carregar_recursos()

    # Recupera as categorias aprendidas pelo OneHotEncoder.
    encoder = (
        preprocessor
        .named_transformers_["cat"]
        .named_steps["onehot"]
    )

    categorias_conduta = [
        str(valor) for valor in encoder.categories_[0]
    ]

    categorias_delegacia = [
        str(valor) for valor in encoder.categories_[1]
    ]

    st.subheader("Dados da ocorrência")
    st.write("Preencha os campos com as características da ocorrência.")

    with st.form("formulario_ocorrencia"):

        mes = st.selectbox(
            "Mês da ocorrência",
            options=list(range(1, 13)),
            format_func=lambda valor: f"{valor:02d}",
        )

        latitude = st.number_input(
            "Latitude",
            min_value=-90.0,
            max_value=90.0,
            value=-23.5505,
            format="%.6f",
            help="Informe a latitude da ocorrência.",
        )

        longitude = st.number_input(
            "Longitude",
            min_value=-180.0,
            max_value=180.0,
            value=-46.6333,
            format="%.6f",
            help="Informe a longitude da ocorrência.",
        )

        conduta = st.selectbox(
            "Conduta",
            options=categorias_conduta,
        )

        delegacia = st.selectbox(
            "Delegacia responsável",
            options=categorias_delegacia,
        )

        enviar = st.form_submit_button(
            "Classificar ocorrência",
            use_container_width=True,
        )

    # --------------------------------------------------
    # CLASSIFICAÇÃO
    # --------------------------------------------------

    if enviar:

        dados = pd.DataFrame(
            [{
                "MES": mes,
                "LATITUDE": latitude,
                "LONGITUDE": longitude,
                "CONDUTA": conduta,
                "NOME_DELEGACIA_CIRC": delegacia,
            }],
            columns=FEATURES,
        )

        dados_transformados = preprocessor.transform(dados)

        dados_transformados = np.asarray(
            dados_transformados,
            dtype=np.float32,
        )

        probabilidade_roubo = float(
            modelo.predict(
                dados_transformados,
                verbose=0,
            )[0][0]
        )

        probabilidade_furto = 1.0 - probabilidade_roubo

        st.divider()
        st.subheader("Resultado da classificação")

        if probabilidade_roubo >= 0.5:
            st.error("Classificação: ROUBO")
        else:
            st.success("Classificação: FURTO")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Probabilidade de furto",
                f"{probabilidade_furto:.2%}",
            )

        with col2:
            st.metric(
                "Probabilidade de roubo",
                f"{probabilidade_roubo:.2%}",
            )

        st.write("Distribuição das probabilidades:")

        grafico = pd.DataFrame(
            {
                "Probabilidade": [
                    probabilidade_furto,
                    probabilidade_roubo,
                ]
            },
            index=["Furto", "Roubo"],
        )

        st.bar_chart(grafico)

        st.caption(
            "A classificação utiliza o limiar de decisão de 0,5, "
            "conforme a configuração do modelo."
        )

except FileNotFoundError as erro:
    st.warning(
        "Os arquivos do modelo ainda não estão disponíveis. "
        "Coloque os dois arquivos treinados na pasta modelo/."
    )
    st.code(str(erro))

except Exception as erro:
    st.error("Não foi possível carregar ou executar o modelo.")
    st.exception(erro)


# --------------------------------------------------
# AVISO
# --------------------------------------------------

st.divider()

st.caption(
    "Projeto acadêmico desenvolvido para a FIAP. "
    "O modelo classifica registros de ocorrências como furto ou roubo "
    "com base nos dados fornecidos. Ele não prevê crimes futuros, "
    "não identifica suspeitos e não estima o risco criminal de pessoas "
    "ou regiões."
)