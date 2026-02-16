import streamlit as st
import pandas as pd
import os

# Configuração da página
st.set_page_config(page_title="Meu Financeiro", page_icon="💰")

# Nome do arquivo onde os dados serão salvos
ARQUIVO_DADOS = "meu_financeiro_dados.csv"

# Função para carregar dados do arquivo CSV
def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        return pd.read_csv(ARQUIVO_DADOS)
    else:
        return pd.DataFrame(columns=['Tipo', 'Valor', 'Vencimento', 'Status'])

# Função para salvar dados no arquivo CSV
def salvar_dados(df):
    df.to_csv(ARQUIVO_DADOS, index=False)

# Inicializa o estado do app com os dados salvos
if 'despesas' not in st.session_state:
    st.session_state.despesas = carregar_dados()

st.title("💰 Meu Controle Financeiro")

# --- ABA DE CADASTRO ---
with st.expander("➕ Nova Despesa", expanded=False):
    tipo = st.text_input("Tipo de Despesa")
    valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
    data = st.date_input("Vencimento")
    
    if st.button("Salvar Despesa"):
        nova_linha = pd.DataFrame([[tipo, valor, str(data), "Pendente"]], 
                                columns=['Tipo', 'Valor', 'Vencimento', 'Status'])
        st.session_state.despesas = pd.concat([st.session_state.despesas, nova_linha], ignore_index=True)
        salvar_dados(st.session_state.despesas)
        st.success("Salvo com sucesso!")
        st.rerun()

# --- RESUMO ---
df = st.session_state.despesas
if not df.empty:
    df['Valor'] = pd.to_numeric(df['Valor'])
    total_pago = df[df['Status'] == 'Pago']['Valor'].sum()
    a_pagar = df[df['Status'] == 'Pendente']['Valor'].sum()

    col1, col2 = st.columns(2)
    col1.metric("A Pagar", f"R$ {a_pagar:.2f}")
    col2.metric("Total Pago", f"R$ {total_pago:.2f}")

    st.divider()

    # --- LISTAGEM ---
    for index, row in df.iterrows():
        status_cor = "✅" if row['Status'] == 'Pago' else "⏳"
        col_text, col_btn = st.columns([3, 1])
        
        with col_text:
            st.write(f"{status_cor} **{row['Tipo']}**")
            st.caption(f"R$ {row['Valor']:.2f} | Venc: {row['Vencimento']}")
        
        with col_btn:
            if row['Status'] == 'Pendente':
                if st.button("Pagar", key=index):
                    st.session_state.despesas.at[index, 'Status'] = 'Pago'
                    salvar_dados(st.session_state.despesas)
                    st.rerun()
else:
    st.info("Nenhuma despesa cadastrada.")

# --- SIDEBAR ---
if st.sidebar.button("Excluir Tudo"):
    if os.path.exists(ARQUIVO_DADOS):
        os.remove(ARQUIVO_DADOS)
    st.session_state.despesas = pd.DataFrame(columns=['Tipo', 'Valor', 'Vencimento', 'Status'])
    st.rerun()
