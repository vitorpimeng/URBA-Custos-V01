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

# ==========================================
# 4. FUNÇÕES DE CARREGAMENTO DE DADOS (MATRIZES)
# ==========================================

def carregar_dados_iniciais():
    """
    Busca todas as matrizes base do Supabase de uma vez só.
    Equivalente às funções carregarPolosDoBanco, carregarProdutosDoBanco, etc.
    """
    dados = {}
    try:
        # 1. Carregar Polos e Cidades
        polos_db = supabase.table('insumos_polos').select('*').execute()
        dados['polos'] = polos_db.data if polos_db.data else []

        # 2. Carregar Matriz de Produtos
        produtos_db = supabase.table('produtos_matriz').select('*').execute()
        dados['produtos'] = produtos_db.data if produtos_db.data else []

        # 3. Carregar Matriz de Pavimentação
        pavimento_db = supabase.table('pavimento_matriz').select('*').execute()
        dados['pavimento'] = pavimento_db.data if pavimento_db.data else []

        # 4. Carregar Custos Indiretos
        indiretos_db = supabase.table('indiretos_matriz').select('*').execute()
        dados['indiretos'] = indiretos_db.data if indiretos_db.data else []

        # 5. Carregar Opcionais
        opcionais_db = supabase.table('opcionais_matriz').select('*').execute()
        dados['opcionais'] = opcionais_db.data if opcionais_db.data else []

        return {"sucesso": True, "dados": dados}
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}

def carregar_orcamentos_recentes(user_id):
    """
    Busca os últimos orçamentos salvos por este usuário para mostrar no Dashboard.
    """
    try:
        res = supabase.table('orcamentos_salvos').select('*').eq('user_id', user_id).order('data_salvamento', desc=True).limit(10).execute()
        return {"sucesso": True, "dados": res.data if res.data else []}
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}
