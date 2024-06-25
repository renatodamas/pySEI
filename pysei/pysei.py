import os
import re
from bs4 import BeautifulSoup
import requests
import urllib3
import warnings


urllib3.disable_warnings()

URL_SEI = ''  # Especificada em SEI.__init__


class ErroLogin(Exception):
    pass


class ProcessoSei:
    def __init__(self, session, html):
        self.session = session
        self.html = html
        self._arvore = None
        self._acoes = None
        self._documentos = {}

    @property
    def metadata(self):
        metadata = {}
        url = [i for i in self.acoes if 'consultar' in i][0]
        html = self.session.get(url, verify=False, timeout=60).text
        data_html = BeautifulSoup(html, 'lxml')

        sel_assuntos = data_html.find('select', {'id': 'selAssuntos'})
        assuntos = [i.text for i in sel_assuntos.find_all('option')]
        metadata['assuntos'] = assuntos

        sel_interessado = data_html.find('select', {'id': 'selInteressadosProcedimento'})
        interessados = [i.text for i in sel_interessado.find_all('option')]
        metadata['interessados'] = interessados

        especificacao = data_html.find('input', {'id': 'txtDescricao'})['value']
        metadata['especificacao'] = especificacao

        select_tipo = data_html.find('select', {'id': 'selTipoProcedimento'})
        tipo = select_tipo.find('option', {'selected': 'selected'}).text
        metadata['tipo'] = tipo

        protocolo = data_html.find('input', {'id': 'txtProtocoloExibir'})['value']
        metadata['protocolo'] = protocolo

        dt_autuacao = data_html.find('input', {'id': 'txtDtaGeracaoExibir'})['value']
        metadata['data_autuacao'] = dt_autuacao

        metadata['documentos'] = self.documentos
        return metadata

    @property
    def arvore(self):
        if self._arvore is None:
            soup = BeautifulSoup(self.html, 'lxml')
            body = soup.html.find('body', recursive=False)
            src = body.find('iframe', {'id': 'ifrArvore'})['src']
            url = URL_SEI + src
            r = self.session.get(url, verify=False, timeout=60)
            self._arvore = r.text
        return self._arvore

    @property
    def acoes(self):
        if self._acoes is None:
            html = self.arvore
            acoes = re.search(r"(?<=Nos\[0\].acoes = ').*", html).group()
            self._acoes = [URL_SEI + i for
                           i in re.findall(r'(?<=href=").*?(?="\stabindex)', acoes)]
        return self._acoes

    @property
    def documentos(self):
        if self._documentos == {}:
            html = self.arvore

            pattern_urls = r'(?<=Nos\[[0-999]\].src\s=\s\').*(?=\';)'
            urls_arvore = re.findall(pattern_urls, html)[1:]

            pattern = r'(?<=Nos\[[0-999]\] = new infraArvoreNo\().*(?=\))'
            nos_arvore = re.findall(pattern, html)[1:]

            for i in ['",'.join(i) for i in zip(nos_arvore, urls_arvore)]:
                doc = Documento(self.session, i)
                self._documentos[doc.number] = doc
        return self._documentos

    def download_pdf(self, filename=None):
        if filename is None:
            filename = 'download_sei.pdf'
        self._download(filetype='pdf', filename=filename)

    def download_zip(self, path=None, filename=None):
        if filename is None:
            filename = 'download_sei.zip'
        self._download(filetype='zip', path=path, filename=filename)

    def _download(self, filetype, path=None, filename='download_sei.pdf'):
        url = [i for i in self.acoes if filetype in i][0]
        r = self.session.get(url, verify=False, timeout=60)
        soup = BeautifulSoup(r.content, 'lxml').html.find('body', recursive=False)
        url_gera_pdf = URL_SEI + soup.find('form')['action']
        # params para o post
        params = {i['id']: i['value'] for
                  i in soup.find_all('input')[:-1]
                  if i.get('type', None) == 'hidden'}
        params['hdnFlagGerar'] = 1

        for n, item in enumerate(params['hdnInfraItens'].split(',')):
            params['chkInfraItem{}'.format(n)] = item
        r = self.session.post(url_gera_pdf, verify=False, data=params, timeout=60)
        url_pdf = re.search(r'(?<=window.open\(\').*(?=\'\))', r.text).group()
        r = self.session.get(URL_SEI + url_pdf, verify=False, timeout=120)
        download_content = r.content

        if r.headers.get('Content-Disposition', None) is not None:
            filename = r.headers.get('Content-Disposition').split('"')[-2]

        if path is not None:
            filename = os.path.join(path, filename)

        with open(filename, 'wb') as f:
            f.write(download_content)


class ResultadoPesquisa:
    def __init__(self, session, html):
        self.session = session
        self.html = html


class Documento:
    def __init__(self, session, attributes: str):
        self.session = session
        self.attributes = attributes
        self.parse_attributes(self.attributes)

    def parse_attributes(self, attributes):
        attrs = attributes.replace('",', '|').replace('"', '').split('|')
        self.url = URL_SEI + attrs[-1]
        self.name = attrs[5]
        # number_pattern = '(?<=\s)[0-9]*$|(?<=\()[0-9]{1,8}(?!\))'
        self.number = attrs[5].split(' ')[-1].replace('(', '').replace(')', '')

    @property
    def filename(self):
        r = self.session.head(self.url)
        filename = r.headers.get('Content-Disposition', None)
        if filename:
            filename = re.search(r'(?<=filename=").*(?=")', filename).group()
        return filename

    @property
    def contents(self):
        r = self.session.get(self.url)
        return r.content

    def to_file(self, filename=''):
        if filename != '':
            outfile = filename
        else:
            outfile = self.filename or self.name

        with open(outfile, 'wb') as f:
            f.write(self.contents)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self.__class__) + self.name


class SEI():

    def __init__(self, url_sei):
        """
        :param url_sei: Endereço da página inicial do SEI do tipo 'https://seimp.planejamento.gov.br/sei/'
        """
        global URL_SEI
        URL_SEI = url_sei
        self.session = requests.Session()
        self._form_url = None

    def login(self, username, password, id_orgao=0, id_unidade=0):
        self.username = username
        self.password = password

        if self.is_online is False:
            raise SystemError('SEI offline.')

        # 1 - Página inicial
        r = self.session.get(URL_SEI, verify=False, allow_redirects=True)
        url_login_php = r.url
        soup = BeautifulSoup(r.text, 'lxml')

        # 2 - Captura o hndToken'
        # r = self.session.get(url_login_php)
        # self.hdn_token = soup.find('input', {'id': re.compile('hdnToken')})

        # 3 - Envia o form de Login'
        data = {
            'txtUsuario': self.username,
            'pwdSenha': self.password,
            'selOrgao': id_orgao,
            'selInfraUnidades': id_unidade,  # quando o usuário está habilitado para mais de uma unidade
            'Acessar': '',
            'hdnAcao': 2,
            # self.hdn_token['name']: self.hdn_token['value']
        }

        r = self.session.post(url_login_php, data=data, verify=False)

        try:
            soup = BeautifulSoup(r.content, 'lxml')
            self.user = soup.find('a', {'id': 'lnkUsuarioSistema'})['title']

        except TypeError:
            warnings.warn('Erro no login')
            return False

        self.html = r.content
        with open('after_login.html', 'wb') as f:
            f.write(self.html)
        return True

    def trocar_unidade(self, id_unidade: int):
        r = self.session.post(URL_SEI, data={'selInfraUnidades': id_unidade}, allow_redirects=True)
        return 200 <= r.status_code < 400

    @property
    def is_online(self):
        r = requests.get(URL_SEI, verify=False, allow_redirects=False)
        return 200 <= r.status_code < 400

    def acessa_tela_pesquisa(self):
        soup = BeautifulSoup(self.html, 'lxml')
        menu = soup.find('a', {'link':"protocolo_pesquisar"})
        url_pesquisa = URL_SEI + menu['href']
        print(url_pesquisa)
        r = self.session.get(url_pesquisa, verify=False)
        return r.text

    @property
    def form_URL(self):
        if self._form_url is None:
            self._form_url = self.get_form_URL()
        return self._form_url

    def get_form_URL(self):
        html = self.acessa_tela_pesquisa()
        soup = BeautifulSoup(html, 'lxml')
        url_pesquisa = soup.find('form', {'id': 'frmPesquisaProtocolo'})['action']
        return URL_SEI + url_pesquisa

    def pesquisa(self, query='', numero_sei='', pesquisar_documentos=True, doc_gerados=True, doc_externos=True,
                 com_tramitacao=False, id_orgao_gerador='', id_unidade_geradora='', id_assunto='',
                 id_usuario_assinatura='', id_contato='', interessado=True, remetente=True, destinatario=True,
                 descricao='', observacao_unidade='', id_tipo_processo='', id_tipo_documento='', numero_nome_arvore='',
                 data_inicial='', data_final='', usuario_gerador1='', usuario_gerador2='', usuario_gerador3=''):

        data = {
            'hdnInfraTipoPagina': '1',
            'sbmPesquisar': 'Pesquisar',
            'rdoPesquisarEm': 'D' if pesquisar_documentos else 'P',
            'chkSinDocumentosGerados': 'S' if doc_gerados else '',
            'chkSinDocumentosRecebidos': 'S' if doc_externos else '',
            'chkSinProcessosTramitacao': 'S' if com_tramitacao else '',
            'q': query,
            'txtUnidade': '',
            'hdnIdUnidade': id_unidade_geradora,
            'txtAssunto': '',
            'hdnIdAssunto': id_assunto,
            'txtAssinante': '',
            'hdnIdAssinante': id_usuario_assinatura,
            'txtContato': '',
            'hdnIdContato': id_contato,
            'chkSinInteressado': 'S' if interessado else '',
            'chkSinRemetente': 'S' if remetente else '',
            'chkSinDestinatario': 'S' if destinatario else '',
            'txtDescricaoPesquisa': descricao,
            'txtObservacaoPesquisa': observacao_unidade,
            'txtProtocoloPesquisa': numero_sei,
            'selTipoProcedimentoPesquisa': id_tipo_processo,
            'selSeriePesquisa': id_tipo_documento,
            'txtNumeroDocumentoPesquisa': numero_nome_arvore,
            'rdoData': '0',  # '30' últimos trintas dias, '60' últimos sessenta dias
            'txtDataInicio': data_inicial,
            'txtDataFim': data_final,
            'txtUsuarioGerador1': usuario_gerador1,
            'hdnIdUsuarioGerador1': '',
            'txtUsuarioGerador2': usuario_gerador2,
            'hdnIdUsuarioGerador2': '',
            'txtUsuarioGerador3': usuario_gerador3,
            'hdnIdUsuarioGerador3': '',
            'frmPesquisaProtocolo': 'submit',
            'hdnInicio': '0',
        }

        if data['rdoPesquisarEm'] == 'P':
            del data['chkSinDocumentosGerados']
            del data['chkSinDocumentosRecebidos']
            del data['selSeriePesquisa']
            del data['chkSinRemetente']
            del data['chkSinDestinatario']
            del data['frmPesquisaProtocolo']
            data['chkSinInteressado'] = 'S'

        if numero_sei == '00058.021932/2020-82':
            print(data)

        data = {k: v for k, v in data.items() if v}
        r = self.session.post(self.form_URL, data=data, allow_redirects=True)

        soup = BeautifulSoup(r.content, 'lxml')

        print(f'{data["rdoPesquisarEm"]= }')
        page_title = soup.find('title').text
        print(f'{page_title= }', type(page_title))
        print(r.url)

        if page_title == 'SEI - Processo':
            return ProcessoSei(self.session, r.text)
        elif page_title == 'SEI - Resultado da Pesquisa':
            return ResultadoPesquisa(self.session, r.text)
        else:
            raise Exception("SEI.pesquisa apresentou resultado inesperado")

