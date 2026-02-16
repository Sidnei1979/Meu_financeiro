import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Financeiro Express", page_icon="💰")

# Inicialização do "banco de dados" (na memória para este exemplo)
if 'despesas' not in st.session_state:
    st.session_state.despesas = pd.DataFrame(columns=['Tipo', 'Valor', 'Vencimento', 'Status'])

st.title("💰 Meu Controle Financeiro")

# --- ABA DE CADASTRO ---
with st.expander("➕ Nova Despesa", expanded=True):
    tipo = st.text_input("Tipo de Despesa (ex: Aluguel)")
    valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
    data = st.date_input("Data de Vencimento")
    
    if st.button("Salvar Despesa"):
        nova_linha = pd.DataFrame([[tipo, valor, data, "Pendente"]], 
                                columns=['Tipo', 'Valor', 'Vencimento', 'Status'])
        st.session_state.despesas = pd.concat([st.session_state.despesas, nova_linha], ignore_index=True)
        st.success("Cadastrado com sucesso!")

# --- RESUMO FINANCEIRO ---
df = st.session_state.despesas
total_geral = df['Valor'].sum()
total_pago = df[df['Status'] == 'Pago']['Valor'].sum()
a_pagar = total_geral - total_pago

col1, col2 = st.columns(2)
col1.metric("A Pagar", f"R$ {a_pagar:.2f}")
col2.metric("Total Pago", f"R$ {total_pago:.2f}", delta_color="normal")

# --- LISTAGEM E BAIXA ---
st.subheader("📋 Suas Contas")

for index, row in df.iterrows():
    status_cor = "✅" if row['Status'] == 'Pago' else "⏳"
    col_desc, col_btn = st.columns([3, 1])
    
    with col_desc:
        st.write(f"{status_cor} **{row['Tipo']}** - R$ {row['Valor']:.2f}")
        st.caption(f"Vencimento: {row['Vencimento']}")
    
    with col_btn:
        if row['Status'] == 'Pendente':
            if st.button("Pagar", key=index):
                st.session_state.despesas.at[index, 'Status'] = 'Pago'
                st.rerun()

# --- BOTÃO PARA LIMPAR TUDO ---
if st.sidebar.button("Limpar Histórico"):
    st.session_state.despesas = pd.DataFrame(columns=['Tipo', 'Valor', 'Vencimento', 'Status'])
    st.rerun()
