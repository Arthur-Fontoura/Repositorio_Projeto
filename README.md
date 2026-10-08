# Microbenchmark de Operações de Memória: Comparativo Windows vs. Linux

Repositório público destinado ao armazenamento de artefatos, códigos-fonte, conjuntos de dados e documentação do experimento comparativo de desempenho de memória RAM entre os sistemas operacionais **Windows** e **Linux**.

A investigação integra o escopo da disciplina de **Programação para Ciência de Dados** e fornece evidências quantitativas para subsidiar escolhas de infraestrutura de software em camadas de integração de **Cidades Inteligentes**.

## Protocolo Experimental e Parâmetros

O experimento foi projetado seguindo um protocolo estrito de pré-registro experimental para assegurar a reprodutibilidade dos resultados. A tabela a seguir especifica cada elemento que compõe o desenho experimental do microbenchmark:

| Elemento do Protocolo         | Requisito / Definição                                                                             |
| ----------------------------- | ------------------------------------------------------------------------------------------------- |
| **Sistemas Operacionais**     | Windows e Linux                                                                                   |
| **Operações Medidas**         | Alocação, Escrita, Leitura e Liberação                                                            |
| **Sequência de Execução**     | Alocar $\\rightarrow$ Escrever $\\rightarrow$ Ler $\\rightarrow$ Liberar                          |
| **Faixa de Tamanho de Bloco** | 100 MB a 1.000 MB (passo de 100 MB, totalizando 10 tamanhos)                                      |
| **Número de Repetições**      | 100 testes independentes para cada tamanho de bloco                                               |
| **Volume de Amostras**        | 1.000 registros por sistema operacional (2.000 registros no total)                                |
| **Precisão Temporal**         | Medição em nanossegundos via `time.perf_counter_ns()`, convertida e salva em milissegundos (`ms`) |
| **Formato de Persistência**   | Arquivos CSV com codificação UTF-8                                                                |
| **Esquema do Cabeçalho**      | `bloco_MB,teste,alloc_ms,write_ms,read_m`                                                         |

### Controle de Equivalência do Ambiente

Para garantir o isolamento da variável independente (Sistema Operacional) e a consistência das variáveis controladas (Hardware e Software):

* **Configuração de Hardware**: Execução em máquina física única via *Dual-Boot* ou em duas Máquinas Virtuais (*VMs*) idênticas no mesmo computador hospedeiro com idêntica atribuição de vCPUs e memória RAM.
* **Ambiente Python**: Mesma versão do interpretador Python 3.x instalada em ambos os sistemas.
* **Isolamento de Processos**: Fechamento de todas as aplicações não essenciais em segundo plano durante as rotinas de amostragem.
  ## \. Pré-requisitos e Dependências

Para executar os scripts de coleta, processamento e análise, são necessários a linguagem Python e as bibliotecas especializadas para ciência de dados. As dependências podem ser instaladas diretamente via gerenciador de pacotes `pip`:

```
pip install pandas matplotlib seaborn

```

---

## \. Guia de Reprodução Passo a Passo

A reprodução do experimento é realizada em três etapas sequenciais: amostragem, validação/unificação dos logs e geração da análise estatística.

### Etapa 1: Coleta das Medições (Execução nos dois SOs)

Em cada sistema operacional (Windows e Linux), execute o script de amostragem para gerar os logs de medição:

```
python scripts/medicao_geral.py

```

O script executará o laço de 100 repetições para cada bloco de 100 MB a 1.000 MB, aplicando a sequência de operações:

* **Alocação**: `bloco = bytearray(bloco_bytes)`
* **Escrita**: `bloco[:] = padrao`
* **Leitura**: `soma = sum(bloco)`
* **Liberação**: `bloco.clear()` e `del bloco`

Após a conclusão em cada ambiente, armazene os arquivos na pasta `logs/` com os nomes `logs_windows.csv` e `logs_linux.csv`.

### Etapa 2: Validação e Unificação dos Dados

Execute o script de processamento para aplicar as regras de validação do protocolo e unificar os conjuntos de dados:

```
python scripts/processamento_csv.py

```

O script realiza as seguintes verificações automatizadas:

1. Validação do cabeçalho exato: `bloco_MB,teste,alloc_ms,write_ms,read_ms,free_ms`.
2. Contagem exata de 1.000 registros por arquivo sem células vazias ou valores ausentes.
3. Verificação de valores de tempo não negativos e integridade das sequências de teste (1 a 100).
4. Adição da coluna de identificação do sistema (`Windows` e `Linux`) e exportação da base combinada para `logs/logs_combinados.csv` com formatação padronizada em 6 casas decimais (`float_format='%.6f'`).

### Etapa 3: Análise Estatística e Geração de Gráficos

Para calcular as métricas estatísticas e gerar as visualizações comparativas, execute:

```
python scripts/analise_comparativa.py

```

O script gera os seguintes artefatos analíticos:

* **Tabela de Média e Desvio Padrão** de cada operação por tamanho de bloco e sistema.
* **Diferença Matemática Relativa** entre os tempos calculados para Linux e Windows.
* **`comparativo_final.png`**: Painel $2 \\times 2$ contendo os gráficos de linha por operação com margem de erro baseada no desvio padrão (`errorbar='sd'`).
* **`comparativo_tempo_total.png`**: Gráfico consolidado do tempo total do ciclo de memória ($T\_{\\text{total}} = T\_{\\text{alloc}} + T\_{\\text{write}} + T\_{\\text{read}} + T\_{\\text{free}}$).

  * **Arthur F. Fontoura** — [GitHub](https://github.com/Arthur-Fontoura)
* **Matheus Meggiolaro** — [GitHub](https://github.com/ghostdarkboss1212)
* **Kevin adiel** — [GitHub](https://github.com/kevinadieldasilva-crypto)
