import streamlit as st

def renderizar_orcamentos():
    st.title("📊 Módulo de Orçamentos")
    
    # Criando duas colunas: 1/3 para parâmetros (esquerda) e 2/3 para EAP (direita)
    col_parametros, col_eap = st.columns([1, 2])
    
    with col_parametros:
        st.subheader("⚙️ Parâmetros de Entrada")
        
        # GRUPO 1: Identificação
        with st.container(border=True):
            st.markdown("**1. Identificação**")
            nome_area = st.text_input("Nome da Área *", value="Residencial Urba Sul")
            
            # Criando sub-colunas para colocar campos lado a lado
            col_mun1, col_mun2 = st.columns(2)
            with col_mun1:
                # Por enquanto, colocamos opções fixas. Depois puxaremos do banco de dados!
                municipio_polo = st.selectbox("Município Polo *", ["Ribeirão Preto", "Campinas", "Bauru"])
            with col_mun2:
                municipio = st.selectbox("Município *", ["Ribeirão Preto", "Cravinhos", "Sertãozinho"])
                
            col_data, col_cat = st.columns(2)
            with col_data:
                data_cadastro = st.date_input("Data de Cadastro *")
            with col_cat:
                categoria = st.selectbox("Categoria *", ["Simulação", "Pré-Orçamento", "Viabilidade"])

        # GRUPO 2: Dimensionamento
        with st.container(border=True):
            st.markdown("**2. Dimensionamento**")
            
            col_dim1, col_dim2 = st.columns(2)
            with col_dim1:
                area_total = st.number_input("Área Total (m²) *", value=150000)
                qtd_lotes = st.number_input("Qtd de Lotes *", value=360)
                largura_leito = st.number_input("Larg. Leito (m) *", value=7.0, step=0.1)
            with col_dim2:
                area_util = st.number_input("Área Útil (m²) *", value=90000)
                area_viaria = st.number_input("Área Viária (m²) *", value=35000)
                largura_passeio = st.number_input("Larg. Passeios (m) *", value=3.0, step=0.1)
                
            passeio_frente = st.selectbox("Passeio em Frente aos Lotes? *", ["Não", "Sim"])
            area_pavimento = st.number_input("Área de Pavimento (m²) *", value=0)

        # GRUPO 3: Características & Produto
        with st.container(border=True):
            st.markdown("**3. Características & Produto**")
            
            col_carac1, col_carac2 = st.columns(2)
            with col_carac1:
                tipo_loteamento = st.selectbox("Tipo *", ["Aberto", "Fechado", "Misto"])
                prazo_obra = st.selectbox("Prazo Obra *", ["24 meses", "36 meses", "42 meses"])
            with col_carac2:
                multiplos_produtos = st.checkbox("Múltiplos Produtos / Condomínios")
                indice_terraplanagem = st.selectbox("Índice Terrapl. *", ["0 a 5%", "5,1 a 9%", "Acima de 9%"])

        # GRUPO 4: Fechamentos & Opcionais
        with st.container(border=True):
            st.markdown("**4. Fechamentos & Opcionais**")
            
            perimetro_muro = st.number_input("Perímetro Muro Alvenaria (m) *", value=2500)
            
            col_fech1, col_fech2 = st.columns(2)
            with col_fech1:
                perimetro_gradil = st.number_input("Mureta + Gradil (m)", value=0)
                demolicao = st.number_input("Demolição (m²)", value=0)
                travessias = st.number_input("Travessias (un)", value=1)
                qtd_lotes_mrv = st.number_input("Qtd Lotes MRV (un)", value=0)
            with col_fech2:
                perimetro_app = st.number_input("Fechamento APP (m)", value=1200)
                supressao_mata = st.number_input("Supressão Mata (m²)", value=5000)
                bacias_retencao = st.number_input("Bacias Retenção (m²)", value=800)
                area_lote_mrv = st.number_input("M² Lote Padrão MRV", value=0)

        # BOTÃO GERAR ORÇAMENTO
        st.write("---")
        if st.button("🚀 GERAR ORÇAMENTO", use_container_width=True, type="primary"):
            st.success("Orçamento gerado com sucesso! (A tabela EAP será atualizada em breve)")
            
    with col_eap:

        st.subheader("📐 EAP Paramétrica")
        st.info("Aqui vai ficar a tabela com as abas de Urbanização, Contrapartida e Resumo.")
