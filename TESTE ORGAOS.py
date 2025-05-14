import aiohttp
import asyncio
import pandas as pd

# URL base da API
BASE_URL = "https://siorg.gov.br/siorg-cidadao-webapp/api/arvore/filhos?origem=VIVA&idPai="

# Definir os headers corretos
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Referer": "https://siorg.gov.br/siorg-cidadao-webapp/resources/app/relatorio-dinamico.html"
}

# Lista para armazenar as unidades extraídas
unidades = []
ids_processados = set()
ids_pendentes = []

# Limite de requisições simultâneas
SEMÁFORO = asyncio.Semaphore(10)  # Limita a 10 requisições simultâneas


async def buscar_unidades(session, id_pai, nivel=0):
    """Busca unidades de forma assíncrona e adiciona novos IDs à fila."""
    if id_pai in ids_processados:
        return

    async with SEMÁFORO:  # Controla a taxa de requisições
        url = BASE_URL + str(id_pai)
        async with session.get(url, headers=HEADERS) as response:
            if response.status == 200:
                data = await response.json()
                for item in data:
                    unidade_id = item.get("id")
                    unidade_codigo = item.get("codigo")
                    unidade_nome = item.get("denominacao")
                    unidade_sigla = item.get("sigla")
                    possui_filhos = item.get("possuiFilhos", False)

                    if unidade_id and unidade_nome:
                        unidades.append({
                            "ID": unidade_id,
                            "Código": unidade_codigo,
                            "Nome": unidade_nome,
                            "Sigla": unidade_sigla,
                            "Nível": nivel,
                            "ID Pai": id_pai  # NOVA COLUNA para indicar a origem
                        })
                        print(unidade_nome)

                        # Adiciona os filhos para buscar depois
                        if possui_filhos and unidade_id not in ids_processados:
                            ids_pendentes.append((unidade_id, nivel + 1))

        ids_processados.add(id_pai)


async def coletar_todas_unidades():
    """Gerencia a busca assíncrona em toda a árvore."""
    async with aiohttp.ClientSession() as session:
        while ids_pendentes:
            tarefas = [buscar_unidades(session, id_atual, nivel_atual) for id_atual, nivel_atual in ids_pendentes[:10]]
            ids_pendentes[:10] = []  # Remove os primeiros 10 processados
            await asyncio.gather(*tarefas)  # Executa as requisições em paralelo


# **IDs iniciais:** "União" e "Distrito Federal"
IDS_INICIAIS = [2, 93404]
ids_pendentes.extend([(id_inicial, 0) for id_inicial in IDS_INICIAIS])

# Iniciar a busca assíncrona
print("🚀 Buscando unidades de forma otimizada...")
asyncio.run(coletar_todas_unidades())

# Salvar os dados em um CSV com a coluna "ID Pai"
df = pd.DataFrame(unidades)
df.to_csv("todas_unidades_siorg_com_hierarquia.csv", index=False, encoding="ISO-8859-1")
print("✅ Unidades salvas em 'todas_unidades_siorg_com_hierarquia.csv' 🚀")
