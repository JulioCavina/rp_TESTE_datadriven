# pages/inicio.py
import streamlit as st
import pandas as pd

def render(df=None):
    st.markdown("### Bem-vindo ao Sistema de Inteligência de Mercado")
    st.markdown("---")
    st.markdown("##### Selecione um módulo para iniciar:")

    # Navegação via botões padrão
    # IDs de navegação baseados na lista 'pages_keys' do streamlit_app.py
    # 1: Visão Geral, 2: Clientes, 3: Perdas, 4: Cruzamentos, 5: Top 10, 6: ABC, 7: Eficiência, 8: Crowley

    # Linha 1
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown("#### 📊 Visão Geral")
        st.caption("Resumo executivo")
        if st.button("Acessar", key="btn_visao", use_container_width=True):
            st.query_params["nav"] = "1"
            st.rerun()

    with c2:
        st.markdown("#### 👥 Clientes & Fat.")
        st.caption("Detalhamento comercial")
        if st.button("Acessar", key="btn_clientes", use_container_width=True):
            st.query_params["nav"] = "2"
            st.rerun()

    with c3:
        st.markdown("#### 📉 Perdas & Ganhos")
        st.caption("Churn e Novos")
        if st.button("Acessar", key="btn_perdas", use_container_width=True):
            st.query_params["nav"] = "3"
            st.rerun()
            
    with c4:
        st.markdown("#### 🔀 Cruzamentos")
        st.caption("Exclusivos vs Comp.")
        if st.button("Acessar", key="btn_cruz", use_container_width=True):
            st.query_params["nav"] = "4"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Linha 2
    c5, c6, c7, c8 = st.columns(4)

    with c5:
        st.markdown("#### 🏆 Top 10")
        st.caption("Ranking Anunciantes")
        if st.button("Acessar", key="btn_top10", use_container_width=True):
            st.query_params["nav"] = "5"
            st.rerun()
        
    with c6:
        st.markdown("#### 🅰️ Relatório ABC")
        st.caption("Pareto (80/20)")
        if st.button("Acessar", key="btn_abc", use_container_width=True):
            st.query_params["nav"] = "6"
            st.rerun()
        
    with c7:
        st.markdown("#### ⚡ Eficiência")
        st.caption("KPIs e Ocupação")
        if st.button("Acessar", key="btn_efi", use_container_width=True):
            st.query_params["nav"] = "7"
            st.rerun()
            
    with c8:
        st.markdown("#### 📻 Relatório Crowley")
        st.caption("Monitoramento Musical")
        if st.button("Acessar", key="btn_crowley", use_container_width=True):
            st.query_params["nav"] = "8"
            st.rerun()