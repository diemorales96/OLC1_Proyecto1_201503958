
tabla = []

def append(numNodo, lexema, sigLista):
    global tabla

    for sig in tabla:
        if (sig[0] == numNodo) and (sig[1] == lexema):
            for new in sigLista:
                if not(new in sig[2]):
                    sig[2].append(new)

            return

    tabla.append( [numNodo, lexema, sigLista] )
#END


def getSig(numNodo):
    global tabla

    for sig in tabla:
        if (sig[0] == numNodo):
            return sig[1],sig[2]

    return "",[]
#END


def impTabla():
    global tabla

    for sig in tabla:
        print(sig[0],sig[1],sig[2])
#END
