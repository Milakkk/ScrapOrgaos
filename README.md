# 🏛️ SIORG API Scraper - Documentação

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Async](https://img.shields.io/badge/Asynchronous-Yes-green)
![License](https://img.shields.io/badge/License-MIT-orange)

## 📌 Visão Geral
Script Python assíncrono para extração hierárquica de dados organizacionais do [SIORG](https://siorg.gov.br), com capacidade de:
- Rastrear toda a estrutura de órgãos públicos brasileiros
- Manter relações hierárquicas entre unidades
- Processamento paralelo otimizado

## ⚙️ Funcionalidades Principais
- **Extração em profundidade** (até 10 níveis hierárquicos)
- **Controle de taxa de requisições** (10 simultâneas)
- **Resiliência** a falhas de conexão
- **Saída estruturada** em CSV com:
  - IDs únicos
  - Códigos SIORG
  - Relações pai-filho
  - Níveis hierárquicos

## 📦 Dependências
| Pacote       | Versão   | Instalação          |
|--------------|----------|---------------------|
| aiohttp      | ≥3.8.0   | `pip install aiohttp` |
| pandas       | ≥1.3.0   | `pip install pandas` |
| asyncio      | nativo   | -                   |

## 🛠️ Configuração
1. **Variáveis de ambiente** (opcional):
   ```python
   # Configurações no código:
   SEMÁFORO = asyncio.Semaphore(10)  # Controla requisições simultâneas
   IDS_INICIAIS = [2, 93404]         # IDs raiz: União e Distrito Federal
Headers personalizáveis:

python
HEADERS = {
    "User-Agent": "Seu User-Agent",
    "Accept-Language": "pt-BR"
}
🚀 Execução
bash
python TESTE_ORGAOS.py
Fluxo de trabalho:
Inicia pelos nós raiz (União e DF)

Busca recursivamente todos os filhos

Armazena em memória com relações hierárquicas

Exporta para CSV com codificação Latin-1

📊 Saída Esperada
Arquivo todas_unidades_siorg_com_hierarquia.csv contendo:

ID	Código	Nome	Sigla	Nível	ID Pai
2	00000	União	-	0	-
93404	53000	Distrito Federal	DF	0	-
...	...	...	...	...	...
⚠️ Considerações Importantes
Limitações da API:

Taxa de requisições limitada

Timeout de 30 segundos por chamada

Otimizações:

python
# Evita processamento duplicado
if id_pai in ids_processados:
    return
Dados sensíveis:

Não altere os IDs raiz sem conhecimento da estrutura SIORG
