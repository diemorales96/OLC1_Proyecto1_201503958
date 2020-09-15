
lista = []

def addHoja(nodo):
    global lista
    lista.append(nodo)
#END


def getHoja(numHoja):
    global lista

    for h in lista:
        if h.numero == numHoja:
            return h
    
    return None
#END


def aceptacion(numHoja):
    global lista

    for h in lista:
        if h.numero == numHoja:
            return h.aceptacion
    
    return False
#END
