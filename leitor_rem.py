import sys
from pathlib import Path

from src.processadores.rem_processor import RemProcessor
from src.processadores.ret_processor import RetProcessor
from src.analise import AnaliseGenerator


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

    arquivo_entrada = path_input / "CBR653313873225120117791001.REM"
    arquivo_saida = path_output / "CBR653313873225120117791001.txt"

    if len(sys.argv) > 1:
        arquivo_entrada = Path(sys.argv[1])
        if not arquivo_entrada.is_absolute():
            arquivo_tentativa = path_input / arquivo_entrada
            if arquivo_tentativa.exists():
                arquivo_entrada = arquivo_tentativa

        nome_base = arquivo_entrada.name
        if nome_base.upper().endswith((".REM", ".RET")):
            arquivo_saida = path_output / (nome_base.rsplit(".", 1)[0] + ".txt")
        else:
            arquivo_saida = path_output / (nome_base + ".txt")

    if not arquivo_entrada.exists():
        print(f"Arquivo não encontrado: {arquivo_entrada}")
        return

    nome_arquivo = arquivo_entrada.name.upper()
    if nome_arquivo.endswith(".RET"):
        print(f"Processando: {arquivo_entrada.name}")
        RetProcessor.processar(arquivo_entrada, arquivo_saida)
    elif nome_arquivo.endswith(".REM"):
        print(f"Processando: {arquivo_entrada.name}")
        RemProcessor.processar(arquivo_entrada, arquivo_saida)
    else:
        print("Tipo de arquivo não reconhecido")
        return

    arquivos_entrada = list(path_input.glob("*.REM")) + list(path_input.glob("*.rem"))
    arquivos_saida = list(path_input.glob("*.RET")) + list(path_input.glob("*.ret"))
    if arquivos_entrada and arquivos_saida:
        print("\nGerando análise...")
        AnaliseGenerator.gerar(path_input, path_output)


if __name__ == "__main__":
    main()
