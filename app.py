import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client, Client

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Ler as credenciais do Supabase a partir das variáveis de ambiente
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Verifique se as variáveis de ambiente foram carregadas corretamente
if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("As credenciais do Supabase não foram encontradas. Verifique as variáveis de ambiente.")
else:
    # Função para iniciar a conexão com Supabase
    def init_connection():
        return create_client(SUPABASE_URL, SUPABASE_KEY)

    supabase: Client = init_connection()

    # Consulta na tabela
    @st.cache_data
    def load_data():
        response = supabase.table("iot_temp_log").select("*").execute()
        data = response.data
        return pd.DataFrame(data)

    df = load_data()

    # Mostrando os dados em um DataFrame
    st.title("Dados de Temperatura IoT")
    st.write(df)

    # Convertemos a coluna de data para formato datetime
    df['noted_date'] = pd.to_datetime(df['noted_date'])

    # Gráfico 1: Temperatura ao longo do tempo
    st.header("Temperatura ao longo do tempo")
    fig1 = px.line(df, x='noted_date', y='temp', title="Evolução da Temperatura")
    st.plotly_chart(fig1)

    # Gráfico 2: Distribuição das temperaturas por ambiente (In/Out)
    st.header("Distribuição das Temperaturas por Ambiente")
    fig2 = px.histogram(df, x='temp', color='out/in', barmode='overlay', title="Temperatura por In/Out")
    st.plotly_chart(fig2)

    # Gráfico 3: Média de temperatura por ambiente (In/Out)
    st.header("Média de Temperatura por Ambiente")
    df_mean = df.groupby('out/in')['temp'].mean().reset_index()
    fig3 = px.bar(df_mean, x='out/in', y='temp', title="Média de Temperatura por Ambiente (In/Out)")
    st.plotly_chart(fig3)
