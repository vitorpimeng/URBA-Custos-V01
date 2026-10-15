import streamlit as st
import pandas as pd
import numpy as np

def renderizar_relatorios():
    st.title("📈 Central de Relatórios e BI")
    st.markdown("Analise os custos, compare orçamentos e visualize indicadores do seu portfólio.")
    
    # Criando as abas para os diferentes relatórios que existiam no seu HTML
    aba_abc, aba_comparativo, aba_indice = st.tabs([
        "📊 Curva ABC", 
        "⚖️ Comparativo de Orçamentos", 
        "📱 Índice Viário"
    ])
    
    # ==========================================
    # ABA 1: CURVA ABC
    # ==========================================
    with aba_abc:
        st.subheader("Curva ABC de Insumos e Serviços")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.selectbox("Selecione o Orçamento", ["Residencial Urba Sul - Campinas", "Loteamento Norte - Ribeirão Preto"])
            st.selectbox("Tipo de Curva", ["Insumos", "Serviços"])
            st.button("Gerar Curva ABC", type="primary", use_container_width=True)
            
        with col2:
            # Dados falsos para simular a Curva ABC
            dados_abc = pd.DataFrame({
                "Item": ["CBUQ", "Tubo Concreto 400mm", "Aço CA-50", "Cimento", "Areia", "Brita"],
                "Valor Total (R$)": [500000, 350000, 200000, 80000, 40000, 20000],
                "Acumulado (%)": [42.0, 71.4, 88.2, 94.9, 98.3, 100.0],
                "Classe": ["A", "A", "B", "C", "C", "C"]
            })
            
            st.dataframe(
                dados_abc, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "Valor Total (R$)": st.column_config.NumberColumn(format="R$ %.2f"),
                    "Acumulado (%)": st.column_config.ProgressColumn(format="%.1f%%", min_value=0, max_value=100)
                }
            )

    # ==========================================
    # ABA 2: COMPARATIVO
    # ==========================================
    with aba_comparativo:
        st.subheader("Análise de Desvios (Comparativo)")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.selectbox("Orçamento Base (Referência)", ["Revisão 01 - Inicial"])
        with col_b:
            st.selectbox("Orçamento Atual (Comparação)", ["Revisão 02 - Ajuste de Projeto"])
            
        st.write("---")
        
        # Métricas de comparação
        m1, m2, m3 = st.columns(3)
        m1.metric(label="Custo Total (Base)", value="R$ 15.000.000")
        m2.metric(label="Custo Total (Atual)", value="R$ 16.500.000", delta="R$ 1.500.000", delta_color="inverse")
        m3.metric(label="Variação (%)", value="10%", delta="10%", delta_color="inverse")

    # ==========================================
    # ABA 3: ÍNDICE VIÁRIO
    # ==========================================
    with aba_indice:
        st.subheader("Evolução do Custo vs Índice Viário")
        st.info("Gráfico de dispersão mostrando a relação entre o Índice Viário (%) e o Custo por m².")
        
        # Gerando dados aleatórios para simular o gráfico do seu BI
        dados_grafico = pd.DataFrame({
            "Índice Viário (%)": np.random.uniform(20, 40, 50),
            "Custo (R$/m²)": np.random.uniform(100, 250, 50)
        })
        
        # O Streamlit tem gráficos nativos muito fáceis de usar
        st.scatter_chart(
            dados_grafico,
            x="Índice Viário (%)",
            y="Custo (R$/m²)",
            color="#10b981", # Verde Urba
            height=400
        )
