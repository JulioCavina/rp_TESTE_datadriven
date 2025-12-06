# utils/loaders.py
import io
import pandas as pd
import streamlit as st
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from .format import normalize_dataframe

# Função interna para baixar e processar do Drive
@st.cache_data(ttl=3600, show_spinner="Carregando do Data Lake...")
def fetch_from_drive():
    """
    Conecta ao Google Drive usando st.secrets, baixa o arquivo
    definido em secrets.drive_files.faturamento_xlsx e retorna
    o DataFrame processado e a data da última atualização.
    """
    # 1. Verifica se os secrets existem
    if "gcp_service_account" not in st.secrets or "drive_files" not in st.secrets:
        st.error("❌ Erro: Segredos de configuração (Secrets) não encontrados ou incompletos.")
        return None, None

    try:
        # 2. Configura Credenciais
        service_account_info = dict(st.secrets["gcp_service_account"])
        
        creds = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        
        # 3. Constrói o Serviço
        service = build('drive', 'v3', credentials=creds)
        
        # 4. Obtém o ID do arquivo
        file_id = st.secrets["drive_files"]["faturamento_xlsx"]
        
        # 5. Baixa o arquivo para memória (BytesIO)
        request = service.files().get_media(fileId=file_id)
        file_io = io.BytesIO()
        downloader = MediaIoBaseDownload(file_io, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
        
        file_io.seek(0)
        
        # 6. Lê o Excel e Normaliza
        df_raw = pd.read_excel(file_io, engine="openpyxl")
        df = normalize_dataframe(df_raw)
        
        if df.empty:
            return None, "Dados Vazios"

        # 7. Determina a data de atualização
        file_metadata = service.files().get(fileId=file_id, fields="modifiedTime").execute()
        mod_time_str = file_metadata.get("modifiedTime")
        
        if mod_time_str:
            mod_dt = datetime.strptime(mod_time_str[:19], "%Y-%m-%dT%H:%M:%S")
            ultima_atualizacao = mod_dt.strftime("%d/%m/%Y %H:%M")
        else:
            ultima_atualizacao = datetime.now().strftime("%d/%m/%Y %H:%M")
            
        return df, ultima_atualizacao

    except Exception as e:
        print(f"Erro no Drive: {e}")
        st.error(f"Erro ao conectar com Google Drive: {e}")
        return None, None


def load_main_base():
    """
    Carrega a base principal.
    Prioridade:
    1. Procura em st.session_state (se o usuário fez upload manual na sessão).
    2. Tenta baixar do Google Drive (cacheado por 1h).
    Retorna (df, data_modificação) ou (None, None) se falhar.
    """
    
    # --- 1. Verifica Upload Manual (Override Temporário) ---
    if "uploaded_dataframe" in st.session_state and st.session_state.uploaded_dataframe is not None:
        df = st.session_state.uploaded_dataframe
        data_modificacao = st.session_state.get("uploaded_timestamp", "Upload Manual")
        st.toast("Usando arquivo carregado manualmente.", icon="📂")
        return df, data_modificacao

    # --- 2. Tenta carregar do Drive (Automático) ---
    df_drive, data_drive = fetch_from_drive()
    
    if df_drive is not None:
        return df_drive, data_drive

    # --- 3. Se falhar tudo ---
    return None, None


def load_crowley_base():
    """Placeholder para base Crowley."""
    return None, None