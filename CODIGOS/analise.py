import pandas as pd
import os

def processar_csv(caminho_arquivo, nome_so):
    
    #Lê o arquivo CSV, converte tipos de dados e realiza validações básicas.
    print(f"\n--- Iniciando o processamento do arquivo: {caminho_arquivo} ({nome_so}) ---")

    # Passo 1: Verificar se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        print(f"ERRO: Arquivo '{caminho_arquivo}' não encontrado.")
        return None

    # Passo 2: Leitura do arquivo
    df = pd.read_csv(caminho_arquivo)
    print("Leitura concluída com sucesso.")

    # Passo 3: Adicionar a coluna de identificação do SO
    df['sistema'] = nome_so

    # --- CONVERSÃO DE TIPOS ---
    print("Convertendo e verificando tipos de dados...")
    
    # Garantir que bloco_MB e teste sejam inteiros
    df['Tamanho_MB'] = df['Tamanho_MB'].astype(int)
    df['Repeticao'] = df['Repeticao'].astype(int)

    # --- VALIDAÇÕES DOS DADOS ---
    erros_validacao = 0

    # Verifica quantidade de registros
    qtd_registros = len(df)
    if qtd_registros != 4000:
        print(f"ERRO DE VALIDAÇÃO: Quantidade de registros incorreta. Encontrado: {qtd_registros}, Esperado: 1000.")
        erros_validacao += 1
    
    # Verifica tempos negativos
    colunas_tempo = ['Tempo_ms']
    for col in colunas_tempo:
        if (df[col] < 0).any():
            print(f"ERRO DE VALIDAÇÃO: Tempos negativos encontrados na coluna {col}.")
            erros_validacao += 1

    if erros_validacao == 0:
        print(f"Processamento e validações do {nome_so} concluídos sem erros.")
        return df
    else:
        print(f"Processamento abortado para {nome_so} devido a erros de validação.")
        return None


# --- FLUXO PRINCIPAL ---
arquivo_windows = 'CSVs/resultados_microbenchmark windows.csv'
arquivo_linux = 'CSVs/resultados_microbenchmark linux.csv'

# Processa e valida cada arquivo individualmente
df_win = processar_csv(arquivo_windows, 'Windows')
df_lin = processar_csv(arquivo_linux, 'Linux')



# Combinar arquivos
if df_win is not None and df_lin is not None:
    print("\n--- Combinando os dados ---")
    df_completo = pd.concat([df_win, df_lin], ignore_index=True)
    
    # Salvar o resultado final em um novo arquivo
    arquivo_saida = 'CSVs/resultado_combinado.csv'
    df_completo.to_csv(arquivo_saida, index=False)
    print(f"Dados unificados salvos com sucesso em: '{arquivo_saida}'")
    
    # Demonstração de que os dados estão prontos
    print("\nAmostra dos dados processados:")
    print(df_completo.head())
    print("\nInformações do DataFrame unificado:")
    print(df_completo.info())
else:
    print("\nFalha na validação de um ou ambos os arquivos. A combinação não foi realizada.")
    print("Corrija os erros apontados antes de prosseguir.")