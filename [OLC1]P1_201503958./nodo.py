from tipo import tipo
import hojas
import sigTabla
import json


class nodo:

    def __init__(self, lexema, tipo, numero, izq, der):
        self.primeros = []
        self.ultimos = []
        self.anulable = True

        self.lexema = lexema
        self.tipo = tipo
        self.numero = numero

        self.aceptacion = False
        if lexema == "#":
            self.aceptacion = True
        
        self.izq = izq
        self.der = der
    #END


    def getNodo(self):
        izq = self.izq.getNodo() if isinstance(self.izq, nodo) else None
        der = self.der.getNodo() if isinstance(self.der, nodo) else None


        if self.tipo == tipo.HOJA:

            self.anulable = False
            self.primeros.append(self.numero)
            self.ultimos.append(self.numero)

        elif self.tipo == tipo.AND:

            if ( isinstance(izq, nodo) and isinstance(der, nodo) ):
                # Anulable
                self.anulable = izq.anulable and der.anulable

                # Primeros
                if izq.anulable:
                    self.primeros.extend(izq.primeros)
                    self.primeros.extend(der.primeros)
                else:
                    self.primeros.extend(izq.primeros)

                # Ultimos
                if der.anulable:
                    self.ultimos.extend(izq.ultimos)
                    self.ultimos.extend(der.ultimos)
                else:
                    self.ultimos.extend(der.ultimos)

        elif self.tipo == tipo.OR:

            if ( isinstance(izq, nodo) and isinstance(der, nodo) ):
                # Anulable
                self.anulable = izq.anulable or der.anulable

                # Primeros
                self.primeros.extend(izq.primeros)
                self.primeros.extend(der.primeros)

                # Ultimos
                self.ultimos.extend(izq.ultimos)
                self.ultimos.extend(der.ultimos)

        elif self.tipo == tipo.KLEENE:

            if isinstance(izq, nodo):
                self.anulable = True
                self.primeros.extend(izq.primeros)
                self.ultimos.extend(izq.ultimos)

        elif self.tipo == tipo.Inte:
            if isinstance(izq,nodo):
                self.anulable = True
                self.primeros.extend(izq.primeros)
                self.ultimos.extend(izq.ultimos)
            #END
        else:
            pass

        return self
    #END


    def siguientes(self):
        izq = None if (self.izq == None) else self.izq.siguientes()
        der = None if (self.der == None) else self.der.siguientes()


        if self.tipo == tipo.AND:
            for i in izq.ultimos:
                nodo = hojas.getHoja(i)
                sigTabla.append(nodo.numero, nodo.lexema, der.primeros)


        elif self.tipo == tipo.KLEENE:
            for i in izq.ultimos:
                nodo = hojas.getHoja(i)
                sigTabla.append(nodo.numero, nodo.lexema, izq.primeros)


        else:
            pass

        return self
    #END
