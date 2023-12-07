import base64
class Documento():
    def __init__(self):
        self._dados = {
            'Tipo': '',  # xsd: string
            'IdSerie': '',  # xsd:string
            'IdProcedimento': '',  # xsd:string
            'ProtocoloProcedimento': '',  # xsd:string
            'Numero': '',  # xsd:string
            'Data': '',  # xsd:string
            'Descricao': '',  # xsd:string
            'IdTipoConferencia': '',  # xsd:string
            'Remetente': {'Sigla': 'rgd', 'Nome': 'Renato'},  # ns0:Remetente
            'Interessados': [{'Sigla': 'rgd', 'Nome': 'Renato'}],  # ns0:ArrayOfInteressado
            'Destinatarios': [{'Sigla': 'rgd', 'Nome': 'Renato'}],  # ns0:ArrayOfDestinatario
            'Observacao': '',  # xsd:string
            'NomeArquivo': '',  # xsd:string
            'NivelAcesso': '',  # xsd:string
            'IdHipoteseLegal': '',  # xsd:string
            'Conteudo': '',  # xsd:string
            'ConteudoMTOM': '',  # xsd:base64Binary
            'IdArquivo': '',  # xsd:string
            # 'Campos': [{}],  # ns0:ArrayOfCampo
            'SinBloqueado': ''  # xsd:string)
        }

    def dados(self):
        return self._dados

    @property
    def tipo(self):
        """
        Tipo do documento
        :return: 'G' ou 'R'
        """
        return self._dados.get('Tipo', None)

    @tipo.setter
    def tipo(self, tipo):
        self._dados['Tipo'] = tipo

    @property
    def id_procedimento(self):
        return self._dados.get('IdProcedimento', None)

    @id_procedimento.setter
    def id_procedimento(self, id_proc):
        self._dados['IdProcedimento'] = id_proc

    @property
    def conteudo(self):
        return self._dados.get('Conteudo', None)

    @conteudo.setter
    def conteudo(self, conteudo):
        conteudo_bytes = message.encode('ascii', errors='ignore')
        conteudo_base64_bytes = base64.b64encode(conteudo_bytes)
        self._dados['Conteudo'] = conteudo_base64_bytes

    @property
    def id_serie(self):
        """
        Id do tipo de documento
        :return:
        """
        return self._dados.get('IdSerie', None)

    @id_serie.setter
    def id_serie(self, id_serie):
        """
        :param id_serie:
        :return:
        """
        self._dados['IdSerie'] = id_serie







