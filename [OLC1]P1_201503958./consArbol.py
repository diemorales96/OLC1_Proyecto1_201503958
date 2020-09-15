from numHoja import numHoja
from nodo import nodo
from tipo import tipo
import hojas


class consArbol:

    def __init__(self, er):

        # Recordar que la er ya viene aumentada
        # y esta es un conjunto de caracteres

        nh = numHoja(er)
        pila = []
        hojas.lista.clear()

        for x in reversed(list(er)):

            if x == "|":
                izq = pila.pop(len(pila) - 1)
                der = pila.pop(len(pila) - 1)

                if (isinstance(izq,nodo) and isinstance(der,nodo)):
                    n = nodo(x, tipo.OR, 0, izq, der)
                    pila.append(n)

            elif x == ".":
                izq = pila.pop(len(pila) - 1)
                der = pila.pop(len(pila) - 1)

                if (isinstance(izq,nodo) and isinstance(der,nodo)):
                    n = nodo(x, tipo.AND, 0, izq, der)
                    pila.append(n)
            
            elif x == "*":
                unario = pila.pop(len(pila) - 1)

                if (isinstance(unario,nodo)):
                    n = nodo(x, tipo.KLEENE, 0, unario, None)
                    pila.append(n)
            elif x == "?":
                unario = pila.pop(len(pila)-1)
                if(isinstance(unario,nodo)):
                    n = nodo(x,tipo.Inte,0,unario,None)
                    pila.append(n)
            else:
                n = nodo(x, tipo.HOJA, nh.getNum(), None, None)
                pila.append(n)
                hojas.addHoja(n) # Importante agregar la hoja


        self.raiz = pila.pop(len(pila) - 1)
    #END


    def getRaiz(self):
        return self.raiz
    #END
