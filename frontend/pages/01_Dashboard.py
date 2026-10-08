import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# --------------------------------------------------

st.set_page_config(
    page_title="Monitoramento de Água - IoT",
    page_icon="💧",
    layout="wide"
)

# --------------------------------------------------
# CARREGAMENTO DOS DADOS
# --------------------------------------------------

@st.cache_data
def carregar_dados():
    df = pd.read_csv("data/dados_ficticios.csv")

    df["data_hora"] = pd.to_datetime(df["data_hora"])

    return df


df = carregar_dados()

# --------------------------------------------------
# TÍTULO
# --------------------------------------------------

st.title("💧 Monitoramento Inteligente do Consumo de Água")

st.write(
    "Sistema IoT para monitoramento do consumo de água "
    "em escolas públicas."
)

# --------------------------------------------------
# FILTROS
# --------------------------------------------------

st.sidebar.header("Filtros")

escolas = ["Todas"] + sorted(df["escola"].unique().tolist())

escola_selecionada = st.sidebar.selectbox(
    "Escola",
    escolas
)

if escola_selecionada != "Todas":
    df_filtrado = df[df["escola"] == escola_selecionada].copy()
else:
    df_filtrado = df.copy()

# --------------------------------------------------
# INDICADORES
# --------------------------------------------------

consumo_total = df_filtrado["volume_l"].sum()

consumo_medio = df_filtrado["volume_l"].mean()

maior_vazao = df_filtrado["vazao_l_min"].max()

quantidade_medicoes = len(df_filtrado)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Consumo total",
    f"{consumo_total:.1f} L"
)

col2.metric(
    "Consumo médio",
    f"{consumo_medio:.1f} L"
)

col3.metric(
    "Maior vazão",
    f"{maior_vazao:.1f} L/min"
)

col4.metric(
    "Medições realizadas",
    quantidade_medicoes
)

# --------------------------------------------------
# GRÁFICO DE CONSUMO
# --------------------------------------------------

st.subheader("Consumo de água")

grafico_consumo = px.line(
    df_filtrado,
    x="data_hora",
    y="volume_l",
    markers=True,
    labels={
        "data_hora": "Data e horário",
        "volume_l": "Volume consumido (L)"
    }
)

grafico_consumo.update_layout(
    hovermode="x unified",
    xaxis=dict(
        title="Data e horário",
        tickformat="%d/%m/%Y %H:%M"
    ),
    yaxis=dict(
        title="Volume consumido (L)"
    )
)

st.plotly_chart(
    grafico_consumo,
    use_container_width=True
)

# --------------------------------------------------
# GRÁFICO DE VAZÃO
# --------------------------------------------------

st.subheader("Vazão registrada")

grafico_vazao = px.bar(
    df_filtrado,
    x="data_hora",
    y="vazao_l_min",
    labels={
        "data_hora": "Data e horário",
        "vazao_l_min": "Vazão (L/min)"
    }
)

grafico_vazao.update_layout(
    xaxis=dict(
        title="Data e horário",
        tickformat="%d/%m/%Y %H:%M"
    ),
    yaxis=dict(
        title="Vazão (L/min)"
    )
)

st.plotly_chart(
    grafico_vazao,
    use_container_width=True
)

# --------------------------------------------------
# HISTÓRICO
# --------------------------------------------------

st.subheader("Histórico das medições")

historico = df_filtrado.sort_values(
    "data_hora",
    ascending=False
).copy()

# Formatação das colunas para apresentação
historico["data_hora"] = historico["data_hora"].dt.strftime(
    "%d/%m/%Y %H:%M"
)

historico = historico.rename(
    columns={
        "data_hora": "Data e horário",
        "escola": "Escola",
        "dispositivo": "Dispositivo",
        "vazao_l_min": "Vazão (L/min)",
        "volume_l": "Volume consumido (L)"
    }
)

st.dataframe(
    historico,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# ALERTAS FICTÍCIOS
# --------------------------------------------------

st.subheader("⚠️ Alertas")

alertas = df_filtrado[
    df_filtrado["vazao_l_min"] > 4.0
].copy()

if len(alertas) > 0:

    st.warning(
        f"Foram identificadas {len(alertas)} medições "
        "que ultrapassaram o limite definido para "
        "demonstração."
    )

    alertas["data_hora"] = alertas["data_hora"].dt.strftime(
        "%d/%m/%Y %H:%M"
    )

    alertas = alertas.rename(
        columns={
            "data_hora": "Data e horário",
            "escola": "Escola",
            "dispositivo": "Dispositivo",
            "vazao_l_min": "Vazão (L/min)",
            "volume_l": "Volume consumido (L)"
        }
    )

    st.dataframe(
        alertas,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "Nenhum alerta encontrado nos dados apresentados."
    )
