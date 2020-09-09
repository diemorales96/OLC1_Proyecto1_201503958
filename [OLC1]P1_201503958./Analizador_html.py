import re
import os
class Analizador_html:
    linea = 0
    columna = 0
    counter = 0

    reservadas = {'html','head','tittle','body','h1','h2','h3','h4','h5','h6','p','br','img','a','ol','ul','style','table','th','tr','td','caption','colgroup','col','thead','tbody','tfoot','li'}
    signos = {"DOSPUNTOS":':',"IGUAL":'=',"PUNTO":'\.'}
    
    def icic(self,_valor,path):
        global linea, columna,counter
        linea = 1
        columna = 1
        listaTokens = []
        Errores = []
        bandera = False
        while self.counter < len(_valor):
            
            if re.search(r"[<]", _valor[self.counter]):
                listaTokens.append([linea,columna,'MENORQUE',_valor[self.counter]])
                self.counter += 1
                columna += 1
                bandera = True
            elif re.search(r"[>]",_valor[self.counter]):
                listaTokens.append([linea,columna,'MAYORQUE',_valor[self.counter]])
                self.counter += 1
                columna += 1
                bandera = False
            elif re.search(r"\n",_valor[self.counter]):
                listaTokens.append([linea,columna,'',_valor[self.counter]])
                self.counter += 1
                linea += 1
                columna = 1
            elif re.search(r"\/", _valor[self.counter]):
                    listaTokens.append(self.StateComment(linea,columna,_valor,_valor[self.counter]))
                    self.counter += 1
                    columna += 1
            elif re.search(r"[ \t]",_valor[self.counter]):
                listaTokens.append([linea,columna,'',_valor[self.counter]])
                self.counter += 1
                columna += 1
            elif bandera == True:
                if re.search(r"[A-Za-z]", _valor[self.counter]):
                    listaTokens.append(self.StateIdentifier(linea,columna,_valor,_valor[self.counter]))
                elif re.search(r"\"",_valor[self.counter]):
                    listaTokens.append(self.StateChain(linea,columna,_valor,_valor[self.counter]))
                else:
                    isSign = False
                    for clave in self.signos:
                        valor = self.signos[clave]
                        if re.search(valor,_valor[self.counter]):
                            listaTokens.append([linea,columna,clave,valor.replace('\\','')])
                            self.counter += 1
                            columna += 1
                            isSign = True
                            break
                        #END
                    if not isSign:
                        Errores.append([linea,columna,_valor[self.counter]])
                        columna+= 1
                        self.counter += 1
                    #END
                #END
            else:
                listaTokens.append(self.StateText(linea,columna,_valor,_valor[self.counter]))
            #END
        #END
        #for a in Errores:
            #print(a)
        self.ReporteTabla(Errores,path)
        return listaTokens
    #END

    def StateIdentifier(self,line,column,text,word):
        global counter,columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if re.search(r"[a-zA-Z_0-9]", text[self.counter]):
                return self.StateIdentifier(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'identificador', word]
            #END
        else:
            return [line, column, 'identificador', word]
        #END
    #END

    def StateText(self,line,column,text,word):
        global counter,columna,linea
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if re.search(r"[<]",text[self.counter]):
                return[line,column,'TEXTO',word]
            elif re.search(r"\/", text[self.counter]):
                self.counter -= 1
                return[line,column,'TEXTO',word] 
            elif re.search(r"\n", text[self.counter]):
                columna = 1
                linea += 1
                return self.StateText(line,column,text,word+text[self.counter])
            else:
                return self.StateText(line,column,text,word+text[self.counter])
        else:
            return[line,column,'TEXTO',word]
        #END
    #END

    def reserved(self,TokenList):
        for token in TokenList:
            if token[2] == 'identificador':
                for reservada in self.reservadas:
                    palabra = r"^" + reservada + "$"
                    if re.match(palabra,token[3],re.IGNORECASE):
                        token[2] = 'reservada'
                        break
                    #END
                #END
            #END
        #END
    #END

    def StateComment(self,line,column,text,word):
        global counter,linea,columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if re.search(r"\*", text[self.counter]):
                return self.StateComm(line,column,text,word+text[self.counter])
            elif re.search(r"[<]", text[self.counter]):
                self.counter -= 1
                return [line,column,'DIAGONAL',word]
            else:
                self.counter-= 1
                return [line,column,'DIAGONAL',word]
            #END
        else:
            self.counter -= 1
            return [line,column,'DIAGONAL',word]
        #END
    #END

    def StateComm(self, line, column, text, word):
        global linea,columna,counter
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if re.search(r"\*", text[self.counter]):
                return self.StateEndComment(line,column,text,word+text[self.counter])
            elif re.search(r"[<]", text[self.counter]):
                return [line,column,'TEXTO',word]
            elif re.search(r"\n", text[self.counter]):
                linea += 1
                columna = 1
                return self.StateComm(linea,columna,text,word+text[self.counter])
            else:
                return self.StateComm(line,column,text,word+text[self.counter])
            #END
        else:
            return [line,column,'TEXTO',word+text[self.counter]]
        #END
    #END

    def StateEndComment(self,line,column,text,word):
        global linea,columna, counter   
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if re.search(r"\*", text[self.counter]):
                return self.StateEndComment(line,column,text,word+text[self.counter])    
            elif re.search(r"\/", text[self.counter]):
                return [line,column,'COMENTARIO',word+text[self.counter]]
            else:
                return self.StateComm(line,column,text,word+text[self.counter])
            #END
        else:
            return [line,column,'TEXTO',word+text[self.counter]]
        #END
    #END

    def StateChain(self,line,column,text,word):
        global columna,counter
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if re.search(r"\"",text[self.counter]):
                return[line,column,'CADENA',word+text[self.counter]]
            elif re.search(r"[>]",text[self.counter]):
                return [line,column,'CADENA',word]
            else:
                return self.StateChain(line,column,text,word+text[self.counter])
            #END
        else:
            return[line,column,'CADENA',word+text[self.counter]]
        #END
    #END

    def ReporteTabla(self,Errores,dir):
        #Creacion del html
        cadena = "<html>\n <head> <head>\n<body>\n<center>\n<table class = \"egt\">\n\t"
        #Creacion de la tabla en html
        cadena = cadena + "\n\t\t<th>No.</th>\n\t\t<th>Linea</th>\n\t\t<th>Columna</th>\n\t\t<th>Descripcion</th>\n\t</tr>\n" 
        cont = 1
        for a in Errores:
            cadena = cadena + "<tr>\n\t\t<td>"+ str(cont) +"</td>\n"
            cadena = cadena + "\t\t<td>"+ str(a[0])+"</td>\n"
            cadena = cadena + "\t\t<td>"+ str(a[1])+"</td>\n"
            cadena = cadena + "\t\t<td>"+ a[2]+"</td>\n\t</tr>\n"
            cont += 1 
        #END
        #FIN de la tabla
        cadena = cadena +"</table>\n</body>\n</html>"
        self.crearArchivo(cadena,dir)
    #END

    def crearArchivo(self,cadena,path):
        try:
            os.stat(path.strip())
        except:
            os.makedirs(path.strip())
        with open(path+"Reporte Errores html.html","w+") as file:
            file.seek(0,0)
            file.write(cadena)
            file.close()
        #END
    #END 
#END