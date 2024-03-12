def pega_nome(nome_do_cliente):
    if nome_do_cliente[0] == ' ':
        nome_do_cliente = nome_do_cliente[1:]
    if nome_do_cliente[-1] == ' ':
        nome_do_cliente = nome_do_cliente[:-1]
    nome = nome_do_cliente.replace(' ','_')
    # print(nome.upper())
    return nome.upper()

def pega_sn(sn_do_cliente):
    if sn_do_cliente[0] == ' ':
        sn_do_cliente = sn_do_cliente[1:]
    if sn_do_cliente[-1] == ' ':
        sn_do_cliente = sn_do_cliente[:-1]
    return sn_do_cliente

if __name__ == "__main__":
    pega_nome()