from AnalizadorSintacticoCalculadora import AnalisisSintactico

import re
import os

class Analizador_calculadora:
    fila = 0
    columna = 0
    counter = 0

    Errores = []
    listaTokens = []

    signos = {"PARA":'\(',"PARC":'\)',"MAS":'\+',"MENOS":'\-',"MULT":'\*',"DIV":'\/'}

    def inic(self,texto,dir):
        self.columna = 1
        self.fila = 1
        cont = 1
        cadena = ""
        while self.counter < len(texto):
            if re.search(r"[A-Za-z]", texto[self.counter]):
                self.StateIdentifier(self.fila,self.columna,texto,texto[self.counter])
            elif re.search(r"\n",texto[self.counter]):
                self.listaTokens.append([self.fila,self.columna,'ULTIMO',''])
                an = AnalisisSintactico()
                er = an.parsear(self.listaTokens)
                print(er)
                cad = ""
                for token in self.listaTokens:
                    cad = cad + token[3]
                #END

                lista = []
                correcto = ""
                if er == True:
                    correcto = "Incorrecto"
                else:
                    correcto = "Correcto"
                #END
                lista.append([self.fila,cad,correcto])
                for l in lista:
                    print(l)
                    cadena = cadena + "<tr>\n\t\t<td>"+ str(cont) +"</td>\n"
                    cadena = cadena + "\t\t<td>"+ str(l[1])+"</td>\n"
                    cadena = cadena + "\t\t<td>"+ l[2]+"</td>\n\t</tr>\n"
                    cont += 1 
                #END
                

                self.counter += 1
                self.columna = 1
                self.fila += 1
                self.listaTokens.clear()
            elif re.search(r"[ \t]",texto[self.counter]):
                self.counter += 1
                self.columna += 1
            elif re.search(r"[0-9]", texto[self.counter]):
                self.StateNumber(self.fila,self.columna,texto,texto[self.counter])
            else:
                isSign = False
                for clave in self.signos:
                    valor = self.signos[clave]
                    if re.search(valor,texto[self.counter]):
                        self.listaTokens.append([self.fila,self.columna,clave,valor.replace('\\','')])
                        self.counter += 1
                        self.columna += 1
                        isSign = True
                        break
                    #END
                #END
                if not isSign:
                    self.Errores.append([self.fila,self.columna,texto[self.counter]])
                    self.columna+= 1
                    self.counter += 1
                #END
            #END
        #END
        self.ReporteTabla(dir,cadena)
        return self.listaTokens     
    #END

    def StateIdentifier(self,line,column,text,word):
        self.counter += 1
        self.columna += 1
        if self.counter < len(text):
            if re.search(r"[A-Za-z0-9_]", text[self.counter]):
                return self.StateIdentifier(line,column,text,word+text[self.counter])
            else:
                self.listaTokens.append([line,column,'identificador',word])
            #END
        else:
            self.listaTokens.append([line,column,'identificador',word])
        #END
    #END

    def StateNumber(self,line,column,text,word):
        self.counter += 1
        self.columna += 1
        if self.counter < len(text):
            if re.search(r"[0-9]", text[self.counter]):
                return self.StateNumber(line,column,text,word+text[self.counter])
            elif re.search(r"\.",text[self.counter]):
                return self.StateDecimal(line,column,text,word+text[self.counter])
            else:
                self.listaTokens.append([line,column,'numero',word])
            #END
        #END
    #END

    def StateDecimal(self,line,column,text,word):
        self.counter += 1
        self.columna += 1
        if self.counter < len(text):
            if re.search(r"[0-9]", text[self.counter]):
                return self.StateDecimal(line,column,text,word+text[self.counter])
            else:
                self.listaTokens.append([line,column,'numero',word])
            #END
        else:
            self.listaTokens.append([line,column,'numero',word])
        #END
    #END

    def ReporteTabla(self,dir,cad):
        #Creacion del html
        cadena = "<html>\n <head> <head>\n<body>\n<center>\n<table class = \"egt\">\n\t"
        #Creacion de la tabla en html
        cadena = cadena + "\n\t\t<th>No.</th>\n\t\t<th>Operacion</th>\n\t\t<th>Analisis</th>\n\t</tr>\n" 
        cadena = cadena + cad
        #FIN de la tabla
        cadena = cadena +"</table>\n</body>\n</html>"
        self.crearArchivo(cadena,dir)
    #END

    def crearArchivo(self,cadena,path):
        try:
            os.stat(path.strip())
        except:
            os.makedirs(path.strip())
        with open(path+"Reporte Errores rmt.html","w+") as file:
            file.seek(0,0)
            file.write(cadena)
            file.close()
        #END
    #END 
#END