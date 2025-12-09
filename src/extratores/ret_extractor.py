"""
Extrator de dados de arquivos RET.
"""

from pathlib import Path
from src.utils.formatadores import formatar_data
from src.utils.ocorrencias import obter_descricao_ocorrencia


class RetExtractor:
    """Classe para extrair dados estruturados de arquivos RET."""
    
    @staticmethod
    def extrair(arquivo_entrada):
        """
        Extrai dados estruturados de um arquivo RET.
        
        Args:
            arquivo_entrada: Caminho para o arquivo .RET
        
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
                    dados.append(RetExtractor._extrair_header(linha, arquivo_entrada))
                elif flag == "7":
                    dados.append(RetExtractor._extrair_detalhe(linha, arquivo_entrada))

            return dados
        except Exception as e:
            print(f"Erro ao extrair dados do arquivo RET: {e}")
            return []
    
    @staticmethod
    def _extrair_header(linha, arquivo_entrada):
        """Extrai dados do header do arquivo RET."""
        tipo_operacao = linha[1:3] if len(linha) >= 3 else ""
        tipo_servico = linha[3:5] if len(linha) >= 5 else ""
        codigo_servico = linha[5:11] if len(linha) >= 11 else ""
        agencia = linha[26:30] if len(linha) >= 30 else ""
        agencia_dv = linha[30:31] if len(linha) >= 31 else ""
        conta = linha[31:39] if len(linha) >= 39 else ""
        conta_dv = linha[39:40] if len(linha) >= 40 else ""
        nome_empresa = linha[46:76] if len(linha) >= 76 else ""
        codigo_banco = linha[76:79] if len(linha) >= 79 else ""
        nome_banco = linha[79:94] if len(linha) >= 94 else ""
        data_gravacao = linha[94:100] if len(linha) >= 100 else ""

        return {
            'tipo': 'HEADER',
            'tipo_operacao': tipo_operacao.strip(),
            'tipo_servico': tipo_servico.strip(),
            'codigo_servico': codigo_servico.strip(),
            'agencia': f"{agencia.strip()}-{agencia_dv.strip()}",
            'conta': f"{conta.strip()}-{conta_dv.strip()}",
            'nome_empresa': nome_empresa.strip(),
            'codigo_banco': codigo_banco.strip(),
            'nome_banco': nome_banco.strip(),
            'data_gravacao': formatar_data(data_gravacao[:6]) if len(data_gravacao) >= 6 else data_gravacao,
            'arquivo_origem': Path(arquivo_entrada).name
        }
    
    @staticmethod
    def _extrair_detalhe(linha, arquivo_entrada):
        """Extrai dados de detalhe do arquivo RET."""
        nosso_numero = linha[63:80] if len(linha) >= 80 else ""
        controle_participante = linha[38:63] if len(linha) >= 63 else ""
        meu_numero = linha[116:126] if len(linha) >= 126 else ""
        codigo_ocorrencia = linha[106:108] if len(linha) >= 108 else ""
        data_liquidacao = linha[110:116] if len(linha) >= 116 else ""
        data_vencimento = linha[146:152] if len(linha) >= 152 else ""
        valor_titulo = linha[152:165] if len(linha) >= 165 else ""
        agencia_recebedora = linha[168:172] if len(linha) >= 172 else ""
        data_credito = linha[175:181] if len(linha) >= 181 else ""
        desconto = linha[240:253] if len(linha) >= 253 else ""
        valor_recebido = linha[253:266] if len(linha) >= 266 else ""

        return {
            'tipo': 'DETALHE',
            'nosso_numero': nosso_numero.strip(),
            'controle_participante': controle_participante.strip(),
            'meu_numero': meu_numero.strip(),
            'codigo_ocorrencia': codigo_ocorrencia.strip(),
            'descricao_ocorrencia': obter_descricao_ocorrencia(codigo_ocorrencia),
            'data_liquidacao': formatar_data(data_liquidacao[:6]) if len(data_liquidacao) >= 6 and data_liquidacao.strip() != "000000" else "00/00/00",
            'data_vencimento': formatar_data(data_vencimento[:6]) if len(data_vencimento) >= 6 and data_vencimento.strip() != "000000" else "00/00/00",
            'valor_titulo': valor_titulo.strip(),
            'agencia_recebedora': agencia_recebedora.strip(),
            'data_credito': formatar_data(data_credito[:6]) if len(data_credito) >= 6 and data_credito.strip() != "000000" else "00/00/00",
            'desconto': desconto.strip(),
            'valor_recebido': valor_recebido.strip(),
            'arquivo_origem': Path(arquivo_entrada).name
        }

