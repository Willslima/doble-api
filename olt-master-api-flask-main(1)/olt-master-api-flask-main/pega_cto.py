def pega_cto(cabo,fibra_primaria,caixa,fibra_secundaria):
    if len(cabo) < 2 or len(fibra_primaria) < 2 or len(caixa) < 2 or len(fibra_secundaria) < 2:
        return 'Verifique os campos e tente novamente.'
    else:
        return f"_CB{cabo}_FP{fibra_primaria}_CX{caixa}_FS{fibra_secundaria}"

if __name__ == '__main__':
    pega_cto()