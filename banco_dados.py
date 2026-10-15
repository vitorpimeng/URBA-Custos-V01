import streamlit as st
from supabase import create_client, Client

# 1. CONEXÃO COM O BANCO DE DADOS
# O @st.cache_resource faz o Streamlit conectar só uma vez e guardar a conexão na memória
@st.cache_resource
def iniciar_conexao() -> Client:
    # Aqui ele pega as chaves que você acabou de guardar no cofre!
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = iniciar_conexao()

# 2. FUNÇÃO DE LOGIN
def fazer_login(email, senha):
    try:
        # Tenta logar no Supabase
        resposta = supabase.auth.sign_in_with_password({"email": email, "password": senha})
        user = resposta.user
        
        if user:
            # Se logou, busca o perfil do usuário na tabela 'perfis'
            perfil_db = supabase.table('perfis').select('*').eq('id', user.id).execute()
            
            funcao = "prospector" # Padrão caso não encontre
            if perfil_db.data and len(perfil_db.data) > 0:
                funcao = perfil_db.data[0]['funcao']
                
            return {"sucesso": True, "email": user.email, "funcao": funcao, "id": user.id}
            
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}

# 3. FUNÇÃO DE CRIAR CONTA
def criar_conta(email, senha, funcao):
    try:
        # Cria o usuário no Supabase Auth
        resposta = supabase.auth.sign_up({
            "email": email, 
            "password": senha,
            "options": {"data": {"funcao": funcao}}
        })
        
        if resposta.user:
            # Insere o perfil na tabela pública
            supabase.table('perfis').insert({
                "id": resposta.user.id,
                "email": email,
                "funcao": funcao
            }).execute()
            
            return {"sucesso": True}
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}
