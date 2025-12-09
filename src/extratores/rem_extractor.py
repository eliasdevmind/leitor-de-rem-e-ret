"""
Extrator de dados de arquivos REM.
"""

from pathlib import Path
from src.utils.formatadores import formatar_data


class RemExtractor:
    """Classe para extrair dados estruturados de arquivos REM."""
    
    @staticmethod
    def extrair(arquivo_entrada):
        """
        Extrai dados estruturados de um arquivo REM.
        
        Args:
            arquivo_entrada: Caminho para o arquivo .REM
        
        Returns:
            Lista de dicionários com os dados extraídos
        """
        dados = []
        try:
            with open(arquivo_entrada, "r", encoding="latin-1") as handle:
                linhas = handle.readlines()

            for linha in linhas:
                linha = linha.rstrip('\r\n')
                if len(linha) == 0:
                    continue

                flag = linha[0] if len(linha) > 0 else ""

                if flag == "0":
                    dados.append(RemExtractor._extrair_header(linha, arquivo_entrada))
                elif flag == "7":
                    dados.append(RemExtractor._extrair_detalhe(linha, arquivo_entrada))

            return dados
        except Exception as e:
            print(f"Erro ao extrair dados do arquivo REM: {e}")
            return []
    
    @staticmethod
    def _extrair_header(linha, arquivo_entrada):
        """Extrai dados do header do arquivo REM."""
        identificacao = linha[11:19] if len(linha) >= 19 else ""
        agencia = linha[26:30] if len(linha) >= 30 else ""
        agencia_dv = linha[30:31] if len(linha) >= 31 else ""
        conta = linha[31:39] if len(linha) >= 39 else ""
        conta_dv = linha[39:40] if len(linha) >= 40 else ""
        beneficiario = linha[46:76] if len(linha) >= 76 else ""
        banco = linha[76:94] if len(linha) >= 94 else ""
        data_gravacao = linha[94:100] if len(linha) >= 100 else ""
        convenio = linha[129:136] if len(linha) >= 136 else ""

        return {
            'tipo': 'HEADER',
            'identificacao': identificacao.strip(),
            'agencia': f"{agencia.strip()}-{agencia_dv.strip()}",
            'conta': f"{conta.strip()}-{conta_dv.strip()}",
            'beneficiario': beneficiario.strip(),
            'banco': banco.strip(),
            'data_gravacao': formatar_data(data_gravacao[:6]) if len(data_gravacao) >= 6 else data_gravacao,
            'convenio': convenio.strip(),
            'arquivo_origem': Path(arquivo_entrada).name
        }
    
    @staticmethod
    def _extrair_detalhe(linha, arquivo_entrada):
        """Extrai dados de detalhe do arquivo REM."""
        cpf_cnpj_beneficiario = linha[3:17] if len(linha) >= 17 else ""
        nosso_numero = linha[63:80] if len(linha) >= 80 else ""
        meu_numero = linha[110:120] if len(linha) >= 120 else ""
        codigo_controle_emp = linha[38:63] if len(linha) >= 63 else ""
        data_vencimento = linha[120:126] if len(linha) >= 126 else ""
        valor_titulo = linha[126:139] if len(linha) >= 139 else ""
        data_emissao = linha[150:156] if len(linha) >= 156 else ""
        cpf_cnpj_pagador = linha[220:234] if len(linha) >= 234 else ""
        nome_pagador = linha[234:271] if len(linha) >= 271 else ""

        return {
            'tipo': 'DETALHE',
            'cpf_cnpj_beneficiario': cpf_cnpj_beneficiario.strip(),
            'nosso_numero': nosso_numero.strip(),
            'meu_numero': meu_numero.strip(),
            'codigo_controle_emp': codigo_controle_emp.strip(),
            'data_vencimento': formatar_data(data_vencimento[:6]) if len(data_vencimento) >= 6 else data_vencimento,
            'valor_titulo': valor_titulo.strip(),
            'data_emissao': formatar_data(data_emissao[:6]) if len(data_emissao) >= 6 else data_emissao,
            'cpf_cnpj_pagador': cpf_cnpj_pagador.strip(),
            'nome_pagador': nome_pagador.strip(),
            'arquivo_origem': Path(arquivo_entrada).name
        }

