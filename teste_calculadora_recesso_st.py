import datetime
from datetime import date
import pandas as pd  # Importado por padrão, mas usamos 'st' para o Streamlit
import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Calculadora de Recesso", page_icon="⏰", layout="centered")

st.title("📊 Calculadora de Compensação de Horas")
st.markdown("Planeje suas horas extras para garantir o seu recesso de fim de ano.")

# --- ENTRADA DE DADOS (INTERFACE) ---
st.sidebar.header("📋 Configurações")

# 1. Seleção do período de recesso
opcao_recesso = st.sidebar.selectbox(
    "Qual recesso você vai tirar?",
    ["Natal", "Ano Novo"]
)

# Definição da data limite com base na escolha
if opcao_recesso == "Natal":
    end_date = datetime.date(2026, 12, 21)
else:
    end_date = datetime.date(2026, 12, 24)

# 2. Entrada do saldo atual de horas já cumpridas
st.sidebar.subheader("⏱️ Saldo Atual Cumprido")
horas_cumpridas = st.sidebar.number_input("Horas", min_value=0, max_value=100, value=1)
minutos_cumpridos = st.sidebar.number_input("Minutos", min_value=0, max_value=59, value=39)

# --- REGRAS DE NEGÓCIO ---
meta = datetime.timedelta(hours=29)
atual = datetime.timedelta(hours=horas_cumpridas, minutes=minutos_cumpridos)
holidays = [datetime.date(2026, 10, 12), datetime.date(2026, 11, 2), datetime.date(2026, 11, 20)]

# Cálculo dos dias úteis restantes a partir de HOJE
today = date.today()
current = today 
working_days = 0

while current < end_date: # < para não contar o próprio dia de início do recesso
    if current.weekday() < 5:  # Segunda a Sexta
        if current not in holidays:
            working_days += 1
    current += datetime.timedelta(days=1)

# Evita divisão por zero
if working_days == 0:
    working_days = 1

# Cálculo do saldo restante
saldo_restante = meta - atual

# --- EXIBIÇÃO DOS RESULTADOS ---
st.info(f"📅 **Data limite para compensação ({opcao_recesso}):** {end_date.strftime('%d/%m/%Y')}")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Dias Úteis Restantes", value=f"{working_days} dias")
with col2:
    if saldo_restante.total_seconds() > 0:
        tot_seg = int(saldo_restante.total_seconds())
        horas_Faltam = tot_seg // 3600
        min_Faltam = (tot_seg % 3600) // 60
        st.metric(label="Saldo Restante Obrigatório", value=f"{horas_Faltam}h {min_Faltam}min")
    else:
        st.metric(label="Saldo Restante Obrigatório", value="Meta batida! 🎉")

st.subheader("📊 Planejamento Diário")

if saldo_restante.total_seconds() > 0:
    # Média necessária por dia útil
    segundos_por_dia = saldo_restante.total_seconds() / working_days
    horas_diarias = int(segundos_por_dia // 3600)
    minutos_diarios = int((segundos_por_dia % 3600) // 60)
    
    st.warning(f"Você precisa fazer em média **{horas_diarias}h e {minutos_diarios}min** por dia útil para atingir a meta.")
    
    # Progresso visual
    progresso_percentual = min(1.0, atual.total_seconds() / meta.total_seconds())
    st.progress(progresso_percentual)
    st.caption(f"Você já cumpriu {progresso_percentual*100:.1f}% da sua meta de 29 horas.")
else:
    st.success("🚀 Parabéns! Você já acumulou as 29 horas necessárias. Aproveite seu recesso!")
