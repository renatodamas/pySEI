import os
import pytest

from pysei import SEI, ResultadoPesquisa, ProcessoSei

SEI_USERNAME = os.environ['SEI_USERNAME']
SEI_PASSWORD = os.environ['SEI_PASSWORD']
SEI_URL = os.environ['SEI_URL']
SEI_UNIDADE = os.environ['SEI_UNIDADE']
SEI_PROCESSO_TESTE = os.environ['SEI_PROCESSO_TESTE']


@pytest.fixture(scope='function')
def sei():
    return SEI(SEI_URL)


def test_login_sei(sei):
    login_status = sei.login(SEI_USERNAME, SEI_PASSWORD)
    assert login_status


def test_login_dados_invalidos_sei(sei):
    login_status = sei.login('00000000000',  SEI_PASSWORD)
    assert not login_status


def test_acessa_tela_pesquisa(sei):
    sei.login(SEI_USERNAME, SEI_PASSWORD)
    html = sei.acessa_tela_pesquisa()
    assert 'Pesquisar em' in html


def test_pesquisa(sei):
    sei.login(SEI_USERNAME, SEI_PASSWORD)
    query = 'Rafael'
    pesquisa = sei.pesquisa(query)
    assert query in pesquisa.html


def test_retorna_resultado_pesquisa(sei):
    sei.login(SEI_USERNAME, SEI_PASSWORD, id_unidade=SEI_UNIDADE)
    p = sei.pesquisa(numero_sei='000000000015500')
    assert isinstance(p, ResultadoPesquisa)


def test_retorna_processo_sei(sei):
    sei.login(SEI_USERNAME, SEI_PASSWORD, id_unidade=SEI_UNIDADE)
    p = sei.pesquisa(numero_sei=SEI_PROCESSO_TESTE, pesquisar_documentos=False)
    assert isinstance(p, ProcessoSei)


def test_get_form_url(sei):
    sei.login(SEI_USERNAME, SEI_PASSWORD)
    assert sei.form_URL.startswith('https://')


def test_form_url(sei):
    sei.login(SEI_USERNAME, SEI_PASSWORD)
    assert sei.form_URL is not None
