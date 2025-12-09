import sys
from pathlib import Path

from src.processadores.rem_processor import RemProcessor
from src.processadores.ret_processor import RetProcessor
from src.analise import AnaliseGenerator


def processar_arquivo(arquivo_entrada, path_output):
    nome_base = arquivo_entrada.name
    nome_arquivo = arquivo_entrada.name.upper()
    
    if nome_arquivo.endswith(".RET"):
        nome_saida = nome_base.rsplit(".", 1)[0] + "_ret.txt"
        arquivo_saida = path_output / nome_saida
        print(f"Processando: {arquivo_entrada.name}")
        RetProcessor.processar(arquivo_entrada, arquivo_saida)
    elif nome_arquivo.endswith(".REM"):
        nome_saida = nome_base.rsplit(".", 1)[0] + "_rem.txt"
        arquivo_saida = path_output / nome_saida
        print(f"Processando: {arquivo_entrada.name}")
        RemProcessor.processar(arquivo_entrada, arquivo_saida)
    else:
        arquivo_saida = path_output / (nome_base + ".txt")


def main():
    diretorio_raiz = Path(__file__).parent.absolute()
    path_input = diretorio_raiz / "dataInput"
    path_output = diretorio_raiz / "dataOutput"

    path_input.mkdir(exist_ok=True)
    path_output.mkdir(exist_ok=True)

    if len(sys.argv) > 1 and sys.argv[1].upper() == "--ANALISE":
        print("Gerando arquivo de análise...")
        AnaliseGenerator.gerar(path_input, path_output)
        return

    if len(sys.argv) > 1:
        arquivo_entrada = Path(sys.argv[1])
        if not arquivo_entrada.is_absolute():
            arquivo_tentativa = path_input / arquivo_entrada
            if arquivo_tentativa.exists():
                arquivo_entrada = arquivo_tentativa

        if not arquivo_entrada.exists():
            print(f"Arquivo não encontrado: {arquivo_entrada}")
            return

        processar_arquivo(arquivo_entrada, path_output)
    else:
        arquivos_encontrados = list(path_input.glob("*.REM")) + list(path_input.glob("*.rem")) + \
                               list(path_input.glob("*.RET")) + list(path_input.glob("*.ret"))

        if not arquivos_encontrados:
            print("Nenhum arquivo .REM ou .RET encontrado no diretório dataInput")
            return

        for arquivo in arquivos_encontrados:
            processar_arquivo(arquivo, path_output)

    arquivos_rem = list(path_input.glob("*.REM")) + list(path_input.glob("*.rem"))
    arquivos_ret = list(path_input.glob("*.RET")) + list(path_input.glob("*.ret"))
    if arquivos_rem and arquivos_ret:
        print("\nGerando análise...")
        AnaliseGenerator.gerar(path_input, path_output)


if __name__ == "__main__":
    main()
