import streamlit as st
import orcamentos
import configuracoes
import relatorios
import banco_dados

# 1. CONFIGURAÇÃO DA PÁGINA (Deve ser a primeira linha do Streamlit)
st.set_page_config(
    page_title="Urba Construtora - Orçamento Paramétrico",
    page_icon="🏗️",
    layout="wide", # Usa a tela toda, parecido com o seu design original
    initial_sidebar_state="expanded"
)

# 2. INICIALIZAÇÃO DO ESTADO DA SESSÃO
# Aqui guardamos as variáveis que não podem ser perdidas quando a tela recarregar
if 'usuario_logado' not in st.session_state:
    st.session_state['usuario_logado'] = False
if 'email_usuario' not in st.session_state:
    st.session_state['email_usuario'] = ""
if 'perfil_usuario' not in st.session_state:
    st.session_state['perfil_usuario'] = ""

# 3. FUNÇÃO DA TELA DE LOGIN
# 3. FUNÇÃO DA TELA DE LOGIN
def tela_login():
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.image("https://urba.com.br/wp-content/uploads/2021/03/logo-urba.png", width=200)
        st.markdown("<h4 style='text-align: center; color: #10b981;'>Módulo Prospecção & Orçamentos</h4>", unsafe_allow_html=True)
        st.write("---")
        
        # Criando as abas de Login e Cadastro (igual você tinha no JS!)
        aba_login, aba_cadastro = st.tabs(["Entrar", "Criar Conta"])
        
        with aba_login:
            with st.form(key="form_login"):
                email = st.text_input("E-mail")
                senha = st.text_input("Senha", type="password")
                submit_login = st.form_submit_button("Entrar no Sistema", use_container_width=True)
                
                if submit_login:
                    if email and senha:
                        with st.spinner("Autenticando..."):
                            # AQUI CHAMAMOS O BANCO DE DADOS REAL!
                            resultado = banco_dados.fazer_login(email, senha)
                            
                            if resultado["sucesso"]:
                                st.session_state['usuario_logado'] = True
                                st.session_state['email_usuario'] = resultado["email"]
                                st.session_state['perfil_usuario'] = resultado["funcao"]
                                st.session_state['user_id'] = resultado["id"]
                                
                                # --- NOVO: CARREGANDO OS DADOS DO BANCO PARA A MEMÓRIA ---
                                with st.spinner("Carregando matrizes de dados..."):
                                    dados_iniciais = banco_dados.carregar_dados_iniciais()
                                    if dados_iniciais["sucesso"]:
                                        st.session_state['matriz_polos'] = dados_iniciais["dados"]["polos"]
                                        st.session_state['matriz_produtos'] = dados_iniciais["dados"]["produtos"]
                                        st.session_state['matriz_pavimento'] = dados_iniciais["dados"]["pavimento"]
                                        st.session_state['matriz_indiretos'] = dados_iniciais["dados"]["indiretos"]
                                        st.session_state['matriz_opcionais'] = dados_iniciais["dados"]["opcionais"]
                                    else:
                                        st.error(f"Erro ao carregar matrizes: {dados_iniciais['erro']}")
                                # ----------------------------------------------------------
                                
                                st.rerun()
                            else:
                                st.error(f"Erro ao entrar: {resultado['erro']}")
                    else:
                        st.warning("Por favor, preencha e-mail e senha.")
                        
        with aba_cadastro:
            with st.form(key="form_cadastro"):
                novo_email = st.text_input("Novo E-mail")
                nova_senha = st.text_input("Nova Senha", type="password")
                funcao = st.selectbox("Perfil de Acesso", ["prospector", "orcamento"])
                submit_cadastro = st.form_submit_button("Criar Nova Conta", use_container_width=True)
                
                if submit_cadastro:
                    if novo_email and nova_senha:
                        with st.spinner("Criando conta..."):
                            resultado = banco_dados.criar_conta(novo_email, nova_senha, funcao)
                            if resultado["sucesso"]:
                                st.success("Conta criada com sucesso! Vá para a aba 'Entrar' para fazer login.")
                            else:
                                st.error(f"Erro ao cadastrar: {resultado['erro']}")
                    else:
                        st.warning("Preencha todos os campos.")

# 4. FUNÇÃO DA TELA PRINCIPAL (O APP) E DASHBOARD
def tela_dashboard():
    # Pega o nome antes do @ no email para dar boas-vindas
    nome_usuario = st.session_state['email_usuario'].split('@')[0].capitalize()
    
    st.title(f"Olá, {nome_usuario}! 👋")
    st.markdown("### Bem-vindo ao seu Centro de Comando de Orçamentos.")
    st.write("---")
    
    # Criando duas colunas (1/3 e 2/3 do espaço)
    col_esq, col_dir = st.columns([1, 2])
    
    with col_esq:
        st.subheader("⭐ Acesso Rápido")
        st.button("📄 Novo Orçamento", use_container_width=True)
        st.button("🧮 Simular Orçamento", use_container_width=True)
        st.button("📝 Solicitar Orçamento", use_container_width=True)
        
    with col_dir:
        st.subheader("🕒 Últimos Orçamentos")
        # Tabela de dados falsos só para vermos o visual
        dados_recentes = {
            "Data": ["15/10/2026", "14/10/2026", "10/10/2026"],
            "Área": ["Residencial Urba Sul", "Loteamento Norte", "Condomínio das Árvores"],
            "Município": ["Ribeirão Preto", "Campinas", "São José do Rio Preto"],
            "Status": ["Concluído", "Em Andamento", "Em Andamento"]
        }
        st.dataframe(dados_recentes, use_container_width=True, hide_index=True)

def tela_principal():
    # Criando o Menu Lateral (Sidebar)
    with st.sidebar:
        st.markdown("### 🏗️ URBA CUSTOS") 
        st.caption(f"👤 {st.session_state['email_usuario']}")
        st.caption(f"🏷️ Perfil: {st.session_state['perfil_usuario']}")
        st.write("---")
        
        # O st.radio é o nosso menu de navegação
        menu_selecionado = st.radio(
            "Navegação",
            ["🏠 Início", "📊 Orçamentos", "📍 Prospecção", "📈 Relatórios", "⚙️ Configurações"]
        )
        
        st.write("---")
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state['usuario_logado'] = False
            st.session_state['email_usuario'] = ""
            st.session_state['perfil_usuario'] = ""
            st.rerun()

    # Roteamento: Mostra a tela dependendo do que foi clicado no menu
    if menu_selecionado == "🏠 Início":
        tela_dashboard()
    elif menu_selecionado == "📊 Orçamentos":
        orcamentos.renderizar_orcamentos()
    elif menu_selecionado == "📍 Prospecção":
        st.title("📍 Módulo de Prospecção")
    elif menu_selecionado == "📈 Relatórios":
        relatorios.renderizar_relatorios()
    elif menu_selecionado == "⚙️ Configurações":
        configuracoes.renderizar_configuracoes()

# 5. ROTEAMENTO (O "Coração" do app)
# Se não estiver logado, mostra login. Se estiver, mostra o app.
if not st.session_state['usuario_logado']:
    tela_login()
else:
    tela_principal()
