from pesquisa_cliente_sn import pesquisa_cliente_sn
from scripts_olt.excluir_cliente import excluir_cliente

def sn_exists(eqp):
    cliente = pesquisa_cliente_sn(eqp)
    for client in cliente:
        excluir_cliente(client)
    
    print(f'cliente\n {client}')

if __name__ == "__main__":
    sn_exists()        