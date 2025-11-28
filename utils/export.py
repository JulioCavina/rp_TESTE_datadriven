# utils/export.py

import io
import zipfile
import pandas as pd
import re

def clean_sheet_name(name):
    """
    Remove caracteres inválidos para nomes de abas do Excel 
    e limita a 31 caracteres.
    """
    # Remove caracteres proibidos: [ ] : * ? / \
    clean = re.sub(r'[\[\]:*?/\\]', '', str(name))
    # Limita tamanho a 31 chars (limite do Excel)
    return clean[:31]

def to_excel_with_images(data_dict, filter_info):
    """
    Gera um arquivo Excel em memória contendo DataFrames e Imagens (Plots).
    """
    output = io.BytesIO()
    
    # Usa xlsxwriter como engine pois é o melhor para inserir imagens
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        # --- ABA 1: RESUMO / FILTROS ---
        df_info = pd.DataFrame([{"Filtros Aplicados": filter_info}])
        df_info.to_excel(writer, sheet_name="Resumo", index=False)
        worksheet_resumo = writer.sheets["Resumo"]
        # Ajusta largura da coluna
        worksheet_resumo.set_column('A:A', 100)
        
        # --- ABAS DE DADOS E GRÁFICOS ---
        for key, value in data_dict.items():
            sheet_name = clean_sheet_name(key)
            
            # 1. Se for Tabela (DataFrame)
            if 'df' in value and value['df'] is not None and not value['df'].empty:
                value['df'].to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Ajuste básico de largura de colunas
                worksheet = writer.sheets[sheet_name]
                worksheet.set_column('A:Z', 18)

            # 2. Se for Gráfico (Plotly Figure)
            elif 'fig' in value and value['fig'] is not None:
                # Cria uma aba vazia apenas para o gráfico
                # (Ou cria um DF vazio para gerar a aba)
                pd.DataFrame().to_excel(writer, sheet_name=sheet_name)
                worksheet = writer.sheets[sheet_name]
                
                try:
                    # Converte o gráfico Plotly para bytes PNG usando Kaleido
                    # scale=2 melhora a resolução
                    img_bytes = value['fig'].to_image(format="png", width=1000, height=600, scale=2, engine="kaleido")
                    
                    # Cria um buffer de imagem para o xlsxwriter
                    image_stream = io.BytesIO(img_bytes)
                    
                    # Insere a imagem na célula A1
                    worksheet.insert_image('A1', f'{sheet_name}.png', {'image_data': image_stream})
                except Exception as e:
                    print(f"Erro ao converter imagem {key}: {e}")
                    worksheet.write('A1', f"Erro ao gerar imagem: {e}")

    return output.getvalue()

def create_zip_package(data_dict, filter_info):
    """
    Empacota o arquivo Excel gerado dentro de um arquivo ZIP.
    """
    # 1. Gera o Excel em memória
    excel_data = to_excel_with_images(data_dict, filter_info)
    
    # 2. Cria o ZIP em memória
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        # Define o nome do arquivo Excel dentro do zip
        zip_file.writestr("Relatorio_Completo.xlsx", excel_data)
    
    return zip_buffer.getvalue()