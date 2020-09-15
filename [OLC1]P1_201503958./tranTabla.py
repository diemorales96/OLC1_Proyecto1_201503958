from transicion import transicion

from graphviz import Digraph
from nodo import nodo
import sigTabla
import hojas


class tranTabla:

    def __init__(self, raiz):
        self.estados = []
        self.cont = 0

        # [ nombre, elementos, transiciones, Aceptacion]
        self.estados.append( ["S"+str(self.cont), raiz.primeros, [], False] )
        self.cont += 1

        for estado in self.estados:
            elementos = estado[1]

            for hoja in elementos:

                lexema, siguientes = sigTabla.getSig(hoja)

                estado_existe = False
                estado_encontrado = ""
                for e in self.estados:
                    if "".join(str(v) for v in e[1]) == "".join(str(v) for v in siguientes):
                        estado_existe = True
                        estado_encontrado = e[0]
                        break


                if not estado_existe:
                    if hojas.aceptacion(hoja):
                        estado[3] = True
                    
                    if lexema == "":
                        continue

                    nuevo = ["S"+str(self.cont), siguientes, [], False]
                    trans = transicion(estado[0], lexema, nuevo[0])
                    estado[2].append(trans)

                    self.cont += 1
                    self.estados.append(nuevo)

                else:
                    if hojas.aceptacion(hoja):
                        estado[3] = True
                    
                    trans_existe = False

                    for trans in estado[2]:
                        if trans.comparar(estado[0], lexema):
                            trans_existe = True
                            break

                    if not trans_existe:
                        trans = transicion(estado[0], lexema, estado_encontrado)
                        estado[2].append(trans)
    #END


    def grafo(self,name):
        dot = Digraph(comment='Grafica de Estados')
        dot.attr('node', shape='circle')

        # Creamos los nodos
        for e in self.estados:
            dot.node(e[0],e[0])
            if e[3]:
                dot.node(e[0], shape='doublecircle')

        #Creamos las transiciones
        for e in self.estados:
            for t in e[2]:
                dot.edge(t.eIni, t.eFin, label=t.tran)

        dot.render('/home/'+ name, view=False)
        print("Grafo de Estados Generado")
    #END


    def impTabla(self):
        for e in self.estados:
            tran = "["
            for tr in e[2]:
                tran += tr.string() + ", "

            tran += "]"

            tran = tran.replace(", ]","]")

            print(e[0],e[1],tran,e[3])
    #END
