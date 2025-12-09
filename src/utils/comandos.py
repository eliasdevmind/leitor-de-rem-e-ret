def obter_descricao_comando(codigo):
    comandos = {
        "01": "Registro de título",
        "02": "Solicitação de baixa",
        "03": "Pedido de devolução",
        "04": "Concessão de abatimento",
        "05": "Cancelamento de abatimento",
        "06": "Alteração de vencimento",
        "07": "Alteração de controle do participante",
        "08": "Alteração de seu número",
        "09": "Protesto",
        "18": "Sustação de protesto",
        "19": "Sustação de protesto e manutenção em carteira",
        "22": "Alteração de dados do pagador",
        "23": "Alteração de dados do sacador/avalista",
        "24": "Alteração de dados do sacador/avalista e endereço do sacado",
        "31": "Alteração de outros dados",
        "35": "Desagendamento do débito automático",
        "68": "Acerto nos dados do rateio de crédito",
        "69": "Cancelamento do rateio de crédito",
    }
    
    codigo = codigo.strip() if codigo else ""
    return comandos.get(codigo, f"Comando {codigo} não mapeado")

