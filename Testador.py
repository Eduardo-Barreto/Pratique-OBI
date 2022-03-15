import pexpect
import requests
import zipfile
import os


def get_download_url(url_tarefa: str) -> str:
    """
    Função responsável por retornar a url de download do gabarito, de acordo com o link da tarefa.

    Parameters
    ----------
    url_tarefa : str
        Link da tarefa.

    Returns
    -------
    str
        Url de download do gabarito.
    """

    url_tarefa = url_tarefa.strip('/').split('/')
    ano = url_tarefa[-3]
    fase = url_tarefa[-2].strip('f')
    nivel = url_tarefa[-4].strip('p')
    nome = url_tarefa[-1]

    nome_arquivo = f'./{ano}f{fase}p{nivel}_{nome}.zip'
    url_download = f'https://olimpiada.ic.unicamp.br/static/extras/obi{ano}/gabaritos/{nome_arquivo}'

    return url_download


def download_gabarito(url: str) -> str:
    """
    Função responsável por baixar o gabarito da tarefa.

    Parameters
    ----------
    url : str
        Url do gabarito.

    Returns
    -------
    str
        Nome do arquivo baixado.
    """

    nome_original = url.split('_')[-1]

    r = requests.get(url, allow_redirects=True)

    if r.status_code == 200:
        open(nome_original, 'wb').write(r.content)

        with zipfile.ZipFile(nome_original, 'r') as zip_ref:
            zip_ref.extractall('./')

        os.remove(nome_original)
        nome_arquivo = nome_original.strip('.zip')

    else:
        return 'Erro ao baixar o gabarito'

    diretorio = os.listdir(f'./')
    for arquivo in diretorio:
        if nome_arquivo in arquivo:
            nome_arquivo = arquivo

    return nome_arquivo


def testar(path_codigo: str, path_entrada: str, path_saida: str, linhas_saida: int) -> dict:
    """
    Função responsável por testar o código do usuário.

    Parameters
    ----------
    path_codigo : str
        Caminho do arquivo do código do usuário.
    path_entrada : str
        Caminho do arquivo com as entradas.
    path_saida : str
        Caminho do arquivo com as saídas.
    linhas_saida : int
        Quantidade de linhas esperadas para a saída.

    Returns
    -------
    dict
        Dicionário com o status do teste e a saída esperada e encontrada.

    """

    arquivo_entrada = open(path_entrada, 'r')
    arquivo_saida = open(path_saida, 'r')

    entrada = arquivo_entrada.read().strip('\n')
    entrada = entrada.strip()
    saida = arquivo_saida.read().strip('\n')

    child = pexpect.spawn(
        f'python3 {path_codigo}', encoding='utf-8'
    )
    child.sendline(entrada)

    retorno = child.read().strip('\r\n')
    retorno = retorno.split('\r\n')
    retorno = ''.join(retorno[-linhas_saida:])

    child.close()
    arquivo_entrada.close()
    arquivo_saida.close()

    if(retorno == saida):
        status = 'OK'
    else:
        status = 'FALHOU'

    return {'status': status, 'esperado': saida, 'encontrado': retorno, 'arquivo': arquivo_entrada}


def testar_gabarito(url: str, path_codigo: str, linhas_saida: int = 1, silent: bool = False) -> float:
    """
    Função responsável por testar o código do usuário com o gabarito.

    Parameters
    ----------
    url : str
        Url do gabarito.
    path_codigo : str
        Caminho do arquivo do código do usuário.
    linhas_saida : int
        Quantidade de linhas esperadas para a saída.
    silent : bool
        Se True, não printa o resultado de cada teste.

    Returns
    -------
    float
        Taxa de sucesso.

    """

    nome = download_gabarito(get_download_url(url))

    directory = os.listdir(nome)

    contador_testes = 0
    contador_erros = 0
    for conjunto in directory:
        pasta_conjunto = os.listdir(f'./{nome}/{conjunto}')
        entradas = []
        saidas = []
        for teste in pasta_conjunto:
            if 'in' in teste:
                entradas.append(teste)
            else:
                saidas.append(teste)

        for i in range(len(entradas)):
            contador_testes += 1
            if(not silent and i != 0):
                print('------------------------')
            teste = testar(
                path_codigo=path_codigo,
                path_entrada=f'./{nome}/{conjunto}/{entradas[i]}',
                path_saida=f'./{nome}/{conjunto}/{saidas[i]}',
                linhas_saida=linhas_saida
            )
            status = teste['status']

            if(not silent):
                print(f'Teste {contador_testes}: {teste["status"]}, arquivo: {teste["arquivo"].name}')

            if(status == 'FALHOU'):
                contador_erros += 1
                if(not silent):
                    print(
                        f'Esperado: {teste["esperado"]}, encontrado: {teste["encontrado"]}')

    taxa_sucesso = round(100-(contador_erros*100/contador_testes), 2)
    return taxa_sucesso


#taxa_sucesso = testar_gabarito(
    #url='https://olimpiada.ic.unicamp.br/pratique/p2/2007/f1/mobile/',
    #path_codigo='./2007/fase1/mobile.py',
#)

#print(f'Esse código obteve {taxa_sucesso}% de sucesso!')
print(get_download_url('https://olimpiada.ic.unicamp.br/pratique/p2/2007/f1/choc/'))