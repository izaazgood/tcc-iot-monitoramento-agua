import streamlit as st

# --------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# --------------------------------------------------

st.set_page_config(
    page_title="Monitoramento de Água - IoT",
    page_icon="💧",
    layout="wide"
)

# --------------------------------------------------
# NAVEGAÇÃO
# --------------------------------------------------

pagina_painel = st.Page(
    "pages/01_Dashboard.py",
    title="Painel",
    icon="📊"
)

pagina_historico = st.Page(
    "pages/02_Historico.py",
    title="Histórico",
    icon="📋"
)

pagina_alertas = st.Page(
    "pages/03_Alertas.py",
    title="Alertas",
    icon="🚨"
)

pagina_escolas = st.Page(
    "pages/04_Escolas.py",
    title="Escolas",
    icon="🏫"
)

# --------------------------------------------------
# MENU PRINCIPAL
# --------------------------------------------------

pg = st.navigation(
    {
        "💧 Monitoramento": [
            pagina_painel,
            pagina_historico,
            pagina_alertas,
            pagina_escolas
        ]
    }
)

# --------------------------------------------------
# EXECUÇÃO
# --------------------------------------------------

pg.run()
