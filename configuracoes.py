import streamlit as st
import pandas as pd

def renderizar_configuracoes():
    st.title("⚙️ Configurações (Matrizes)")
    st.markdown("Gerencie as matrizes de cálculo e parâmetros globais do sistema.")
    
    # Criando abas para organizar as diferentes matrizes
    aba_produtos, aba_pavimentacao, aba_gerais = st.tabs(["Matriz de Produtos", "Matriz de Pavimentação", "Parâmetros Gerais"])
    
    with aba_produtos:
        st.subheader("Matriz de Produtos")
        st.info("💡 Dica: Você pode editar os valores clicando duas vezes nas células, ou adicionar novas linhas no final da tabela.")
        
        # Dados iniciais (mock) para a matriz de produtos
        dados_produtos = pd.DataFrame({
            "Tipo de Loteamento": ["Aberto", "Fechado", "Misto"],
            "Custo Base (R$/m²)": [120.50, 180.00, 150.75],
            "Fator Multiplicador": [1.0, 1.2, 1.1]
        })
        
        # st.data_editor é a mágica do Streamlit para tabelas editáveis!
        produtos_editados = st.data_editor(dados_produtos, use_container_width=True, num_rows="dynamic")
        
        if st.button("💾 Salvar Matriz de Produtos", type="primary"):
            st.success("Matriz de Produtos salva com sucesso! (Simulação)")
            
    with aba_pavimentacao:
        st.subheader("Matriz de Pavimentação")
        
        dados_pav = pd.DataFrame({
            "Tipo de Pavimento": ["Asfalto (CBUQ)", "Bloquete Intertravado", "Concreto Usinado"],
            "Espessura (cm)": [5, 8, 10],
            "Custo (R$/m²)": [85.00, 65.00, 110.00]
        })
        
        pav_editados = st.data_editor(dados_pav, use_container_width=True, num_rows="dynamic")
        
        if st.button("💾 Salvar Matriz de Pavimentação", type="primary"):
            st.success("Matriz de Pavimentação salva com sucesso! (Simulação)")
            
    with aba_gerais:
        st.subheader("Parâmetros Gerais")
        with st.container(border=True):
            st.number_input("BDI Padrão (%)", value=25.0, step=0.5)
            st.number_input("Taxa de Administração (%)", value=5.0, step=0.5)
            st.write("---")
            if st.button("💾 Salvar Parâmetros", type="primary"):
                st.success("Parâmetros salvos com sucesso!")
