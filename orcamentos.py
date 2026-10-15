import streamlit as st

def renderizar_orcamentos():
    st.title("📊 Módulo de Orçamentos")
    
    # Criando duas colunas: 1/3 para parâmetros (esquerda) e 2/3 para EAP (direita)
    col_parametros, col_eap = st.columns([1, 2])
    
    with col_parametros:
        st.subheader("⚙️ Parâmetros de Entrada")
        st.info("Aqui vamos colocar os campos: Nome da Área, Município, Área Total, etc.")
        
    with col_eap:
        st.subheader("📐 EAP Paramétrica")
        st.info("Aqui vai ficar a tabela com as abas de Urbanização, Contrapartida e Resumo.")
