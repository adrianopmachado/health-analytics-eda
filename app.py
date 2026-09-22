import streamlit as st
import pandas as pd
import joblib

# ----------------------------------------------------------------------------
# Regra oficial da OMS para classificação do IMC
# ----------------------------------------------------------------------------
def classificar_imc(imc):
    if imc < 18.5:
        return 'Abaixo do normal'
    elif 18.5 <= imc < 25.0:
        return 'Peso normal (Ideal)'
    elif 25.0 <= imc < 30.0:
        return 'Sobrepeso'
    elif 30.0 <= imc < 35.0:
        return 'Obesidade Grau I'
    elif 35.0 <= imc < 40.0:
        return 'Obesidade Grau II'
    else:
        return 'Obesidade Grau III'

# Cores por classificação — derivadas da paleta do projeto (tons de teal e terracota)
CORES_IMC = {
    'Abaixo do normal':   '#5b7b7a',
    'Peso normal (Ideal)':'#3c887e',
    'Sobrepeso':          '#ceb5a7',
    'Obesidade Grau I':   '#a17c6b',
    'Obesidade Grau II':  '#8a6759',
    'Obesidade Grau III': '#6f5245',
}

def montar_escala_imc(imc):
    """Gera uma barra horizontal segmentada mostrando onde o IMC do
    colaborador cai dentro das faixas da OMS."""
    faixas = [12, 18.5, 25, 30, 35, 40, 45]
    cores = ['#5b7b7a', '#3c887e', '#ceb5a7', '#a17c6b', '#8a6759', '#6f5245']
    escala_min, escala_max = faixas[0], faixas[-1]

    segmentos = ""
    for i in range(len(faixas) - 1):
        largura = (faixas[i + 1] - faixas[i]) / (escala_max - escala_min) * 100
        segmentos += f'<div class="imc-seg" style="flex:0 0 {largura:.4f}%; background:{cores[i]};"></div>'

    pos = max(0, min(100, (imc - escala_min) / (escala_max - escala_min) * 100))
    marcador = f'''
        <div class="imc-marker" style="left:{pos:.2f}%;">
            <div class="imc-marker-pill">{imc:.1f}</div>
            <div class="imc-marker-stick"></div>
        </div>
    '''

    return f'''
    <div class="imc-scale-wrap">
        <div class="imc-track">{segmentos}{marcador}</div>
        <div class="imc-scale-labels">
            <span>12</span><span>18.5</span><span>25</span><span>30</span><span>35</span><span>40</span><span>45+</span>
        </div>
    </div>
    '''

# ----------------------------------------------------------------------------
# Configuração da página
# ----------------------------------------------------------------------------
st.set_page_config(page_title="Simulador de Custos Médicos", page_icon="🩺", layout="wide")

# ----------------------------------------------------------------------------
# CSS — identidade visual do projeto
# ----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600;700&display=swap');

:root{
    --mint:      #e0f2e9;
    --beige:     #ceb5a7;
    --mocha:     #a17c6b;
    --slate:     #5b7b7a;
    --teal:      #3c887e;
    --teal-dark: #1f3a37;
    --ink:       #22302d;
    --paper:     #f8faf7;
}

html, body, [class*="css"]{
    font-family: 'Inter', sans-serif;
    color: var(--ink);
}

/* fundo geral */
[data-testid="stAppViewContainer"]{
    background: var(--paper);
}
[data-testid="stHeader"]{
    background: transparent;
}
.block-container{
    padding-top: 2rem;
    max-width: 980px;
}

/* ---------------- SIDEBAR ---------------- */
section[data-testid="stSidebar"]{
    background: var(--teal-dark);
    border-right: 1px solid rgba(255,255,255,0.06);
}
section[data-testid="stSidebar"] .block-container{
    padding-top: 2.2rem;
}
section[data-testid="stSidebar"] h2, 
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p{
    color: var(--mint) !important;
}
.sidebar-eyebrow{
    color: rgba(224,242,233,0.55);
    font-size: 0.78rem;
    letter-spacing: 0.02em;
    margin-bottom: 0.1rem;
}
.sidebar-title{
    font-family: 'Fraunces', serif;
    font-weight: 500;
    font-size: 1.55rem;
    color: #ffffff;
    margin-bottom: 1.6rem;
    border-bottom: 1px solid rgba(255,255,255,0.12);
    padding-bottom: 0.9rem;
}
.sidebar-section-label{
    color: var(--beige) !important;
    font-size: 0.82rem;
    margin: 1.3rem 0 0.2rem 0;
    font-weight: 600;
}

/* ---------------- SLIDERS (CORREÇÃO DEFINITIVA DAS CAIXAS) ---------------- */
/* Força a transparência no valor atual, mínimo e máximo, incluindo divs filhas */
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stThumbValue"],
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stThumbValue"] > div,
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stTickBarMin"],
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stTickBarMax"] {
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    color: var(--mint) !important;
}

/* Remove a sombra/anel que aparece ao redor da bolinha ao clicar ou arrastar */
section[data-testid="stSidebar"] [data-testid="stSlider"] div[role="slider"]:focus,
section[data-testid="stSidebar"] [data-testid="stSlider"] div[role="slider"]:hover,
section[data-testid="stSidebar"] [data-testid="stSlider"] div[role="slider"]:active {
    box-shadow: none !important;
}

/* inputs / selects dentro da sidebar */
section[data-testid="stSidebar"] [data-baseweb="input"],
section[data-testid="stSidebar"] [data-baseweb="input"] > div,
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #2b4542 !important; /* Fundo escuro fixo */
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 8px;
}

section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] [data-baseweb="select"] div {
    color: #ffffff !important; 
    -webkit-text-fill-color: #ffffff !important; /* Força o número a ficar branco */
    background: transparent !important;
}

/* Ajuste dos botões de + e - do IMC */
section[data-testid="stSidebar"] [data-testid="stNumberInput"] button {
    background-color: transparent !important;
    color: #ffffff !important;
}

/* caixa de classificação de IMC na sidebar */
.imc-chip{
    border-radius: 10px;
    padding: 0.65rem 0.85rem;
    margin-top: 0.5rem;
    font-size: 0.86rem;
    border: 1px solid rgba(255,255,255,0.12);
    color: #ffffff !important; /* Garante que o texto da classificação fique branco */
}
.imc-chip b{ color: var(--mint); }

/* ---------------- HERO / CABEÇALHO ---------------- */
.hero{
    background: linear-gradient(135deg, var(--teal) 0%, #2d6a62 100%);
    border-radius: 18px;
    padding: 2.4rem 2.6rem;
    color: #fff;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.hero::after{
    content:"";
    position:absolute; right:-60px; top:-60px;
    width:220px; height:220px; border-radius:50%;
    background: rgba(224,242,233,0.10);
}
.hero::before{
    content:"";
    position:absolute; right:40px; bottom:-70px;
    width:140px; height:140px; border-radius:50%;
    background: rgba(206,181,167,0.18);
}
.hero-eyebrow{
    color: var(--mint);
    font-size: 0.85rem;
    margin-bottom: 0.5rem;
    position: relative;
}
.hero-title{
    font-family: 'Fraunces', serif;
    font-weight: 500;
    font-size: 2.5rem;
    line-height: 1.1;
    margin: 0 0 0.7rem 0;
    position: relative;
}
.hero-sub{
    max-width: 46ch;
    color: rgba(255,255,255,0.85);
    font-size: 1rem;
    line-height: 1.5;
    position: relative;
}

/* ---------------- BOTÃO ---------------- */
.stButton > button{
    background: var(--ink);
    color: #fff;
    border: none;
    border-radius: 9px;
    padding: 0.65rem 1.6rem;
    font-weight: 600;
    font-size: 0.95rem;
    transition: background 0.15s ease, transform 0.1s ease;
}
.stButton > button:hover{
    background: var(--teal);
    transform: translateY(-1px);
}

/* ---------------- ESTADO VAZIO ---------------- */
.empty-card{
    border: 1px dashed var(--slate);
    border-radius: 14px;
    padding: 2.4rem 2rem;
    text-align: center;
    color: var(--slate);
    background: #fff;
}
.empty-card .emoji{ font-size: 1.8rem; margin-bottom: 0.4rem; }

/* ---------------- RESULTADO ---------------- */
.result-card{
    background: #fff;
    border: 1px solid #e7e0da;
    border-left: 6px solid var(--teal);
    border-radius: 14px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.6rem;
}
.result-label{
    color: var(--slate);
    font-size: 0.9rem;
    margin-bottom: 0.3rem;
}
.result-value{
    font-family: 'Fraunces', serif;
    font-weight: 500;
    font-size: 2.6rem;
    color: var(--ink);
}
.result-value span{
    font-size: 1.3rem;
    color: var(--mocha);
    font-weight: 600;
    font-family: 'Inter', sans-serif;
}

/* stat cards */
.stat-row{ display:flex; gap: 0.9rem; margin-bottom: 1.6rem; flex-wrap: wrap; }
.stat-card{
    flex: 1 1 150px;
    background:#fff;
    border:1px solid #e7e0da;
    border-radius:12px;
    padding: 0.95rem 1.1rem;
}
.stat-card .k{ color: var(--slate); font-size: 0.78rem; margin-bottom: 0.25rem;}
.stat-card .v{ font-size: 1.15rem; font-weight: 600; color: var(--ink);}

/* escala de imc */
.imc-panel{
    background:#fff;
    border:1px solid #e7e0da;
    border-radius:14px;
    padding: 1.6rem 1.9rem 1.3rem 1.9rem;
    margin-bottom: 1.6rem;
}
.imc-panel-title{
    font-size: 0.92rem;
    font-weight: 600;
    color: var(--ink);
    margin-bottom: 1rem;
}
.imc-scale-wrap{ padding-top: 26px; }
.imc-track{
    position: relative;
    display:flex;
    height: 10px;
    border-radius: 6px;
    overflow: visible;
}
.imc-seg:first-child{ border-radius: 6px 0 0 6px; }
.imc-seg:last-child{ border-radius: 0 6px 6px 0; }
.imc-marker{
    position:absolute;
    top: -26px;
    transform: translateX(-50%);
    text-align:center;
}
.imc-marker-pill{
    background: var(--ink);
    color:#fff;
    font-size:0.72rem;
    font-weight:600;
    padding: 2px 7px;
    border-radius: 20px;
    white-space:nowrap;
}
.imc-marker-stick{
    width:2px; height:14px; background: var(--ink);
    margin: 1px auto 0 auto;
}
.imc-scale-labels{
    display:flex; justify-content:space-between;
    font-size: 0.68rem; color: var(--slate);
    margin-top: 0.4rem;
}

/* footer */
.footer-note{
    text-align:center;
    color: var(--slate);
    font-size: 0.78rem;
    margin-top: 2.4rem;
    padding-top: 1.2rem;
    border-top: 1px solid #e7e0da;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Carregar o modelo treinado
# ----------------------------------------------------------------------------
modelo = joblib.load('models/modelo_predicao_custos.pkl')
# ----------------------------------------------------------------------------
# Sidebar — entrada de dados
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-eyebrow">Simulador de custos</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Perfil do Colaborador</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">Dados pessoais</div>', unsafe_allow_html=True)
    idade = st.slider('Idade', 18, 100, 30)
    sexo = st.selectbox('Sexo', ['Feminino', 'Masculino'])
    filhos = st.slider('Quantidade de Filhos', 0, 5, 0)

    st.markdown('<div class="sidebar-section-label">Saúde</div>', unsafe_allow_html=True)
    imc = st.number_input('IMC', min_value=10.0, max_value=60.0, value=25.0)
    classificacao_imc = classificar_imc(imc)
    cor_imc = CORES_IMC[classificacao_imc]
    st.markdown(
        f'''<div class="imc-chip" style="background:{cor_imc}22; border-color:{cor_imc}55;">
                <b>Classificação:</b> {classificacao_imc}
            </div>''',
        unsafe_allow_html=True
    )
    fumante = st.selectbox('Fumante', ['Não', 'Sim'])

    st.markdown('<div class="sidebar-section-label">Localização</div>', unsafe_allow_html=True)
    regiao = st.selectbox('Região', ['Centro', 'Nordeste', 'Norte', 'Sudeste'])

# ----------------------------------------------------------------------------
# Cabeçalho principal
# ----------------------------------------------------------------------------
st.markdown('''
<div class="hero">
    <div class="hero-eyebrow">Plano de saúde · Modelo preditivo</div>
    <div class="hero-title">Simulador de Custos Médicos</div>
    <div class="hero-sub">
        Estime o impacto financeiro mensal de um colaborador no plano de saúde
        com base no perfil demográfico e de saúde informado ao lado.
    </div>
</div>
''', unsafe_allow_html=True)

calcular = st.button('Calcular Previsão de Custo')

# ----------------------------------------------------------------------------
# Resultado
# ----------------------------------------------------------------------------
if calcular:
    colunas_modelo = modelo.feature_names_in_
    dados = {col: 0 for col in colunas_modelo}

    # Dados numéricos
    if 'Idade' in dados: dados['Idade'] = idade
    elif 'idade' in dados: dados['idade'] = idade

    if 'IMC' in dados: dados['IMC'] = imc
    elif 'imc' in dados: dados['imc'] = imc

    if 'Qte_Filhos' in dados: dados['Qte_Filhos'] = filhos
    elif 'qte_filhos' in dados: dados['qte_filhos'] = filhos

    # Categorias
    if sexo == 'Masculino' and 'Sexo_Masculino' in dados: dados['Sexo_Masculino'] = 1
    if fumante == 'Sim' and 'Fumante_Sim' in dados: dados['Fumante_Sim'] = 1
    if regiao == 'Nordeste' and 'Região_Nordeste' in dados: dados['Região_Nordeste'] = 1
    if regiao == 'Norte' and 'Região_Norte' in dados: dados['Região_Norte'] = 1
    if regiao == 'Sudeste' and 'Região_Sudeste' in dados: dados['Região_Sudeste'] = 1

    nome_col_imc = f'Classificacao_IMC_{classificacao_imc}'
    if nome_col_imc in dados:
        dados[nome_col_imc] = 1

    df_predict = pd.DataFrame([dados])[colunas_modelo]
    previsao = modelo.predict(df_predict)[0]

    # ---- Cartão de resultado
    st.markdown(f'''
    <div class="result-card">
        <div class="result-label">Custo mensal estimado</div>
        <div class="result-value"><span>R$</span> {previsao:,.2f}</div>
    </div>
    '''.replace(",", "@").replace(".", ",").replace("@", "."), unsafe_allow_html=True)

    # ---- Cartões de contexto do perfil
    st.markdown(f'''
    <div class="stat-row">
        <div class="stat-card"><div class="k">Idade</div><div class="v">{idade} anos</div></div>
        <div class="stat-card"><div class="k">Sexo</div><div class="v">{sexo}</div></div>
        <div class="stat-card"><div class="k">Filhos</div><div class="v">{filhos}</div></div>
        <div class="stat-card"><div class="k">Fumante</div><div class="v">{fumante}</div></div>
        <div class="stat-card"><div class="k">Região</div><div class="v">{regiao}</div></div>
    </div>
    ''', unsafe_allow_html=True)

    # ---- Painel de escala de IMC
    st.markdown(f'''
    <div class="imc-panel">
        <div class="imc-panel-title">Posição do IMC na escala da OMS — {classificacao_imc}</div>
        {montar_escala_imc(imc)}
    </div>
    ''', unsafe_allow_html=True)

else:
    st.markdown('''
    <div class="empty-card">
        <div class="emoji">📋</div>
        Preencha os dados do colaborador na barra lateral e clique em
        <b>Calcular Previsão de Custo</b> para gerar a estimativa.
    </div>
    ''', unsafe_allow_html=True)

st.markdown(
    '<div class="footer-note">Projeto desenvolvido para portfólio · Modelo preditivo de custos médicos</div>',
    unsafe_allow_html=True
)