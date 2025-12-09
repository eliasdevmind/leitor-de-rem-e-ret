"""
Módulo para geração de arquivos de análise relacionando REM e RET.
"""

import csv
from pathlib import Path
from datetime import datetime

from src.extratores.rem_extractor import RemExtractor
from src.extratores.ret_extractor import RetExtractor
from src.utils.formatadores import formatar_valor, normalizar_chave


class AnaliseGenerator:
    """Classe para gerar arquivos de análise relacionando REM e RET."""
    
    @staticmethod
    def gerar(path_input, path_output):
        """
        Gera arquivo CSV relacionando arquivos REM e RET.
        
        Args:
            path_input: Diretório com arquivos REM e RET
            path_output: Diretório para salvar o arquivo de análise
        """
        arquivos_rem = list(path_input.glob("*.REM")) + list(path_input.glob("*.rem"))
        arquivos_ret = list(path_input.glob("*.RET")) + list(path_input.glob("*.ret"))

        if not arquivos_rem and not arquivos_ret:
            print("Nenhum arquivo REM ou RET encontrado no diretório de entrada.")
            return

        dados_rem = {}
        dados_ret = {}

        # Extrai dados dos arquivos REM
        for arquivo_rem in arquivos_rem:
            print(f"Extraindo dados de: {arquivo_rem.name}")
            dados = RemExtractor.extrair(arquivo_rem)
            for dado in dados:
                if dado['tipo'] == 'DETALHE':
                    meu_num = normalizar_chave(dado.get('meu_numero', ''))
                    nosso_num = normalizar_chave(dado.get('nosso_numero', ''))

                    if meu_num:
                        chave = f"M:{meu_num}"
                        dados_rem[chave] = dado
                    if nosso_num:
                        chave = f"N:{nosso_num}"
                        dados_rem[chave] = dado

        # Extrai dados dos arquivos RET
        for arquivo_ret in arquivos_ret:
            print(f"Extraindo dados de: {arquivo_ret.name}")
            dados = RetExtractor.extrair(arquivo_ret)
            for dado in dados:
                if dado['tipo'] == 'DETALHE':
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

        matches = AnaliseGenerator._criar_matches(dados_rem, dados_ret)
        AnaliseGenerator._escrever_csv(arquivo_analise, matches)
        
        AnaliseGenerator._exibir_resumo(arquivo_analise, matches)
    
    @staticmethod
    def _criar_matches(dados_rem, dados_ret):
        """Cria dicionário de matches entre REM e RET."""
        matches = {}

        for chave in set(dados_rem.keys()) | set(dados_ret.keys()):
            rem = dados_rem.get(chave, {})
            ret = dados_ret.get(chave, {})

            if rem or ret:
                if chave.startswith("M:"):
                    numero_exibicao = chave[2:]
                else:
                    numero_exibicao = chave[2:]

                if rem and ret:
                    match_key = f"MATCH_{chave}"
                    matches[match_key] = {
                        'rem': rem,
                        'ret': ret,
                        'numero_exibicao': numero_exibicao,
                        'status': 'MATCH'
                    }
                elif rem:
                    matches[chave] = {
                        'rem': rem,
                        'ret': {},
                        'numero_exibicao': numero_exibicao,
                        'status': 'SOMENTE REM'
                    }
                else:
                    matches[chave] = {
                        'rem': {},
                        'ret': ret,
                        'numero_exibicao': numero_exibicao,
                        'status': 'SOMENTE RET'
                    }

        return matches
    
    @staticmethod
    def _escrever_csv(arquivo_analise, matches):
        """Escreve o arquivo CSV de análise."""
        with open(arquivo_analise, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')

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
    
    @staticmethod
    def _exibir_resumo(arquivo_analise, matches):
        """Exibe resumo da análise gerada."""
        total_matches = sum(1 for m in matches.values() if m['status'] == 'MATCH')

        print(f"\nArquivo de análise gerado: {arquivo_analise}")
        print(f"Total de registros REM: {len([m for m in matches.values() if m['rem']])}")
        print(f"Total de registros RET: {len([m for m in matches.values() if m['ret']])}")
        print(f"Total de matches: {total_matches}")
        print(f"\nO arquivo CSV pode ser aberto no Excel ou LibreOffice Calc.")
        print(f"Use o separador ';' (ponto e vírgula) ao importar.")

