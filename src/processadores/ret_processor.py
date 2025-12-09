from src.utils.formatadores import formatar_data, formatar_valor
from src.utils.ocorrencias import obter_descricao_ocorrencia
from src.utils.comandos import obter_descricao_comando
from src.utils.arquivo import gravar_substring


class RetProcessor:
    
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
                unico_header = True
                unico_detalhe = True
                nlinhas = 0

                for linha in linhas:
                    linha = linha.rstrip('\r\n')
                    if len(linha) == 0:
                        continue

                    flag = linha[0] if len(linha) > 0 else ""

                    if flag == "0":
                        RetProcessor._processar_header(saida, linha, unico_header)
                        if unico_header:
                            unico_header = False
                    elif flag == "7":
                        RetProcessor._processar_detalhe(saida, linha, unico_detalhe)
                        if unico_detalhe:
                            unico_detalhe = False
                        nlinhas = nlinhas + 1
                    elif flag == "9":
                        RetProcessor._processar_trailer(saida, linha)

                RetProcessor._gravar_rodape(saida, nlinhas)

            print("Processamento realizado com sucesso!")
            print(f"Total de lançamentos processados: {nlinhas}")
            return True

        except Exception as e:
            print(f"Erro ao processar o arquivo: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    @staticmethod
    def _processar_header(saida, linha, unico_header):
        tipo_operacao = linha[1:3] if len(linha) >= 3 else ""
        tipo_servico = linha[3:5] if len(linha) >= 5 else ""
        codigo_servico = linha[5:11] if len(linha) >= 11 else ""

        agencia = linha[26:30] if len(linha) >= 30 else ""
        agencia_dv = linha[30:31] if len(linha) >= 31 else ""
        agencia_formatada = f"{agencia}-{agencia_dv}" if agencia_dv else agencia

        conta = linha[31:39] if len(linha) >= 39 else ""
        conta_dv = linha[39:40] if len(linha) >= 40 else ""
        conta_formatada = f"{conta}-{conta_dv}" if conta_dv else conta

        nome_empresa = linha[46:76] if len(linha) >= 76 else ""
        nome_empresa = nome_empresa[:30].rstrip()

        codigo_banco = linha[76:79] if len(linha) >= 79 else ""
        nome_banco = linha[79:94] if len(linha) >= 94 else ""
        nome_banco = nome_banco[:18].rstrip()

        data_gravacao = linha[94:100] if len(linha) >= 100 else ""
        data_gravacao = formatar_data(data_gravacao[:6]) if len(data_gravacao) >= 6 else data_gravacao

        sequencial = linha[394:400] if len(linha) >= 400 else ""

        if unico_header:
            cabecalho = "TIPO OPERACAO TIPO SERV. CODIGO SERV. AG.      CONTA      EMPRESA                         BANCO            NOME DO BANCO          DT. GRAVACAO SEQ."
            gravar_substring(saida, cabecalho)
            cabecalho = "-" * 120
            gravar_substring(saida, cabecalho)

        substring = (tipo_operacao.ljust(13) +
                    tipo_servico.ljust(11) +
                    codigo_servico.ljust(13) +
                    agencia_formatada.ljust(9) +
                    conta_formatada.ljust(11) +
                    nome_empresa.ljust(32) +
                    codigo_banco.ljust(6) +
                    nome_banco.ljust(22) +
                    data_gravacao.ljust(13) +
                    sequencial)

        gravar_substring(saida, substring)
    
    @staticmethod
    def _processar_detalhe(saida, linha, unico_detalhe):
        if unico_detalhe:
            cabecalho = "NOSSO NUMERO          CONTROLE PARTICIPANTE              CARTEIRA MEU NUMERO       COMANDO DESCRICAO COMANDO                            DATA LIQUIDACAO DATA VENCIMENTO VALOR TITULO AG RECEBEDORA DATA CREDITO DESCONTO CONCEDIDO VALOR RECEBIDO"
            gravar_substring(saida, cabecalho)
            cabecalho = "-" * 275
            gravar_substring(saida, cabecalho)

        nosso_numero = linha[63:80] if len(linha) >= 80 else ""
        nosso_numero = nosso_numero[:17].strip()

        controle_participante = linha[38:63] if len(linha) >= 63 else ""
        controle_participante = controle_participante[:25].strip()

        carteira = linha[106:108] if len(linha) >= 108 else ""
        carteira = carteira.strip()

        comando = linha[108:110] if len(linha) >= 110 else ""
        comando = comando.strip()
        descricao_comando = obter_descricao_comando(comando)

        data_liquidacao = linha[110:116] if len(linha) >= 116 else ""
        data_liquidacao = formatar_data(data_liquidacao[:6]) if len(data_liquidacao) >= 6 and data_liquidacao.strip() and data_liquidacao.strip() != "000000" else "00/00/00"

        meu_numero = linha[116:126] if len(linha) >= 126 else ""
        meu_numero = meu_numero[:10].strip()

        data_vencimento = linha[146:152] if len(linha) >= 152 else ""
        data_vencimento = formatar_data(data_vencimento[:6]) if len(data_vencimento) >= 6 and data_vencimento.strip() and data_vencimento.strip() != "000000" else "00/00/00"

        valor_titulo = linha[152:165] if len(linha) >= 165 else ""
        valor_titulo = formatar_valor(valor_titulo[:13])

        agencia_recebedora = linha[168:172] if len(linha) >= 172 else ""
        agencia_recebedora = agencia_recebedora[:4].strip()

        data_credito = linha[175:181] if len(linha) >= 181 else ""
        data_credito = formatar_data(data_credito[:6]) if len(data_credito) >= 6 and data_credito.strip() and data_credito.strip() != "000000" else "00/00/00"

        desconto = linha[240:253] if len(linha) >= 253 else ""
        desconto = formatar_valor(desconto[:13])

        valor_recebido = linha[253:266] if len(linha) >= 266 else ""
        valor_recebido = formatar_valor(valor_recebido[:13])

        substring = (nosso_numero.ljust(21) +
                    controle_participante.ljust(32) +
                    carteira.ljust(9) +
                    meu_numero.ljust(17) +
                    comando.ljust(8) +
                    descricao_comando[:45].ljust(45) +
                    data_liquidacao.ljust(15) +
                    data_vencimento.ljust(15) +
                    valor_titulo.ljust(13) +
                    agencia_recebedora.ljust(15) +
                    data_credito.ljust(13) +
                    desconto.ljust(16) +
                    valor_recebido)

        gravar_substring(saida, substring)
    
    @staticmethod
    def _processar_trailer(saida, linha):
        total_registros = linha[17:23] if len(linha) >= 23 else ""
        valor_total = linha[23:35] if len(linha) >= 35 else ""
        valor_total = formatar_valor(valor_total[:12])

        cabecalho = "-" * 275
        gravar_substring(saida, cabecalho)
        gravar_substring(saida, f"Total de Registros: {total_registros.strip()}")
        gravar_substring(saida, f"Valor Total: {valor_total}")
    
    @staticmethod
    def _gravar_rodape(saida, nlinhas):
        cabecalho = "-" * 275
        gravar_substring(saida, cabecalho)
        substring = f"Total de Lancamentos Processados: {nlinhas}"
        gravar_substring(saida, substring)
