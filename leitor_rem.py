

import os
import csv
from pathlib import Path
from datetime import datetime


def gravar_substring(arquivo_saida, substring):
    """
    Grava uma linha no arquivo de saída.
    
    Args:
        arquivo_saida: Arquivo aberto para escrita
        substring: String a ser gravada
    """
    arquivo_saida.write(substring + "\n")


def formatar_data(data_str):
    """
    Formata data de DDMMAA para DD/MM/AA.
    
    Args:
        data_str: String com data no formato DDMMAA
    
    Returns:
        String com data formatada DD/MM/AA
    """
    if len(data_str) == 6:
        return f"{data_str[0:2]}/{data_str[2:4]}/{data_str[4:6]}"
    return data_str


def obter_descricao_ocorrencia(codigo):
    """
    Retorna a descrição do código de ocorrência do Banco do Brasil.
    
    Args:
        codigo: Código de ocorrência de 2 dígitos
    
    Returns:
        String com a descrição da ocorrência
    """
    ocorrencias = {
        "00": "Cobrança registrada",
        "01": "Cobrança recusada - instrução inválida",
        "02": "Entrada confirmada",
        "03": "Entrada rejeitada",
        "04": "Transferência de carteira/entrada",
        "05": "Transferência de carteira/baixa",
        "06": "Liquidação normal",
        "07": "Liquidação parcial",
        "08": "Baixa solicitada",
        "09": "Baixado automaticamente via arquivo",
        "10": "Baixado conforme instruções da agência",
        "11": "Em ser (só no retorno mensal)",
        "12": "Abatimento concedido",
        "13": "Abatimento cancelado",
        "14": "Vencimento alterado",
        "15": "Liquidação em cartório",
        "16": "Título pago em cheque - bloqueado",
        "17": "Liquidação após baixa ou título não registrado",
        "18": "Acerto de depositária",
        "19": "Confirmação recebimento instrução de protesto",
        "20": "Confirmação recebimento instrução sustação de protesto",
        "21": "Acerto do controle do participante",
        "22": "Título com pagamento cancelado",
        "23": "Entrada do título em cartório",
        "24": "Entrada rejeitada por CEP irregular",
        "25": "Confirmação recebimento instrução de alteração de dados",
        "26": "Debitado a conta corrente",
        "27": "Retirado da compensação por instrução",
        "28": "Débito não efetuado - falta de autorização",
        "29": "Débito não efetuado - saldo insuficiente",
        "30": "Débito não efetuado - conta inexistente",
        "31": "Liquidação normal - em trânsito",
        "32": "Rejeição do pagador - alega que faturamento é indevido",
        "33": "Instrução rejeitada - tipo de valor inválido",
        "34": "Instrução rejeitada - falta de comprovante prestação de serviço",
        "35": "Instrução rejeitada - não comprovado o pagamento do título",
        "36": "Instrução rejeitada - comprovante de prestação de serviços inválido",
        "40": "Estorno de pagamento",
        "41": "Estorno de pagamento - título em cartório",
        "42": "Estorno de pagamento – baixado",
        "43": "Estorno de pagamento – liquidado",
        "44": "Estorno de liquidação",
        "51": "Título DDA reconhecido pelo pagador",
        "52": "Título DDA não reconhecido pelo pagador",
        "53": "Título DDA recusado pela CIP",
        "AA": "Controle inválido",
        "AB": "Tipo de operação inválido",
        "AC": "Tipo de serviço inválido",
        "AD": "Forma de lançamento inválida",
        "AE": "Tipo/Número de inscrição inválido",
        "AF": "Código de convenio inválido",
        "AG": "Agência/conta corrente/DV inválido",
        "AH": "Nº sequencial do registro no lote inválido",
        "AI": "Código de segmento de detalhe inválido",
        "AJ": "Tipo de movimento inválido",
        "AK": "Código da câmara de compensação do banco favorecido/depositário inválido",
        "AL": "Código do banco favorecido ou depositário inválido",
        "AM": "Agência mantenedora da conta corrente do favorecido inválida",
        "AN": "Conta corrente/DV do favorecido inválido",
        "AO": "Nome do favorecido não informado",
        "AP": "Data lançamento inválido",
        "AQ": "Tipo/quantidade da moeda inválido",
        "AR": "Valor do lançamento inválido",
        "AS": "Aviso ao favorecido - identificação inválida",
        "AT": "Tipo/Número de inscrição do favorecido inválido",
        "AU": "Logradouro do favorecido não informado",
        "AV": "Nº do local do favorecido não informado",
        "AW": "Cidade do favorecido não informada",
        "AX": "CEP/complemento do favorecido inválido",
        "AY": "Sigla do estado do favorecido inválida",
        "AZ": "Código/Nome do banco depositário inválido",
        "BA": "Código/Nome da agência depositária inválido",
        "BB": "Seu número inválido",
        "BC": "Nosso número inválido",
        "BD": "Inclusão efetuada com sucesso",
        "BE": "Alteração efetuada com sucesso",
        "BF": "Exclusão efetuada com sucesso",
        "BG": "Agência/conta impedida legalmente",
        "BH": "Empresa não pagou salário",
    }
    
    codigo = codigo.strip() if codigo else ""
    return ocorrencias.get(codigo, f"Ocorrência {codigo} não mapeada")


def formatar_valor(valor_str):
    """
    Formata valor numérico dividindo por 100 (centavos).
    
    Args:
        valor_str: String com valor numérico
    
    Returns:
        String formatada com vírgula como separador decimal e ponto como separador de milhar
    """
    try:
        if valor_str and valor_str.strip():
            valor = int(valor_str.strip()) / 100.0
            # Formata com 2 casas decimais, vírgula como separador decimal e ponto como separador de milhar
            partes = f"{valor:.2f}".split(".")
            parte_inteira = partes[0]
            parte_decimal = partes[1] if len(partes) > 1 else "00"
            
            # Adiciona separador de milhar (ponto)
            parte_inteira_formatada = ""
            for i, digito in enumerate(reversed(parte_inteira)):
                if i > 0 and i % 3 == 0:
                    parte_inteira_formatada = "." + parte_inteira_formatada
                parte_inteira_formatada = digito + parte_inteira_formatada
            
            return f"{parte_inteira_formatada},{parte_decimal}"
        return "0,00"
    except (ValueError, AttributeError):
        return valor_str if valor_str else "0,00"


def processar_arquivo_ret(arquivo_entrada, arquivo_saida):
    """
    Processa um arquivo RET e gera um arquivo REL formatado.
    
    Args:
        arquivo_entrada: Caminho para o arquivo .RET
        arquivo_saida: Caminho para o arquivo .REL de saída
    """
    # Abre o arquivo de entrada para leitura
    try:
        with open(arquivo_entrada, "r", encoding="latin-1") as handle:
            linhas = handle.readlines()
    except FileNotFoundError:
        print(f"Erro: Arquivo de entrada '{arquivo_entrada}' não encontrado.")
        return False
    except Exception as e:
        print(f"Erro ao abrir o arquivo de entrada: {e}")
        return False

    # Abre o arquivo de saída para escrita
    try:
        with open(arquivo_saida, "w", encoding="utf-8") as saida:
            unico_header = True
            unico_detalhe = True
            nlinhas = 0

            # Processa linha por linha
            for linha in linhas:
                # Remove quebra de linha e espaços extras
                linha = linha.rstrip('\r\n')
                
                if len(linha) == 0:
                    continue

                # Obtém o flag (primeiro caractere, índice 0)
                flag = linha[0] if len(linha) > 0 else ""

                if flag == "0":
                    # Header do retorno
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
                        unico_header = False

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

                elif flag == "7":
                    # Detalhe do retorno - Baseado na especificação CBR643 Banco do Brasil
                    # Posições convertidas de 1-indexed (especificação) para 0-indexed (Python)
                    if unico_detalhe:
                        cabecalho = "NOSSO NUMERO          CONTROLE PARTICIPANTE              MEU NUMERO       COD OCORR DESCRICAO DA OCORRENCIA                            DATA LIQUIDACAO DATA VENCIMENTO VALOR TITULO AG RECEBEDORA DATA CREDITO DESCONTO CONCEDIDO VALOR RECEBIDO"
                        gravar_substring(saida, cabecalho)
                        cabecalho = "-" * 225
                        gravar_substring(saida, cabecalho)
                        unico_detalhe = False

                    # Extrai campos baseado na especificação oficial CBR643
                    # Nosso-Número: posição 64-80 (Python [63:80])
                    nosso_numero = linha[63:80] if len(linha) >= 80 else ""
                    nosso_numero = nosso_numero[:17].strip()
                    
                    # Número de Controle do Participante: posição 039-063 (Python [38:63])
                    controle_participante = linha[38:63] if len(linha) >= 63 else ""
                    controle_participante = controle_participante[:25].strip()
                    
                    # Número do boleto dado pelo cedente (meu número): posição 117-126 (Python [116:126])
                    meu_numero = linha[116:126] if len(linha) >= 126 else ""
                    meu_numero = meu_numero[:10].strip()
                    
                    # Comando (código de ocorrência): posição 109-110 (Python [108:110])
                    codigo_ocorrencia = linha[108:110] if len(linha) >= 110 else ""
                    codigo_ocorrencia = codigo_ocorrencia.strip()
                    
                    # Obtém a descrição da ocorrência
                    descricao_ocorrencia = obter_descricao_ocorrencia(codigo_ocorrencia)
                    
                    # Data de liquidação: posição 111-116 (Python [110:116])
                    data_liquidacao = linha[110:116] if len(linha) >= 116 else ""
                    data_liquidacao = formatar_data(data_liquidacao[:6]) if len(data_liquidacao) >= 6 and data_liquidacao.strip() and data_liquidacao.strip() != "000000" else "00/00/00"
                    
                    # Data de vencimento: posição 147-152 (Python [146:152])
                    data_vencimento = linha[146:152] if len(linha) >= 152 else ""
                    data_vencimento = formatar_data(data_vencimento[:6]) if len(data_vencimento) >= 6 and data_vencimento.strip() and data_vencimento.strip() != "000000" else "00/00/00"
                    
                    # Valor do boleto: posição 153-165 (11 dígitos com 2 decimais, Python [152:165])
                    valor_titulo = linha[152:165] if len(linha) >= 165 else ""
                    valor_titulo = formatar_valor(valor_titulo[:13])
                    
                    # Prefixo da agência recebedora: posição 169-172 (Python [168:172])
                    agencia_recebedora = linha[168:172] if len(linha) >= 172 else ""
                    agencia_recebedora = agencia_recebedora[:4].strip()
                    
                    # Data do crédito: posição 176-181 (Python [175:181])
                    data_credito = linha[175:181] if len(linha) >= 181 else ""
                    data_credito = formatar_data(data_credito[:6]) if len(data_credito) >= 6 and data_credito.strip() and data_credito.strip() != "000000" else "00/00/00"
                    
                    # Desconto concedido: posição 241-253 (Python [240:253])
                    desconto = linha[240:253] if len(linha) >= 253 else ""
                    desconto = formatar_valor(desconto[:13])
                    
                    # Valor recebido: posição 254-266 (Python [253:266])
                    valor_recebido = linha[253:266] if len(linha) >= 266 else ""
                    valor_recebido = formatar_valor(valor_recebido[:13])

                    substring = (nosso_numero.ljust(21) +
                                controle_participante.ljust(32) +
                                meu_numero.ljust(17) +
                                codigo_ocorrencia.ljust(12) +
                                descricao_ocorrencia[:50].ljust(50) +
                                data_liquidacao.ljust(15) +
                                data_vencimento.ljust(15) +
                                valor_titulo.ljust(13) +
                                agencia_recebedora.ljust(15) +
                                data_credito.ljust(13) +
                                desconto.ljust(16) +
                                valor_recebido)

                    gravar_substring(saida, substring)
                    nlinhas = nlinhas + 1

                elif flag == "9":
                    # Trailer do retorno
                    # Total de registros e valor total devem ser extraídos das posições corretas
                    # As posições exatas dependem da especificação do trailer
                    total_registros = linha[17:23] if len(linha) >= 23 else ""
                    valor_total = linha[23:35] if len(linha) >= 35 else ""
                    valor_total = formatar_valor(valor_total[:12])

                    cabecalho = "-" * 225
                    gravar_substring(saida, cabecalho)
                    gravar_substring(saida, f"Total de Registros: {total_registros.strip()}")
                    gravar_substring(saida, f"Valor Total: {valor_total}")

            # Linha final
            if not unico_detalhe:
                cabecalho = "-" * 225
                gravar_substring(saida, cabecalho)
            
            # Total de lançamentos processados
            substring = f"Total de Lancamentos Processados: {nlinhas}"
            gravar_substring(saida, substring)

        print("Processamento realizado com sucesso!")
        print(f"Total de lançamentos processados: {nlinhas}")
        return True

    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        import traceback
        traceback.print_exc()
        return False


def extrair_dados_rem(arquivo_entrada):
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
                # Header
                identificacao = linha[11:19] if len(linha) >= 19 else ""
                agencia = linha[26:30] if len(linha) >= 30 else ""
                agencia_dv = linha[30:31] if len(linha) >= 31 else ""
                conta = linha[31:39] if len(linha) >= 39 else ""
                conta_dv = linha[39:40] if len(linha) >= 40 else ""
                beneficiario = linha[46:76] if len(linha) >= 76 else ""
                banco = linha[76:94] if len(linha) >= 94 else ""
                data_gravacao = linha[94:100] if len(linha) >= 100 else ""
                convenio = linha[129:136] if len(linha) >= 136 else ""
                
                dados.append({
                    'tipo': 'HEADER',
                    'identificacao': identificacao.strip(),
                    'agencia': f"{agencia.strip()}-{agencia_dv.strip()}",
                    'conta': f"{conta.strip()}-{conta_dv.strip()}",
                    'beneficiario': beneficiario.strip(),
                    'banco': banco.strip(),
                    'data_gravacao': formatar_data(data_gravacao[:6]) if len(data_gravacao) >= 6 else data_gravacao,
                    'convenio': convenio.strip(),
                    'arquivo_origem': Path(arquivo_entrada).name
                })
            
            elif flag == "7":
                # Detalhe
                cpf_cnpj_beneficiario = linha[3:17] if len(linha) >= 17 else ""
                nosso_numero = linha[63:80] if len(linha) >= 80 else ""
                meu_numero = linha[110:120] if len(linha) >= 120 else ""
                codigo_controle_emp = linha[38:63] if len(linha) >= 63 else ""
                data_vencimento = linha[120:126] if len(linha) >= 126 else ""
                valor_titulo = linha[126:139] if len(linha) >= 139 else ""
                data_emissao = linha[150:156] if len(linha) >= 156 else ""
                cpf_cnpj_pagador = linha[220:234] if len(linha) >= 234 else ""
                nome_pagador = linha[234:271] if len(linha) >= 271 else ""
                
                dados.append({
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
                })
        
        return dados
    except Exception as e:
        print(f"Erro ao extrair dados do arquivo REM: {e}")
        return []


def extrair_dados_ret(arquivo_entrada):
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
                # Header
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
                
                dados.append({
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
                })
            
            elif flag == "7":
                # Detalhe
                nosso_numero = linha[63:80] if len(linha) >= 80 else ""
                controle_participante = linha[38:63] if len(linha) >= 63 else ""
                meu_numero = linha[116:126] if len(linha) >= 126 else ""
                codigo_ocorrencia = linha[108:110] if len(linha) >= 110 else ""
                data_liquidacao = linha[110:116] if len(linha) >= 116 else ""
                data_vencimento = linha[146:152] if len(linha) >= 152 else ""
                valor_titulo = linha[152:165] if len(linha) >= 165 else ""
                agencia_recebedora = linha[168:172] if len(linha) >= 172 else ""
                data_credito = linha[175:181] if len(linha) >= 181 else ""
                desconto = linha[240:253] if len(linha) >= 253 else ""
                valor_recebido = linha[253:266] if len(linha) >= 266 else ""
                
                dados.append({
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
                })
        
        return dados
    except Exception as e:
        print(f"Erro ao extrair dados do arquivo RET: {e}")
        return []


def normalizar_chave(chave):
    """
    Normaliza uma chave removendo zeros à esquerda e espaços.
    
    Args:
        chave: String com a chave a ser normalizada
    
    Returns:
        String normalizada
    """
    if not chave:
        return ""
    chave = str(chave).strip()
    # Remove zeros à esquerda mas mantém pelo menos um dígito
    chave_normalizada = chave.lstrip('0') if chave.lstrip('0') else '0'
    return chave_normalizada


def gerar_arquivo_analise(path_input, path_output):
    """
    Gera arquivo Excel/CSV relacionando arquivos REM e RET.
    
    Args:
        path_input: Diretório com arquivos REM e RET
        path_output: Diretório para salvar o arquivo de análise
    """
    # Encontra todos os arquivos REM e RET
    arquivos_rem = list(path_input.glob("*.REM")) + list(path_input.glob("*.rem"))
    arquivos_ret = list(path_input.glob("*.RET")) + list(path_input.glob("*.ret"))
    
    if not arquivos_rem and not arquivos_ret:
        print("Nenhum arquivo REM ou RET encontrado no diretório de entrada.")
        return
    
    # Extrai dados de todos os arquivos
    dados_rem = {}
    dados_ret = {}
    
    for arquivo_rem in arquivos_rem:
        print(f"Extraindo dados de: {arquivo_rem.name}")
        dados = extrair_dados_rem(arquivo_rem)
        for dado in dados:
            if dado['tipo'] == 'DETALHE':
                # Tenta matching por meu_numero primeiro, depois nosso_numero
                meu_num = normalizar_chave(dado.get('meu_numero', ''))
                nosso_num = normalizar_chave(dado.get('nosso_numero', ''))
                
                if meu_num:
                    chave = f"M:{meu_num}"
                    dados_rem[chave] = dado
                if nosso_num:
                    chave = f"N:{nosso_num}"
                    dados_rem[chave] = dado
    
    for arquivo_ret in arquivos_ret:
        print(f"Extraindo dados de: {arquivo_ret.name}")
        dados = extrair_dados_ret(arquivo_ret)
        for dado in dados:
            if dado['tipo'] == 'DETALHE':
                # Tenta matching por meu_numero primeiro, depois nosso_numero
                meu_num = normalizar_chave(dado.get('meu_numero', ''))
                nosso_num = normalizar_chave(dado.get('nosso_numero', ''))
                
                if meu_num:
                    chave = f"M:{meu_num}"
                    dados_ret[chave] = dado
                if nosso_num:
                    chave = f"N:{nosso_num}"
                    dados_ret[chave] = dado
    
    # Gera arquivo CSV de análise
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo_analise = path_output / f"analise_rem_ret_{timestamp}.csv"
    
    with open(arquivo_analise, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')
        
        # Cabeçalho
        writer.writerow([
            'MEU NUMERO',
            'NOSSO NUMERO (REM)',
            'NOSSO NUMERO (RET)',
            'CONTROLE PARTICIPANTE',
            'ARQUIVO REMESSA',
            'ARQUIVO RETORNO',
            'CPF/CNPJ BENEFICIARIO',
            'CPF/CNPJ PAGADOR',
            'NOME PAGADOR',
            'DATA EMISSAO',
            'DATA VENCIMENTO',
            'VALOR TITULO',
            'CODIGO OCORRENCIA',
            'DESCRICAO OCORRENCIA',
            'DATA LIQUIDACAO',
            'DATA CREDITO',
            'VALOR RECEBIDO',
            'DESCONTO',
            'AGENCIA RECEBEDORA',
            'STATUS MATCH'
        ])
        
        # Une todas as chaves (REM e RET) e faz matching inteligente
        matches = {}
        
        # Primeiro, tenta fazer match por chave exata
        for chave in set(dados_rem.keys()) | set(dados_ret.keys()):
            rem = dados_rem.get(chave, {})
            ret = dados_ret.get(chave, {})
            
            if rem or ret:
                # Usa o nosso_numero ou meu_numero da chave
                if chave.startswith("M:"):
                    numero_exibicao = chave[2:]
                    tipo_chave = "MEU NUMERO"
                else:
                    numero_exibicao = chave[2:]
                    tipo_chave = "NOSSO NUMERO"
                
                # Se encontrou match, usa uma chave única
                if rem and ret:
                    match_key = f"MATCH_{chave}"
                    matches[match_key] = {
                        'rem': rem,
                        'ret': ret,
                        'numero_exibicao': numero_exibicao,
                        'tipo_chave': tipo_chave,
                        'status': 'MATCH'
                    }
                elif rem:
                    matches[chave] = {
                        'rem': rem,
                        'ret': {},
                        'numero_exibicao': numero_exibicao,
                        'tipo_chave': tipo_chave,
                        'status': 'SOMENTE REM'
                    }
                else:
                    matches[chave] = {
                        'rem': {},
                        'ret': ret,
                        'numero_exibicao': numero_exibicao,
                        'tipo_chave': tipo_chave,
                        'status': 'SOMENTE RET'
                    }
        
        # Escreve os dados ordenados
        for chave in sorted(matches.keys()):
            match = matches[chave]
            rem = match['rem']
            ret = match['ret']
            
            writer.writerow([
                match['numero_exibicao'],
                rem.get('nosso_numero', '') if rem else '',
                ret.get('nosso_numero', '') if ret else '',
                ret.get('controle_participante', '') if ret else '',
                rem.get('arquivo_origem', '') if rem else '',
                ret.get('arquivo_origem', '') if ret else '',
                rem.get('cpf_cnpj_beneficiario', '') if rem else '',
                rem.get('cpf_cnpj_pagador', '') if rem else '',
                rem.get('nome_pagador', '') if rem else '',
                rem.get('data_emissao', '') if rem else '',
                rem.get('data_vencimento', '') if rem else ret.get('data_vencimento', ''),
                formatar_valor(rem.get('valor_titulo', '')) if rem and rem.get('valor_titulo') else '',
                ret.get('codigo_ocorrencia', '') if ret else '',
                ret.get('descricao_ocorrencia', '') if ret else '',
                ret.get('data_liquidacao', '') if ret else '',
                ret.get('data_credito', '') if ret else '',
                formatar_valor(ret.get('valor_recebido', '')) if ret and ret.get('valor_recebido') else '',
                formatar_valor(ret.get('desconto', '')) if ret and ret.get('desconto') else '',
                ret.get('agencia_recebedora', '') if ret else '',
                match['status']
            ])
    
    total_matches = sum(1 for m in matches.values() if m['status'] == 'MATCH')
    
    print(f"\nArquivo de análise gerado: {arquivo_analise}")
    print(f"Total de registros REM: {len([m for m in matches.values() if m['rem']])}")
    print(f"Total de registros RET: {len([m for m in matches.values() if m['ret']])}")
    print(f"Total de matches: {total_matches}")
    print(f"\nO arquivo CSV pode ser aberto no Excel ou LibreOffice Calc.")
    print(f"Use o separador ';' (ponto e vírgula) ao importar.")


def processar_arquivo_rem(arquivo_entrada, arquivo_saida):
    """
    Processa um arquivo REM e gera um arquivo REL formatado.
    
    Args:
        arquivo_entrada: Caminho para o arquivo .REM
        arquivo_saida: Caminho para o arquivo .REL de saída
    """
    # Abre o arquivo de entrada para leitura
    try:
        with open(arquivo_entrada, "r", encoding="latin-1") as handle:
            linhas = handle.readlines()
    except FileNotFoundError:
        print(f"Erro: Arquivo de entrada '{arquivo_entrada}' não encontrado.")
        return False
    except Exception as e:
        print(f"Erro ao abrir o arquivo de entrada: {e}")
        return False

    # Abre o arquivo de saída para escrita
    try:
        with open(arquivo_saida, "w", encoding="utf-8") as saida:
            unico = True
            nlinhas = 0

            # Processa linha por linha
            for linha in linhas:
                # Remove quebra de linha e espaços extras
                linha = linha.rstrip('\r\n')
                
                if len(linha) == 0:
                    continue

                # Obtém o flag (primeiro caractere, índice 0)
                flag = linha[0] if len(linha) > 0 else ""

                if flag == "0":
                    # Header
                    identificacao = linha[11:19] if len(linha) >= 19 else linha[11:].ljust(8)
                    identificacao = identificacao[:8]  # Garante tamanho máximo de 8
                    
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

                elif flag == "7":
                    # Linha detalhe
                    if unico:
                        cabecalho = "CPF/CNPJ DO BENEFICIARIO      NOSSO NUMERO      CONTROLE EMPRESA          MEU NUMERO DT VENCIMENTO VALOR DO TITULO DT EMISSAO  CPF/CNPJ DO PAGADOR PAGADOR"
                        gravar_substring(saida, cabecalho)
                        cabecalho = "-" * 195
                        gravar_substring(saida, cabecalho)
                        unico = False

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
                    nlinhas = nlinhas + 1

            # Linha final
            cabecalho = "-" * 195
            gravar_substring(saida, cabecalho)
            
            # Total de lançamentos
            substring = f"Total de Lancamentos: {nlinhas}"
            gravar_substring(saida, substring)

        print("Processamento realizado com sucesso!")
        print(f"Total de lançamentos processados: {nlinhas}")
        return True

    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        return False


def main():
    """Função principal do script."""
    # Define o diretório raiz
    diretorio_raiz = Path(__file__).parent.absolute()
    
    # Define os caminhos de entrada e saída
    path_input = diretorio_raiz / "dataInput"
    path_output = diretorio_raiz / "dataOutput"
    
    # Cria os diretórios se não existirem
    path_input.mkdir(exist_ok=True)
    path_output.mkdir(exist_ok=True)
    
    # Exemplo de arquivo (pode ser modificado para aceitar argumentos)
    arquivo_entrada = path_input / "CBR653313873225120117791001.REM"
    arquivo_saida = path_output / "CBR653313873225120117791001.REL"
    
    # Verifica se deve gerar análise
    import sys
    if len(sys.argv) > 1 and sys.argv[1].upper() == "--ANALISE":
        print("Gerando arquivo de análise relacionando REM e RET...")
        gerar_arquivo_analise(path_input, path_output)
        return
    
    # Se o arquivo de entrada foi passado como argumento, usa ele
    if len(sys.argv) > 1:
        arquivo_entrada = Path(sys.argv[1])
        if not arquivo_entrada.is_absolute():
            # Tenta primeiro no diretório de entrada
            arquivo_tentativa = path_input / arquivo_entrada
            if arquivo_tentativa.exists():
                arquivo_entrada = arquivo_tentativa
            else:
                # Se não encontrar, usa o caminho fornecido diretamente
                arquivo_entrada = arquivo_entrada
        
        # Gera nome do arquivo de saída baseado no nome do arquivo de entrada
        nome_base = arquivo_entrada.name
        if nome_base.upper().endswith(".REM"):
            arquivo_saida = path_output / nome_base.replace(".REM", ".REL").replace(".rem", ".REL")
        elif nome_base.upper().endswith(".RET"):
            arquivo_saida = path_output / nome_base.replace(".RET", ".REL").replace(".ret", ".REL")
        else:
            arquivo_saida = path_output / (nome_base + ".REL")
    
    # Verifica se o arquivo de entrada existe
    if not arquivo_entrada.exists():
        print(f"Arquivo de entrada não encontrado: {arquivo_entrada}")
        print(f"Por favor, coloque o arquivo .REM ou .RET no diretório: {path_input}")
        return
    
    # Detecta o tipo de arquivo pela extensão
    nome_arquivo = arquivo_entrada.name.upper()
    if nome_arquivo.endswith(".RET"):
        print(f"Processando arquivo de RETORNO: {arquivo_entrada.name}")
        processar_arquivo_ret(arquivo_entrada, arquivo_saida)
    elif nome_arquivo.endswith(".REM"):
        print(f"Processando arquivo de REMESSA: {arquivo_entrada.name}")
        processar_arquivo_rem(arquivo_entrada, arquivo_saida)
    else:
        print(f"Tipo de arquivo não reconhecido. Use arquivos .REM ou .RET")
        return
    
    # Gera análise após processar (se houver arquivos de ambos os tipos)
    arquivos_rem = list(path_input.glob("*.REM")) + list(path_input.glob("*.rem"))
    arquivos_ret = list(path_input.glob("*.RET")) + list(path_input.glob("*.ret"))
    if arquivos_rem and arquivos_ret:
        print("\nGerando arquivo de análise relacionando REM e RET...")
        gerar_arquivo_analise(path_input, path_output)


if __name__ == "__main__":
    main()

