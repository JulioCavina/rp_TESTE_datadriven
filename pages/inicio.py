# pages/inicio.py
import streamlit as st
import pandas as pd

def render(df=None):
    st.markdown("### Bem-vindo ao Sistema de Inteligência de Mercado")
    
    # Status da base (se carregada)
    if df is not None and not df.empty:
        total_linhas = len(df)
        
        # Tenta pegar a data de atualização mais recente
        if "data_ref" in df.columns:
            max_date = df["data_ref"].max()
            data_str = max_date.strftime("%d/%m/%Y") if pd.notna(max_date) else "N/A"
        else:
            data_str = "Desconhecida"
            
        st.info(f"✅ Base de Vendas carregada com sucesso! | Registros: {total_linhas} | Última referência: {data_str}")
    
    st.markdown("---")
    st.markdown("##### Selecione um módulo para iniciar:")

    # Estilo dos Cards (CSS Inline para garantir funcionamento rápido no componente)
    card_style = """
    <div style="
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 20px;
        height: 100%;
        background-color: white;
        transition: transform 0.2s, box-shadow 0.2s;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    " onmouseover="this.style.transform='translateY(-5px)';this.style.boxShadow='0 4px 10px rgba(0,0,0,0.1)'" 
       onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='none'">
        <div>
            <h4 style="color: #004a99; margin-bottom: 10px;">{title}</h4>
            <p style="color: #666; font-size: 0.9rem;">{desc}</p>
        </div>
        <a href="?nav={nav_idx}" target="_self" style="
            display: inline-block;
            margin-top: 15px;
            text-decoration: none;
            color: white;
            background-color: #007bff;
            padding: 8px 16px;
            border-radius: 5px;
            text-align: center;
            font-weight: 600;
            font-size: 0.85rem;
        ">Acessar &rarr;</a>
    </div>
    """

    # Layout em Grid (2 Colunas para melhor visualização)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(card_style.format(
            title="Visão Geral", 
            desc="KPIs principais, atingimento de metas e performance geral.", 
            nav_idx=1
        ), unsafe_allow_html=True)
        
    with c2:
        st.markdown(card_style.format(
            title="Clientes & Faturamento", 
            desc="Detalhamento por agência, cliente, executivo e tabelas completas.", 
            nav_idx=2
        ), unsafe_allow_html=True)

    with c3:
        st.markdown(card_style.format(
            title="Perdas & Ganhos", 
            desc="Análise de Churn, novos clientes e recuperação.", 
            nav_idx=3
        ), unsafe_allow_html=True)
        
    with c4:
        st.markdown(card_style.format(
            title="Relatório Crowley", 
            desc="Monitoramento musical, spots e concorrência (Rádio).", 
            nav_idx=8  # Index 8 na lista pages_keys
        ), unsafe_allow_html=True)

    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)

    c5, c6, c7, c8 = st.columns(4)

    with c5:
        st.markdown(card_style.format(
            title="Cruzamentos", 
            desc="Clientes exclusivos vs. compartilhados entre emissoras.", 
            nav_idx=4
        ), unsafe_allow_html=True)

    with c6:
        st.markdown(card_style.format(
            title="Top 10", 
            desc="Ranking dos maiores anunciantes e setores.", 
            nav_idx=5
        ), unsafe_allow_html=True)
        
    with c7:
        st.markdown(card_style.format(
            title="Relatório ABC", 
            desc="Curva de Pareto (80/20) e concentração de carteira.", 
            nav_idx=6
        ), unsafe_allow_html=True)
        
    with c8:
        st.markdown(card_style.format(
            title="Eficiência", 
            desc="Preço médio, ocupação e eficiência comercial.", 
            nav_idx=7
        ), unsafe_allow_html=True)