import streamlit as st

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
def tela_login():
    # Usamos colunas para centralizar o form de login, simulando o flexbox do Tailwind
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.image("https://urba.com.br/wp-content/uploads/2021/03/logo-urba.png", width=200) # Logo provisória
        st.markdown("<h4 style='text-align: center; color: #10b981;'>Módulo Prospecção & Orçamentos</h4>", unsafe_allow_html=True)
        st.write("---")
        
        # Formulário de Login
        with st.form(key="form_login"):
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            
            # Botão de submit do formulário
            submit = st.form_submit_button("Entrar no Sistema", use_container_width=True)
            
            if submit:
                # Lógica de autenticação (Por enquanto, mockada/falsa para testes)
                if email and senha:
                    # Aqui no futuro conectaremos com o Supabase
                    st.session_state['usuario_logado'] = True
                    st.session_state['email_usuario'] = email
                    st.session_state['perfil_usuario'] = "Orçamento" # Mock
                    st.rerun() # Força a tela a recarregar para aplicar o novo estado
                else:
                    st.error("Por favor, preencha e-mail e senha.")

# 4. FUNÇÃO DA TELA PRINCIPAL (O APP)
def tela_principal():
    st.success(f"Bem-vindo, {st.session_state['email_usuario']}! Seu perfil é: {st.session_state['perfil_usuario']}")
    
    if st.button("Sair (Logout)"):
        st.session_state['usuario_logado'] = False
        st.session_state['email_usuario'] = ""
        st.session_state['perfil_usuario'] = ""
        st.rerun()

# 5. ROTEAMENTO (O "Coração" do app)
# Se não estiver logado, mostra login. Se estiver, mostra o app.
if not st.session_state['usuario_logado']:
    tela_login()
else:
    tela_principal()
