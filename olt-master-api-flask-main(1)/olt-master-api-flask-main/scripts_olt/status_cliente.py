
from pesquisa_cliente import pesquisa_cliente

def status_cliente(nome):
    resultado = pesquisa_cliente(nome)      
    return resultado

if __name__ == '__main__':
    status_cliente('WILLIAN_SANTOS_LIMA')