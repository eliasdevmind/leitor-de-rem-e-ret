def formatar_data(data_str):
    if len(data_str) == 6:
        return f"{data_str[0:2]}/{data_str[2:4]}/{data_str[4:6]}"
    return data_str


def formatar_valor(valor_str):
    try:
        if valor_str and valor_str.strip():
            valor = int(valor_str.strip()) / 100.0
            partes = f"{valor:.2f}".split(".")
            parte_inteira = partes[0]
            parte_decimal = partes[1] if len(partes) > 1 else "00"

            parte_inteira_formatada = ""
            for i, digito in enumerate(reversed(parte_inteira)):
                if i > 0 and i % 3 == 0:
                    parte_inteira_formatada = "." + parte_inteira_formatada
                parte_inteira_formatada = digito + parte_inteira_formatada

            return f"{parte_inteira_formatada},{parte_decimal}"
        return "0,00"
    except (ValueError, AttributeError):
        return valor_str if valor_str else "0,00"


def normalizar_chave(chave):
    if not chave:
        return ""
    chave = str(chave).strip()
    chave_normalizada = chave.lstrip('0') if chave.lstrip('0') else '0'
    return chave_normalizada
