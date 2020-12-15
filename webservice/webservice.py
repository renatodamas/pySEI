from pysei import SEI
from zeep import Client
from zeep.wsse.username import UsernameToken
from zeep.transports import Transport


class LoginErro(Exception):
    pass


class SEIWebService(SEI):

    def __init__(
            self,
            wsdl: str
    ):
        super().__init__(wsdl[:wsdl.find('controlador')])
        self.client = None
        self.wsdl = wsdl
        self.is_connected = False
        self.id_orgao = None
        self.id_unidade = None

    def login(
            self,
            username,
            password,
            id_orgao=0,
            id_unidade=0
    ) -> bool:
        """
        Realiza o login no WebService via WSSE
        :param username:
        :param password:
        :param id_orgao:
        :param id_unidade:
        :return:
        """

        self.id_orgao = id_orgao
        self.id_unidade = id_unidade
        user_token = UsernameToken(username, password)
        transport = Transport(session=self.session)
        try:
            self.client = Client(wsdl=self.wsdl, wsse=user_token, transport=transport)
        except Exception:
            raise LoginErro('Erro no login')
        else:
            return True

    def adicionar_arquivo(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            nome: str,
            tamanho: str,
            hash_md5: str,
            conteudo: str
    ) -> bool:
        """
        O serviço criará um arquivo no repositório de documentos e retornará seu identificador. O envio do arquivo
        poderá ser particionado com chamadas posteriores ao serviço adicionar_conteudo_arquivo.
        Após todo o conteúdo ser transferido o arquivo será ativado e poderá ser associado com um documento ex-
        terno no serviço de inclusão de documento (campo id_arquivo da estrutura documento). Neste caso, ao chamar
        o respectivo serviço o conteúdo não precisará ser informado pois já foi enviado previamente.
        Quando o agendamento removerArquivosNaoUtilizados for executado serão excluídos todos os arquivos com
        mais de 24 horas e que não foram completados ou que não foram associados com um documento externo.

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param nome: Opcional. Filtra contato pelo nome.
        :param tamanho: tamanho total do arquivo em bytes
        :param hash_md5: MD5 do conteúdo total do arquivo
        :param conteudo: Conteúdo codificado em Base64 para ser adicionado no arquivo
        :return:
        """
        raise Exception('Método adicionar_arquivo não implementado!')

    def adicionar_conteudo_arquivo(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_arquivo: str,
            conteudo: str
    ) -> str:
        """
        O sistema identificará automaticamente quando o conteúdo foi completado validando o tamanho em bytes e
        o hash do conteúdo. Quando as condições forem satisfeitas o arquivo será ativado e poderá ser utilizado nas
        chamadas de inclusão de documento.

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param id_arquivo: Identificador do arquivo criado pelo serviço adicionar_arquivo
        :param conteudo: Conteúdo codificado em Base64 para ser adicionado no arquivo
        :return: Retorna o identificador do arquivo criado
        """
        raise Exception('Método adicionar_conteudo_arquivo não implementado!')

    def agendar_publicacao(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_documento: str,
            protocolo_documento: str,
            sta_motivo: int,
            id_veiculo_publicacao: str,
            data_disponibilizacao: str,
            resumo: str,
            imprensa_nacional  #: Publicacaoimprensa_nacional
    ) -> str:
        """
        É possível informar apenas um dos parâmetros id_documento ou protocolo_documento para identificação.

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param id_documento: Identificador do documento
        :param protocolo_documento: Número do documento visível para o usuário, ex.: 0003934
        :param sta_motivo: 1 = Publicação, 2 = Retificação, 3 = Republicação, 4 = Apostilamento
        :param id_veiculo_publicacao: Identificador do veículo de publicação
        :param data_disponibilizacao: Data de disponibilização
        :param resumo: Texto do resumo da publicação
        :param imprensa_nacional: Opcional, dados informativos da Imprensa Nacional
                (ver estrutura Publicacaoimprensa_nacional)
        :return: Retorna o identificador interno da publicação
        """
        raise Exception('Método agendar_publicacao não implementado!')

    def alterar_publicacao(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_publicacao: str,
            id_documento: str,
            protocolo_documento: str,
            sta_motivo: str,
            id_veiculo_publicacao: str,
            data_disponibilizacao: str,
            resumo: str,
            imprensa_nacional  #: Publicacaoimprensa_nacional
    ) -> bool:
        """
        É possível informar apenas um dos parâmetros id_documento ou protocolo_documento para identificação.

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param id_publicacao: Identificador da publicação
        :param id_documento: Identificador do documento
        :param protocolo_documento: Número do documento visível para o usuário, ex.: 0003934
        :param sta_motivo: 1 = Publicação, 2 = Retificação, 3 = Republicação, 4 = Apostilamento
        :param id_veiculo_publicacao: Identificador do veículo de publicação
        :param data_disponibilizacao: Data de disponibilização
        :param resumo: Texto do resumo da publicação
        :param imprensa_nacional: Opcional, dados informativos da Imprensa Nacional
                (ver estrutura Publicacaoimprensa_nacional)
        :return: Retorna true
        """
        raise Exception('Método alterar_publicacao não implementado!')

    def anexar_processo(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_procedimento_principal: str,
            protocolo_procedimento_anexado: str
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param protocolo_procedimento_principal: Número do processo visível para o usuário, ex: 12.1.000000077-4
        :param protocolo_procedimento_anexado: Número do processo visível para o usuário, ex: 12.1.000000077-4
        :return: Retorna true
        """
        raise Exception('Método anexar_processo não implementado!')

    def atribuir_processo(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_procedimento: str,
            id_usuario: str,
            sin_reabrir: str
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param protocolo_procedimento: Número do processo visível para o usuário, ex: 12.1.000000077-
        :param id_usuario: Opcional. Filtra determinado usuário.
        :param sin_reabrir: S/N - indica se o processo deve ser reaberto automaticamente (valor padrão N)
        :return: Retorna true
        """
        raise Exception('Método atribuir_processo não implementado!')

    def atualizar_contatos(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            contatos  # : ArrayOfContato
    ) -> bool:
        """
        Cada um dos contatos do conjunto informado será tratado separadamente. Sendo assim, mesmo que alguns
        apresentem erro ou falha na validação dos dados os demais serão atualizados. Os erros e validações de dados
        serão acumulados e retornados como uma exceção.
        Com relação a pessoa jurídica associada serão processados apenas os atributos IdContatoAssociado e SinEnde-
        recoAssociado.
        para cidade, estado, país e cargo devem ser informados os campos relativos aos identificadores internos (IdCi-
        dade, id_estado, id_pais e id_cargo).

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Id da unidade onde o bloco foi gerado
        :param contatos: Informar conjunto de contatos para atualização (ver estrutura Contato).
        :return: Retorna true
        """
        raise Exception('Método atualizar_contatos não implementado!')

    def bloquear_processo(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_procedimento: str
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Id da unidade onde o processo está aberto
        :param protocolo_procedimento: Número do processo visível para o usuário, ex: 12.1.000000077-
        :return: Retorna true
        """
        raise Exception('Método bloquear_processo não implementado!')

    def cancelar_agendamento_publicacao(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_publicacao: str,
            id_documento: str,
            protocolo_documento: str
    ) -> bool:
        """
        É possível informar apenas um dos parâmetros id_publicacao, id_documento ou protocolo_documento para iden-
        tificação.

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param id_publicacao: Identificador da publicação
        :param id_documento: Identificador do documento
        :param protocolo_documento: Número do documento visível para o usuário, ex.: 0003934
        :return: Retorna true
        """
        raise Exception('Método cancelar_agendamento_publicacao não implementado!')

    def cancelar_disponibilizacao_bloco(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_bloco: str
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Id da unidade onde o processo está aberto
        :param id_bloco: Número do bloco
        :return: Retorna true
        """
        raise Exception('Método cancelar_disponibilizacao_bloco não implementado!')

    def cancelar_documento(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_documento: str,
            motivo: str
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Id da unidade onde o processo está aberto
        :param protocolo_documento: Número do documento visível para o usuário, ex.: 0003934
        :param motivo: Texto do motivo do sobrestamento
        :return: Retorna true
        """
        raise Exception('Método cancelar_documento não implementado!')

    def concluir_processo(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_procedimento: str
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Id da unidade onde o processo está aberto
        :param protocolo_procedimento: Número do processo visível para o usuário, ex: 12.1.000000077-
        :return: Retorna true
        """
        raise Exception('Método concluir_processo não implementado!')

    def confirmar_disponibilizacao_publicacao(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_veiculo_publicacao: str,
            data_disponibilizacao: str,
            data_publicacao: str,
            numero: str,
            id_documentos  # : ArrayOfid_documento
    ) -> bool:
        """
        Este método é responsável por atualizar o andamento de agendamento no processo com o número e a data
        efetiva da publicação. Além disso, haverá mudança no nível de acesso do documento para público e o conteúdo
        será disponibilizado na pesquisa de publicações do SEI (se a opção “Exibir as publicações enviadas para este
        veículo na pesquisa de publicações interna” estiver marcada no cadastro do veículo de publicação).

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_veiculo_publicacao: Identificador do veículo de publicação
        :param data_disponibilizacao: Data de disponibilização
        :param data_publicacao: Data de publicação
        :param numero: Número da publicação
        :param id_documentos: Conjunto de identificadores internos dos documentos
        :return: Retorna true
        """
        raise Exception('Método confirmar_disponibilizacao_publicacao não implementado!')

    def consultar_bloco(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_bloco: str,
            sin_retornar_protocolos: str
    ) -> object:
        """
        O bloco deve ser da unidade ou estar disponibilizado para ela. O sinalizador de retorno dos protocolos implica
        em processamento adicional realizado pelo sistema, sendo assim, recomenda-se que seja solicitado o retorno
        apenas se as informações forem estritamente necessárias.

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Identificador da unidade no SEI
                (sugere-se que este id seja armazenado em uma tabela auxiliar do sistema cliente).
        :param id_bloco: Número do bloco
        :param sin_retornar_protocolos: S/N - sinalizador para retorno dos protocolos do bloco (valor padrão N)
        :return: Uma ocorrência da estrutura RetornoConsultaBloco
        """
        raise Exception('Método consultar_bloco não implementado!')

    def consultar_documento(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_documento: str,
            sin_retornar_andamento_geracao: str,
            sin_retornar_assinaturas: str,
            sin_retornar_publicacao: str,
            sin_retornar_campos: str
    ) -> object:
        """
        documento de processos sigilosos não são retornados. Cada um dos sinalizadores implica em processamento
        adicional realizado pelo sistema, sendo assim, recomenda-se que seja solicitado o retorno somente para infor-
        mações estritamente necessárias.

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param protocolo_documento: Número do documento visível para o usuário, ex.: 0003934
        :param sin_retornar_andamento_geracao: S/N - sinalizador para retorno do andamento de geração
        :param sin_retornar_assinaturas: S/N - sinalizador para retorno das assinaturas do documento
        :param sin_retornar_publicacao: S/N - sinalizador para retorno dos dados de publicação
        :param sin_retornar_campos: S/N - sinalizador para retorno dos campos do formulário
        :return: Uma ocorrência da estrutura RetornoConsultadocumento
        """
        raise Exception('Método consultar_documento não implementado!')

    def consultar_procedimento(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_procedimento: str,
            sin_retornar_assuntos: str,
            sin_retornar_interessados: str,
            sin_retornar_observacoes: str,
            sin_retornar_andamento_geracao: str,
            sin_retornar_andamento_conclusao: str,
            sin_retornar_ultimo_andamento: str,
            sin_retornar_unidades_procedimento_aberto: str,
            sin_retornar_procedimentos_relacionados: str,
            sin_retornar_procedimentos_anexados: str
    ) -> object:
        """
        Processos sigilosos não são retornados. Cada um dos sinalizadores implica em processamento adicional reali-
        zado pelo sistema, sendo assim, recomenda-se que seja solicitado o retorno somente para informações estri-
        tamente necessárias.

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Identificador da unidade no SEI
                (sugere-se que este id seja armazenado em uma tabela auxiliar do sistema cliente)
        :param protocolo_procedimento: Número do processo visível para o usuário, ex: 12.1.000000077-4
        :param sin_retornar_assuntos: S/N - sinalizador para retorno dos assuntos do processo
        :param sin_retornar_interessados: S/N - sinalizador para retorno de interessados do processo
        :param sin_retornar_observacoes: S/N - sinalizador para retorno das observações das unidades
        :param sin_retornar_andamento_geracao: S/N - sinalizador para retorno do andamento de geração
        :param sin_retornar_andamento_conclusao: S/N - sinalizador para retorno do andamento de conclusão
        :param sin_retornar_ultimo_andamento: S/N - sinalizador para retorno do último andamento
        :param sin_retornar_unidades_procedimento_aberto: S/N - sinalizador para retorno das unidades
                onde o processo se encontra aberto
        :param sin_retornar_procedimentos_relacionados: S/N - sinalizador para retorno dos processos relacionados
        :param sin_retornar_procedimentos_anexados: S/N - sinalizador para retorno dos processos anexados
        :return: Uma ocorrência da estrutura RetornoConsultaprocedimento
        """
        raise Exception('Método consultar_procedimento não implementado!')

    def consultar_procedimento_individual(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_orgao_procedimento: str,
            id_tipo_procedimento: str,
            id_orgao_usuario: str,
            sigla_usuario: str
    ) -> object:
        """
        Processos individuais são aqueles onde o cadastro do tipo associado esta sinalizado como "Processo único no
        órgão por usuário interessado". Se para o tipo informado houver mais de um processo individual onde o usuário
        é interessado então será retornado o mais recente. Caso nenhum processo seja encontrado será retornado
        nulo. Processos sigilosos não são retornados.

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Identificador da unidade no SEI
                (sugere-se que este id seja armazenado em uma tabela auxiliar do sistema cliente).
        :param id_orgao_procedimento: Identificador do órgão do processo
        :param id_tipo_procedimento: Identificador do tipo do processo
        :param id_orgao_usuario: Identificador do órgão do usuário
        :param sigla_usuario: sigla do usuário
        :return: Uma ocorrência da estrutura procedimentoResumido
        """
        raise Exception('Método consultar_procedimentoIndividual não implementado!')

    def consultar_publicacao(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_publicacao: str,
            id_documento: str,
            protocolo_documento: str,
            sin_retornar_andamento: str,
            sin_retornar_assinaturas: str
    ) -> object:
        """
        para filtro é possível utilizar qualquer um dos parâmetros id_publicacao, id_documento ou protocolo_documento.
        Cada um dos sinalizadores implica em processamento adicional realizado pelo sistema, sendo assim, reco-
        menda-se que seja solicitado o retorno somente para informações estritamente necessárias.

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Identificador da unidade no SEI
                (sugere-se que este id seja armazenado em uma tabela auxiliar do sistema cliente).
        :param id_publicacao: Identificador da publicação
        :param id_documento: Identificador do documento
        :param protocolo_documento: Número do documento visível para o usuário, ex.: 0003934
        :param sin_retornar_andamento: S/N - sinalizador para retorno do andamento de publicação
        :param sin_retornar_assinaturas: S/N - sinalizador para retorno das assinaturas do documento
        :return: Uma ocorrência da estrutura RetornoConsultaPublicacao
        """
        raise Exception('Método consultar_publicacao não implementado!')

    def definir_marcador(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            definicoes  #: ArrayOfdefinicaoMarcador
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Id da unidade onde o processo está aberto
        :param definicoes: Conjunto de definições de marcadores (ver estrutura definicaoMarcador)
        :return: Retorna true
        """
        raise Exception('Método definir_marcador não implementado!')

    def desanexar_processo(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_procedimento_principal: str,
            protocolo_procedimento_anexado: str,
            motivo: str
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param protocolo_procedimento_principal: Número do processo visível para o usuário, ex: 12.1.000000077-4
        :param protocolo_procedimento_anexado: Número do processo visível para o usuário, ex: 12.1.000000077-4
        :param motivo: Texto do motivo do sobrestamento
        :return: Retorna true
        """
        raise Exception('Método desanexar_processo não implementado!')

    def desbloquear_processo(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_procedimento: str
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Id da unidade onde o processo está aberto
        :param protocolo_procedimento: Número do processo visível para o usuário, ex: 12.1.000000077-
        :return: Retorna true
        """
        raise Exception('Método desbloquear_processo não implementado!')

    def disponibilizar_bloco(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_bloco: str
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param id_bloco: Número do bloco
        :return: Retorna true
        """
        raise Exception('Método disponibilizar_bloco não implementado!')

    def enviar_email(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_procedimento: str,
            de: str,
            para: str,
            cco: str,
            assunto: str,
            mensagem: str,
            id_documentos  #: ArrayOfid_documento
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param protocolo_procedimento: Número do processo visível para o usuário, ex: 12.1.000000077-
        :param de:
        :param para:
        :param cco: CCO
        :param assunto:
        :param mensagem:
        :param id_documentos: Conjunto de identificadores internos dos documentos
        :return: Retorna true
        """
        raise Exception('Método enviar_email não implementado!')

    def enviar_processo(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_procedimento: str,
            unidades_destino: object,  # ArrayOfid_unidade
            sin_manter_aberto_unidade: str,
            sin_remover_anotacao: str,
            sin_enviar_email_notificacao: str,
            data_retorno_programado: str,
            dias_retorno_programado: str,
            sin_dias_uteis_retorno_programado: str,
            sin_reabrir: str
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param protocolo_procedimento: Número do processo visível para o usuário, ex: 12.1.000000077-4
        :param unidades_destino: Conjunto de unidades destinatárias (ver estrutura Unidade)
        :param sin_manter_aberto_unidade: S/N - sinalizador indica se o processo deve ser mantido aberto na unidade
        :param sin_remover_anotacao: S/N - sinalizador indicando se deve ser removida anotação do processo
        :param sin_enviar_email_notificacao: S/N - sinalizador indicando se deve ser enviado email de aviso
                para as unidades destinatárias (valor padrão N)
        :param data_retorno_programado: Data para definição de Retorno Programado (valor padrão nulo)
        :param dias_retorno_programado: Número de dias para o Retorno Programado (valor padrão nulo)
        :param sin_dias_uteis_retorno_programado: S/N - sinalizador indica se o valor passado no parâmetro
                dias_retorno_programado corresponde a dias úteis ou não (valor padrão N)
        :param sin_reabrir: S/N - sinalizador indicando se o processo deve ser reaberto automaticamente caso esteja
                concluído na unidade. para realizar a reabertura o serviço deverá ter também a operação
                "Reabrir Processo" liberada no SEI.
        :return: Retorna true
        """
        raise Exception('Método enviar_processo não implementado!')

    def excluir_bloco(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_bloco: str
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Id da unidade onde o bloco foi gerado
        :param id_bloco: Número do bloco
        :return: Retorna true
        """
        raise Exception('Método excluir_bloco não implementado!')

    def excluir_documento(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_documento: str
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param protocolo_documento: Número do documento visível para o usuário, ex.: 0003934
        :return: Retorna true
        """
        raise Exception('Método excluir_documento não implementado!')

    def excluir_processo(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_procedimento: str
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param protocolo_procedimento: Número do processo visível para o usuário, ex: 12.1.000000077-4
        :return: Retorna true
        """
        raise Exception('Método excluir_processo não implementado!')

    def gerar_bloco(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            tipo: str,
            descricao: str,
            unidades_disponibilizacao: object,  # ArrayOfid_unidade
            documentos: object,  # ArrayOfdocumentoFormatado,
            sin_disponibilizar: str
    ) -> int:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Id da unidade onde será gerado o bloco
        :param tipo: tipo do bloco: A – Assinatura, R – Reunião, I - Interno
        :param descricao: descrição do bloco
        :param unidades_disponibilizacao: Conjunto de unidades para disponibilização (ver estrutura Unidade).
                Passar um conjunto vazio caso o bloco não deva ser disponibilizado.
        :param documentos: Lista de protocolos de documentos (número visível para o usuário, ex.: 0003934). Para
                realizar a inclusão o serviço deverá ter também a operação "Incluir documento em Bloco" liberada no SEI.
        :param sin_disponibilizar: S/N - sinalizador indicando se o bloco deve ser automaticamente disponibilizado.
                Para realizar a disponibilização o serviço deverá ter também a operação "Disponibilizar Bloco"
                liberada no SEI.
        :return: Retorna o número do bloco gerado.
        """
        raise Exception('Método gerar_bloco não implementado!')

    def gerar_procedimento(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            procedimento: object,  # procedimento,
            documentos: object,  # ArrayOfdocumento,
            procedimentos_relacionados: object,  # ArrayOfprocedimentoRelacionado,
            unidades_envio: object,  # ArrayOfid_unidade,
            sin_manter_aberto_unidade: str,
            sin_enviar_email_notificacao: str,
            data_retorno_programado: str,
            dias_retorno_programado: str,
            sin_dias_uteis_retorno_programado: str,
            id_marcador: str,
            texto_marcador: str
    ) -> object:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param procedimento: Informar os dados do processo (ver estrutura procedimento)
        :param documentos: Informar os documentos que devem ser gerados em conjunto com o processo
                (ver estrutura documento). Se nenhum documento for gerado informar um conjunto vazio. O número máximo
                de documentos por chamada é limitado através do parâmetro SEI_WS_NUM_MAX_DOCS (menu Infra/Parâmetros).
        :param procedimentos_relacionados: Conjunto com Ids de processos que devem ser relacionados automaticamente
                com o novo processo
        :param unidades_envio: Conjunto com Ids de unidades para envio do processo após a geração. O processo ficará
                aberto na unidade geradora e nas unidades informadas neste parâmetro.
        :param sin_manter_aberto_unidade: S/N - sinalizador indica se o processo deve ser mantido aberto na unidade de
                origem (valor padrão S)
        :param sin_enviar_email_notificacao: S/N - sinalizador indicando se deve ser enviado email de aviso para as
                unidades destinatárias (valor padrão N)
        :param data_retorno_programado: Data para definição de Retorno Programado (valor padrão nulo)
        :param dias_retorno_programado: Número de dias para o Retorno Programado (valor padrão nulo)
        :param sin_dias_uteis_retorno_programado: S/N - sinalizador indica se o valor passado no parâmetro
                dias_retorno_programado corresponde a dias úteis ou não (valor padrão N)
        :param id_marcador: Opcional. Identificador de um marcador da unidade para associação
        :param texto_marcador: Opcional. Texto do marcador
        :return: Uma ocorrência da estrutura RetornoGeracaoprocedimento
        """
        raise Exception('Método gerar_procedimento não implementado!')

    def incluir_documento(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            documento: object  # documento
    ) -> object:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Identificador da unidade no SEI (sugere-se que este id seja armazenado em uma tabela
                auxiliar do sistema cliente)
        :param documento: Informar os dados do documento (ver estrutura documento)
        :return: Uma ocorrência da estrutura RetornoInclusaodocumento
        """
        raise Exception('Método incluir_documento não implementado!')

    def incluir_documento_bloco(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_bloco: str,
            protocolo_documento: str,
            anotacao: str
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Id da unidade onde o bloco foi gerado
        :param id_bloco: Número do bloco
        :param protocolo_documento: Número do documento visível para o usuário, ex.: 0003934
        :param anotacao: Opcional. Texto de anotação associado com o processo no bloco.
        :return: Retorna true
        """
        raise Exception('Método incluir_documentoBloco não implementado!')

    def incluir_processo_bloco(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_bloco: str,
            protocolo_procedimento: str,
            anotacao: str
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Id da unidade onde o bloco foi gerado
        :param id_bloco: Número do bloco
        :param protocolo_procedimento: Número do processo visível para o usuário, ex: 12.1.000000077-4
        :param anotacao: Opcional. Texto de anotação associado com o processo no bloco.
        :return: Retorna true
        """
        raise Exception('Método incluir_processo_bloco não implementado!')

    def lancar_andamento(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_procedimento: str,
            id_tarefa: str,
            id_tarefa_modulo: str,
            atributos: object,  # ArrayOfAtributoAndamento
    ) -> object:
        """
        O parâmetro id_tarefa deve ser um número maior ou igual a 1000 (identificadores abaixo deste valor são reser-
        vados do SEI) ou então 65 que equivale a tarefa de atualização de andamento (neste caso informar um atributo
        com nome="DESCRICAO" e Valor="texto do andamento").
        Pode ser informado id_tarefa ou id_tarefaModulo o que for mais conveniente.

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param protocolo_procedimento: Número do processo visível para o usuário, ex: 12.1.000000077-4
        :param id_tarefa: Identificador da tarefa associada
        :param id_tarefa_modulo: Identificador da tarefa de módulo
        :param atributos: Conjunto de atributos associados (ver estrutura AtributoAndamento)
        :return: Retorna o andamento gerado (ver estrutura Andamento)
        """
        raise Exception('Método lancar_andamento não implementado!')

    def listar_andamentos(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_procedimento: str,
            sin_retornar_atributos: str,
            andamentos: object,  # ArrayOfIdandamentos,
            tarefas: object,  # ArrayOfid_tarefas,
            tarefas_modulos: object,  # ArrayOfid_tarefasModulo
    ) -> object:
        """
        É necessário informar pelo menos um dos parâmetros andamentos, tarefas ou tarefasModulos. No parâmetro
        tarefas é possível filtrar por qualquer tarefa do sistema (verificar os valores de tarefas internas nas
        constantes existentes no arquivo TarefaRN.php).

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param protocolo_procedimento: Número do processo visível para o usuário, ex: 12.1.000000077-4
        :param sin_retornar_atributos: S/N - sinalizador para retorno dos atributos associados
        :param andamentos: Opcional. Filtra andamentos pelos identificadores informados.
        :param tarefas: Opcional. Filtra andamentos pelos identificadores de tarefas informados.
        :param tarefas_modulos: Opcional. Filtra andamentos pelos identificadores de tarefas de módulo informados.
        :return: Um conjunto de ocorrências da estrutura Andamento.
        """
        raise Exception('Método listar_andamentos não implementado!')

    def listar_andamentosmarcadores(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_procedimento: str,
            marcadores: object,  # ArrayOfid_marcadores
    ) -> object:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param protocolo_procedimento: Número do processo visível para o usuário, ex: 12.1.000000077-4
        :param marcadores: Opcional. Filtra andamentos pelos identificadores informados. para retornar também os
                andamentos onde o marcador foi removido adicionar na lista o valor nulo.
        :return: Um conjunto de ocorrências da estrutura AndamentoMarcador.
        """
        raise Exception('Método listar_andamentosmarcadores não implementado!')

    def listar_cargos(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_cargo: str
    ) -> object:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param id_cargo: Opcional. Filtra por um cargo específico.
        :return: Um conjunto de ocorrências da estrutura Cargo.
        """
        raise Exception('Método listar_cargos não implementado!')

    def listar_cidades(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_pais: str,
            id_estado: str
    ) -> object:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param id_pais: Opcional. Filtra estados pelo país informado.
        :param id_estado: Opcional. Filtra cidades pelo estado informado.
        :return: Um conjunto de ocorrências da estrutura Cidade.
        """
        raise Exception('Método listar_cidades não implementado!')

    def listar_contatos(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_tipo_contato: str,
            pagina_registros: str,
            pagina_atual: str,
            sigla: str,
            nome: str,
            cpf: str,
            cnpj: str,
            matricula: str,
            id_contatos: object  # ArrayOfIdcontatos
    ) -> object:
        """
        Os contatos retornarão ordenados pelo atributo nome.

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param id_tipo_contato: Opcional. Filtra o tipo de contato
        :param pagina_registros: Opcional. Informa o número máximo de registros que devem ser retornados por página de
                consulta (1 a 1000 com valor padrão 1).
        :param pagina_atual: Opcional. Informa o número da página atual (valor padrão 1).
        :param sigla: Opcional. Filtra contato pela sigla.
        :param nome: Opcional. Filtra contato pelo nome.
        :param cpf: Opcional. Filtra contato pelo CPF.
        :param cnpj: Opcional. Filtra contato pelo CNPJ.
        :param matricula: Opcional. Filtra contato pelo número de matrícula.
        :param id_contatos: Opcional. Filtra contatos pelos identificadores internos.
        :return: Um conjunto de ocorrências da estrutura Contato.
        """
        raise Exception('Método listar_contatos não implementado!')

    def listar_estados(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_pais: str
    ) -> object:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param id_pais: Opcional. Filtra estados pelo país informado.
        :return: Um conjunto de ocorrências da estrutura Estado.
        """
        raise Exception('Método listar_estados não implementado!')

    def listar_extensoes_permitidas(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_arquivo_extensao: str
    ) -> object:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param id_arquivo_extensao: Opcional. Filtra determinada extensão.
        :return: Um conjunto de ocorrências da estrutura ArquivoExtensao.
        """
        raise Exception('Método listar_extensoes_permitidas não implementado!')

    def listar_feriados(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_orgao: str,
            data_inicial: str,
            data_final: str
    ) -> object:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param id_orgao: Identificador do órgão
        :param data_inicial: Data final do período de consulta
        :param data_final: Data final do período de consulta
        :return: Um conjunto de ocorrências da estrutura Feriado.
        """
        raise Exception('Método listar_feriados não implementado!')

    def listar_hipoteses_legais(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            nivel_acesso: str
    ) -> object:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param nivel_acesso: Opcional. Filtra hipóteses pelo nível de acesso associado (1 - restrito, 2 - sigiloso).
        :return: Um conjunto de ocorrências da estrutura HipoteseLegal.
        """
        raise Exception('Método listar_hipoteses_legais não implementado!')

    def listar_marcadores_unidade(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str
    ) -> object:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :return: Um conjunto de ocorrências da estrutura Marcador.
        """
        raise Exception('Método listar_marcadores_unidade não implementado!')

    def listar_paises(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str
    ) -> object:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :return: Um conjunto de ocorrências da estrutura Pais.
        """
        raise Exception('Método listar_paises não implementado!')

    def listar_series(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_tipo_procedimento: str
    ) -> object:
        """
        As séries serão listadas de acordo com o acesso configurado para o serviço informado. Por exemplo, caso o
        serviço informado seja composto por 2 operações de geração de documento dos tipos A e B então apenas estas
        2 séries retornarão. Os parâmetros id_unidade e id_tipo_procedimento podem ser informados como filtros adici-
        onais que serão aplicados nas operações do serviço. desta forma a lista de retorno pode ser montada no sis-
        tema cliente apenas com valores válidos (evitando chamadas com valores não liberados para o serviço no SEI).

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param id_tipo_procedimento: Opcional. tipo do processo cadastrado no serviço.
        :return: Um conjunto de ocorrências da estrutura Serie.
        """
        raise Exception('Método listar_series não implementado!')

    def listar_tipos_conferencia(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str
    ) -> object:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :return: Um conjunto de ocorrências da estrutura tipoConferencia.
        """
        raise Exception('Método listar_tipos_conferencia não implementado!')

    def listar_tipos_procedimento(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_serie: str
    ) -> object:
        """
        Os tipos de processo serão listados de acordo com o acesso configurado para o serviço informado. Por exemplo,
        caso o serviço informado seja composto por 3 operações de geração de processo dos tipos A, B e C então
        apenas estes 3 tipos retornarão. Os parâmetros id_unidade e id_serie podem ser informados como filtros adici-
        onais que serão aplicados nas operações do serviço. desta forma a lista de retorno pode ser montada no sis-
        tema cliente apenas com valores válidos (evitando chamadas com valores não liberados para o serviço no SEI).

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param id_serie: Opcional. tipo do documento cadastrado no serviço.
        :return: Um conjunto de ocorrências da estrutura tipoprocedimento.
        """
        raise Exception('Método listar_tipos_procedimento não implementado!')

    def listar_unidades(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_tipo_procedimento: str,
            id_serie: str
    ) -> object:
        """
        As unidades serão listadas de acordo com o acesso configurado para o serviço informado. Por exemplo, caso o
        serviço informado seja composto por 3 operações de geração de processo nas unidades X, Y e Z então apenas
        estas 3 unidades retornarão. Os parâmetros id_tipo_procedimento e id_serie podem ser informados como filtros
        adicionais que serão aplicados nas operações do serviço. desta forma a lista de retorno pode ser montada no
        sistema cliente apenas com valores válidos (evitando chamadas com valores não liberados para o serviço no
        SEI).

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_tipo_procedimento: Opcional. tipo do processo cadastrado no serviço.
        :param id_serie: Opcional. tipo do documento cadastrado no serviço.
        :return: Um conjunto de ocorrências da estrutura Unidade.
        """
        raise Exception('Método listar_unidades não implementado!')

    def listar_usuarios(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_usuario: str
    ) -> object:
        """
        Retorna o conjunto de usuários que possuem o perfil "Básico" do SEI na unidade.

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param id_usuario: Opcional. Filtra determinado usuário.
        :return: Um conjunto de ocorrências da estrutura Usuario.
        """
        raise Exception('Método listar_usuarios não implementado!')

    def reabrir_processo(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_procedimento: str
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Id da unidade por onde o processo tramitou
        :param protocolo_procedimento: Número do processo visível para o usuário, ex: 12.1.000000077-4
        :return: Retorna true
        """
        raise Exception('Método reabrir_processo não implementado!')

    def relacionar_processo(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_procedimento1: str,
            protocolo_procedimento2: str
    ) -> bool:
        """
        O relacionamento entre processos é bilateral sendo assim é necessário que a unidade possua permissão para
        relacionar nos dois tipos de processos envolvidos.

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param protocolo_procedimento1: Número do processo visível para o usuário, ex: 12.1.000000077-4
        :param protocolo_procedimento2: Número do processo visível para o usuário, ex: 11.1.000000293-2
        :return: Retorna true
        """
        raise Exception('Método relacionar_processo não implementado!')

    def remover_relacionamento_processo(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_procedimento1: str,
            protocolo_procedimento2: str
    ) -> bool:
        """
        O relacionamento entre processos é bilateral sendo assim é necessário que a unidade possua permissão para
        remover relacionamento nos dois tipos de processos envolvidos.

        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Id da unidade onde o bloco foi gerado
        :param protocolo_procedimento1: Número do processo visível para o usuário, ex: 12.1.000000077-4
        :param protocolo_procedimento2: Número do processo visível para o usuário, ex: 11.1.000000293-2
        :return: Retorna true
        """
        raise Exception('Método remover_relacionamento_processo não implementado!')

    def remover_sobrestamento_processo(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_procedimento: str
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param protocolo_procedimento: Número do processo visível para o usuário, ex: 12.1.000000077-
        :return: Retorna true
        """
        raise Exception('Método remover_sobrestamento_processo não implementado!')

    def retirar_documento_bloco(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_bloco: str,
            protocolo_documento: str
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Id da unidade onde o bloco foi gerado
        :param id_bloco: Número do bloco
        :param protocolo_documento: Número do documento visível para o usuário, ex.: 0003934
        :return: Retorna true
        """
        raise Exception('Método retirar_documento_bloco não implementado!')

    def retirar_processo_bloco(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            id_bloco: str,
            protocolo_procedimento: str
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Id da unidade onde o bloco foi gerado
        :param id_bloco: Número do bloco
        :param protocolo_procedimento: Número do processo visível para o usuário, ex: 12.1.000000077-
        :return: Retorna true
        """
        raise Exception('Método retirar_processo_bloco não implementado!')

    def sobrestar_processo(
            self,
            sigla_sistema: str,
            identificacao_servico: str,
            id_unidade: str,
            protocolo_procedimento: str,
            protocolo_procedimento_vinculado: str,
            motivo: str
    ) -> bool:
        """


        :param sigla_sistema: Valor informado no cadastro do sistema realizado no SEI
        :param identificacao_servico: Valor informado no cadastro do serviço realizado no SEI
        :param id_unidade: Valor informado no cadastro do serviço realizado no SEI
        :param protocolo_procedimento: Número do processo visível para o usuário, ex: 12.1.000000077-4
        :param protocolo_procedimento_vinculado: Opcional. Número do processo visível para o usuário, ex:
        :param motivo: Texto do motivo do sobrestamento
        :return: Retorna true
        """
        raise Exception('Método sobrestar_processo não implementado!')
