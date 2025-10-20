import streamlit as st
import pandas as pd
import altair as alt

# ---------------------------------------------------------
# CONFIGURAÇÃO BÁSICA
# ---------------------------------------------------------
st.set_page_config(page_title="Evolução Populacional e Mortalidade", layout="wide")

st.title("📊 Crescimento e Mortalidade Populacional ao Longo da História")
st.write("""
Esta aplicação mostra como a população mundial evoluiu ao longo dos séculos, 
com base em dados históricos e estimativas globais. 
Também analisa a taxa de mortalidade e os eventos que mais impactaram o crescimento humano.
""")

# ---------------------------------------------------------
# CARREGAR DADOS
# ---------------------------------------------------------
url = "https://raw.githubusercontent.com/datasets/population/master/data/population.csv"
dados = pd.read_csv(url)

# ---------------------------------------------------------
# CRIAR ABAS
# ---------------------------------------------------------
aba1, aba2 = st.tabs(["🌍 Visão Global", "🇨🇳 Comparar Países"])

# ---------------------------------------------------------
# 🌍 ABA 1 – VISÃO GLOBAL
# ---------------------------------------------------------
with aba1:
    dados_mundo = dados[dados['Country Name'] == 'World']

    st.subheader("🌍 Dados Históricos de População Mundial")
    st.dataframe(dados_mundo.tail(10))

    st.subheader("📈 Crescimento da População Mundial (1960 - Atual)")

    grafico_pop = alt.Chart(dados_mundo).mark_area(color='lightblue').encode(
        x=alt.X('Year:O', title='Ano'),
        y=alt.Y('Value:Q', title='População Mundial'),
        tooltip=['Year', alt.Tooltip('Value', format=',.0f')]
    ).properties(width=800, height=400)

    st.altair_chart(grafico_pop, use_container_width=True)

    st.subheader("⚰️ Taxa Global de Mortalidade (estimativa histórica)")

    mortality = pd.DataFrame({
        'Ano': list(range(1800, 2021, 10)),
        'Taxa de Mortalidade (%)': [25, 22, 20, 18, 15, 13, 12, 11, 10, 9, 8, 7, 6, 5, 5, 4, 3, 3, 2.5, 2.3, 2.1, 1.9, 1.8]
    })

    grafico_morte = alt.Chart(mortality).mark_line(point=True, color='crimson').encode(
        x='Ano:O',
        y='Taxa de Mortalidade (%):Q',
        tooltip=['Ano', 'Taxa de Mortalidade (%)']
    ).properties(width=800, height=400)

    st.altair_chart(grafico_morte, use_container_width=True)

    st.subheader("🕰️ Contexto Histórico")
    st.markdown("""
    - **Antes de 1800:** Alta mortalidade infantil e doenças infecciosas limitavam o crescimento.  
    - **1850–1950:** Revolução Industrial e avanços médicos aumentaram a expectativa de vida.  
    - **Após 1950:** Medicina moderna e globalização impulsionaram o crescimento.  
    - **Hoje:** Desafios com sustentabilidade e envelhecimento populacional.
    """)

    st.info("""
    O crescimento populacional humano reflete nossa capacidade de adaptação, 
    mas traz desafios de sustentabilidade e recursos limitados.
    """)

# ---------------------------------------------------------
# 🇨🇳 ABA 2 – COMPARAR PAÍSES
# ---------------------------------------------------------
with aba2:
    st.subheader("🇺🇳 Comparação de Crescimento Populacional entre Países")

    # Lista de países disponíveis
    paises = sorted(dados['Country Name'].unique())

    col1, col2 = st.columns(2)
    with col1:
        pais1 = st.selectbox("Selecione o primeiro país:", paises, index=paises.index("Brazil") if "Brazil" in paises else 0)
    with col2:
        pais2 = st.selectbox("Selecione o segundo país:", paises, index=paises.index("China") if "China" in paises else 1)

    # Filtrando dados
    dados_pais1 = dados[dados['Country Name'] == pais1]
    dados_pais2 = dados[dados['Country Name'] == pais2]

    # Mesclando para tabela comparativa
    comparacao = pd.merge(
        dados_pais1[['Year', 'Value']].rename(columns={'Value': f'População - {pais1}'}),
        dados_pais2[['Year', 'Value']].rename(columns={'Value': f'População - {pais2}'}),
        on='Year'
    )

    st.dataframe(comparacao.tail(10))

    # Gráfico comparativo
    st.subheader("📊 Comparação Gráfica")

    grafico_comp = alt.Chart(
        pd.concat([
            dados_pais1.assign(País=pais1),
            dados_pais2.assign(País=pais2)
        ])
    ).mark_line(point=True).encode(
        x=alt.X('Year:O', title='Ano'),
        y=alt.Y('Value:Q', title='População'),
        color='País:N',
        tooltip=['País', 'Year', alt.Tooltip('Value', format=',.0f')]
    ).properties(width=800, height=400)

    st.altair_chart(grafico_comp, use_container_width=True)

    st.subheader("📘 Análise e Contexto")
    st.markdown(f"""
    - **{pais1}** e **{pais2}** apresentam trajetórias populacionais distintas, influenciadas por fatores históricos, econômicos e sociais.  
    - Em países como **{pais2}**, políticas de natalidade e industrialização aceleraram o crescimento no século XX.  
    - Já em **{pais1}**, o crescimento foi mais estável, ligado a melhorias graduais em saúde e economia.  
    - O gráfico permite observar **picos, quedas ou estagnações** associadas a eventos históricos.
    """)

