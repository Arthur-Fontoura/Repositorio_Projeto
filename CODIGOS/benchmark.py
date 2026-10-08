import time
import csv
import os
import gc

# Configurações do benchmark
TAMANHOS_MB = range(100, 1001, 100)
REPETICOES = 100
ARQUIVO_CSV = "resultados_microbenchmark.csv"

# Tamanho do bloco utilizado para escrita/leitura
BLOCO = 1024 * 1024  # 1 MB


def medir_tempo(funcao):
    """Executa uma função e retorna o tempo gasto em milissegundos."""
    inicio = time.perf_counter()
    funcao()
    fim = time.perf_counter()

    return (fim - inicio) * 1000


def benchmark():
    resultados = []

    print("Iniciando microbenchmark...")
    print(f"Repetições por tamanho: {REPETICOES}")
    print("-" * 60)

    for tamanho_mb in TAMANHOS_MB:

        tamanho_bytes = tamanho_mb * 1024 * 1024

        print(f"Testando {tamanho_mb} MB...")

        for repeticao in range(1, REPETICOES + 1):

            dados = None

            # ---------------------------------
            # 1. ALOCAÇÃO
            # ---------------------------------
            inicio = time.perf_counter()

            dados = bytearray(tamanho_bytes)

            fim = time.perf_counter()

            tempo_alocacao = (fim - inicio) * 1000

            resultados.append([
                tamanho_mb,
                repeticao,
                "alocacao",
                tempo_alocacao
            ])

            # ---------------------------------
            # 2. ESCRITA
            # ---------------------------------
            inicio = time.perf_counter()

            dados[:] = b'\xAA' * tamanho_bytes

            fim = time.perf_counter()

            tempo_escrita = (fim - inicio) * 1000

            resultados.append([
                tamanho_mb,
                repeticao,
                "escrita",
                tempo_escrita
            ])

            # ---------------------------------
            # 3. LEITURA
            # ---------------------------------
            inicio = time.perf_counter()

            soma = 0

            # Leitura em blocos de 1 MB
            for inicio_bloco in range(0, tamanho_bytes, BLOCO):
                fim_bloco = min(inicio_bloco + BLOCO, tamanho_bytes)
                soma += sum(dados[inicio_bloco:fim_bloco])

            fim = time.perf_counter()

            tempo_leitura = (fim - inicio) * 1000

            resultados.append([
                tamanho_mb,
                repeticao,
                "leitura",
                tempo_leitura
            ])

            # Evita que o Python otimize/remova a leitura
            _ = soma

            # ---------------------------------
            # 4. LIBERAÇÃO
            # ---------------------------------
            inicio = time.perf_counter()

            del dados
            gc.collect()

            fim = time.perf_counter()

            tempo_liberacao = (fim - inicio) * 1000

            resultados.append([
                tamanho_mb,
                repeticao,
                "liberacao",
                tempo_liberacao
            ])

    # -----------------------------------------
    # SALVAR RESULTADOS NO CSV
    # -----------------------------------------

    with open(
        ARQUIVO_CSV,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        escritor = csv.writer(arquivo)

        escritor.writerow([
            "Tamanho_MB",
            "Repeticao",
            "Operacao",
            "Tempo_ms"
        ])

        escritor.writerows(resultados)

    print("-" * 60)
    print("Benchmark concluído!")
    print(f"Resultados salvos em: {os.path.abspath(ARQUIVO_CSV)}")


if __name__ == "__main__":
    benchmark()