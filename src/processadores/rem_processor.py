from src.utils.formatadores import formatar_data
from src.utils.arquivo import gravar_substring


class RemProcessor:
    
    @staticmethod
    def processar(arquivo_entrada, arquivo_saida):
        try:
            with open(arquivo_entrada, "r", encoding="latin-1") as handle:
                linhas = handle.readlines()
        except FileNotFoundError:
            print(f"Erro: Arquivo '{arquivo_entrada}' não encontrado.")
            return False
        except Exception as e:
            print(f"Erro ao abrir o arquivo: {e}")
            return False

        try:
            with open(arquivo_saida, "w", encoding="utf-8") as saida:
                unico = True
                nlinhas = 0

                for linha in linhas:
                    linha = linha.rstrip('\r\n')
                    if len(linha) == 0:
                        continue

                    flag = linha[0] if len(linha) > 0 else ""

                    if flag == "0":
                        RemProcessor._processar_header(saida, linha)
                    elif flag == "7":
                        RemProcessor._processar_detalhe(saida, linha, unico)
                        if unico:
                            unico = False
                        nlinhas = nlinhas + 1

                RemProcessor._gravar_rodape(saida, nlinhas)

            print("Processamento realizado com sucesso!")
            print(f"Total de lançamentos processados: {nlinhas}")
            return True

        except Exception as e:
            print(f"Erro ao processar o arquivo: {e}")
            return False
    
    @staticmethod
    def _processar_header(saida, linha):
        identificacao = linha[11:19] if len(linha) >= 19 else linha[11:].ljust(8)
        identificacao = identificacao[:8]

        agencia = linha[26:30] if len(linha) >= 30 else linha[26:].ljust(4)
        agencia = agencia[:4]
        agencia_dv = linha[30:31] if len(linha) >= 31 else ""
        agencia = f"{agencia}-{agencia_dv}"

        conta = linha[31:39] if len(linha) >= 39 else linha[31:].ljust(8)
        conta = conta[:8]
        conta_dv = linha[39:40] if len(linha) >= 40 else ""
        conta = f"{conta}-{conta_dv}"

        beneficiario = linha[46:76] if len(linha) >= 76 else linha[46:].ljust(30)
        beneficiario = beneficiario[:30].rstrip()

        banco = linha[76:94] if len(linha) >= 94 else linha[76:].ljust(18)
        banco = banco[:18].rstrip()

        data_gravacao = linha[94:100] if len(linha) >= 100 else linha[94:].ljust(6)
        data_gravacao = formatar_data(data_gravacao[:6])

        convenio = linha[129:136] if len(linha) >= 136 else linha[129:].ljust(7)
        convenio = convenio[:7].rstrip()

        substring = (identificacao + " " * 8 +
                    agencia + " " +
                    conta + " " +
                    beneficiario + " " +
                    banco + " " +
                    data_gravacao + " " * 5 +
                    convenio)

        cabecalho = "TIPO DE SERVICO AG.    CONTA      BENEFICIARIO                   ARRECADADOR        DT. GRAVACAO CONVENIO"
        gravar_substring(saida, cabecalho)
        cabecalho = "-" * 105
        gravar_substring(saida, cabecalho)
        gravar_substring(saida, substring)
        gravar_substring(saida, cabecalho)
    
    @staticmethod
    def _processar_detalhe(saida, linha, unico):
        if unico:
            cabecalho = "CPF/CNPJ DO BENEFICIARIO      NOSSO NUMERO      CONTROLE EMPRESA          MEU NUMERO DT VENCIMENTO VALOR DO TITULO DT EMISSAO  CPF/CNPJ DO PAGADOR PAGADOR"
            gravar_substring(saida, cabecalho)
            cabecalho = "-" * 195
            gravar_substring(saida, cabecalho)

        cpf_cnpj_beneficiario = linha[3:17] if len(linha) >= 17 else linha[3:].ljust(14)
        cpf_cnpj_beneficiario = cpf_cnpj_beneficiario[:14]

        nosso_numero = linha[63:80] if len(linha) >= 80 else linha[63:].ljust(17)
        nosso_numero = nosso_numero[:17]

        meu_numero = linha[110:120] if len(linha) >= 120 else linha[110:].ljust(10)
        meu_numero = meu_numero[:10]

        codigo_controle_emp = linha[38:63] if len(linha) >= 63 else linha[38:].ljust(25)
        codigo_controle_emp = codigo_controle_emp[:25].rstrip()

        data_vencimento = linha[120:126] if len(linha) >= 126 else linha[120:].ljust(6)
        data_vencimento = formatar_data(data_vencimento[:6])

        valor_titulo = linha[126:139] if len(linha) >= 139 else linha[126:].ljust(13)
        valor_titulo = valor_titulo[:13].rstrip()

        data_emissao = linha[150:156] if len(linha) >= 156 else linha[150:].ljust(6)
        data_emissao = formatar_data(data_emissao[:6])

        cpf_cnpj_pagador = linha[220:234] if len(linha) >= 234 else linha[220:].ljust(14)
        cpf_cnpj_pagador = cpf_cnpj_pagador[:14]

        nome_pagador = linha[234:271] if len(linha) >= 271 else linha[234:]
        nome_pagador = nome_pagador[:37].rstrip() if len(nome_pagador) > 37 else nome_pagador.rstrip()

        substring = (cpf_cnpj_beneficiario + " " * 16 +
                    nosso_numero + " " * 1 +
                    codigo_controle_emp + " " * 1 +
                    meu_numero + " " * 3 +
                    data_vencimento + " " * 6 +
                    valor_titulo + " " * 2 +
                    data_emissao + " " * 4 +
                    cpf_cnpj_pagador + " " * 5 +
                    nome_pagador)

        gravar_substring(saida, substring)
    
    @staticmethod
    def _gravar_rodape(saida, nlinhas):
        cabecalho = "-" * 195
        gravar_substring(saida, cabecalho)
        substring = f"Total de Lancamentos: {nlinhas}"
        gravar_substring(saida, substring)
