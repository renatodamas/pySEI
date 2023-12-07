import re
import json


CLASS_WEBSERVICE =
'''
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
        if super().login(username, password, id_orgao, id_unidade):
            self.id_orgao = id_orgao
            self.id_unidade = id_unidade
            self.session.auth = HTTPBasicAuth(username=username, password=password)
            self.session.auth.__dict__[self.hdn_token['name']] = self.hdn_token['value']
            print(self.session.auth.__dict__)
            transport = Transport(session=self.session)
            self._soapheaders = {
                "credentialsHeader": {
                    "Username": username,
                    "Password": password,
                    self.hdn_token['name']: self.hdn_token['value']
                }

            }
            self.client = Client(wsdl=self.wsdl,
                                 transport=transport,
                                 # wsse=UsernameToken(username=username, password=password)
                                 # _soapheaders=self._soapheaders
                                 )

            print(self.client.wsdl.dump())
            self.is_connected = True
            
        return self.is_connected
'''

with open('/home/damas/Documentos/Renato/Projetos/Python/SEI-WebService/utils/services.txt') as file:
    lines = file.readlines()

with open('param_doc.json', encoding='utf-8') as file:
    param_doc = json.load(file)


with open('/home/damas/Documentos/Renato/Projetos/Python/SEI-WebService/utils/parse_result.txt', 'w') as file:
    
    file.write(

)
    for line in lines:
        line = line.replace(' -> parametros: ', '')
        line = line.replace('string', 'str')
        service = re.search('(\w+)\(', line).group(1)
        params = re.findall('\(?(\w+):\s', line)

        types = re.findall(':\s[\w\d]+:([\w\d]+)[,)]?', line)
        params_lst = [f'{p}: {t}' for p, t in zip(params, types)]
        params_prt = ",\n\t".join(params_lst)
        print(params)
        print(types)

        file.write(f'def {service}(\n\t{params_prt}):\n')
        file.write("\t'''\n\n\n")
        for param in params:
            file.write(f'\t:param {param}: {param_doc.get(param, "")}\n')
        file.write("\t'''\n"+
                   f"\traise Exception('Method {service} is not implemented.')\n\n")

