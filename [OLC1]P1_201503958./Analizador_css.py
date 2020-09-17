import re
import os

class Analizador_css:

    linea = 0
    columna = 0 
    counter = 0

    listaToknes = []
    Errores = []

    reservadas = {'color','background-color','background-image','border','opacity','background','text-align','font-family','font-size','font-weight','font-size','font','padding-left','padding-rigth','padding-bottom','padding-top','padding','display','line-height','width','height','margin-top','margin-rigth','margin-bottom','margin-left','margin','border-style','position','bottom','top','rigth','left','float','clear','max-width','min-width','max-height','min-height'}
    signos = {"LLAVEA":'{',"LLAVEC":'}',"DOSPUNTOS":'\:',"PUNTOYCOMA":';',"MULT":'\*',"NUMERAL":'#',"PUNTO":'\.',"COMA":',',"MENOS":'\-',"PARA":'\(',"PARC":'\)',"MOD":'%'}
    def inic(self,texto,dir):
        global linea,columna,counter,Errores
        #listaToknes = []
        #Errores = []
        linea = 1
        columna = 1
        print("==========Bitacora:===========")
        while self.counter < len(texto):
            if re.search(r"[A-Za-z]", texto[self.counter]):
                print("S0 -> S1: con " + texto[self.counter])
                self.listaToknes.append(self.StateIdentifier(linea,columna,texto,texto[self.counter]))
            elif re.search(r"[0-9]", texto[self.counter]):
                print("S0 -> S2: con " + texto[self.counter])
                self.listaToknes.append(self.StateNumber(linea,columna,texto,texto[self.counter]))
            elif re.search(r"\/", texto[self.counter]):
                print("S0 -> S3: con " + texto[self.counter])
                count = self.counter
                self.StateComment(linea,columna,texto,texto[self.counter],count)
            elif re.search(r"\"", texto[self.counter]):
                print("S0 -> S4: con " + texto[self.counter])
                count = self.counter
                self.listaToknes.append(self.StateChain(linea,columna,texto,texto[self.counter],count))
            elif re.search(r"\n",texto[self.counter]):
                self.listaToknes.append([linea,columna,'',texto[self.counter]])
                linea += 1
                columna = 1
                self.counter += 1          
            elif re.search(r"[ \t]", texto[self.counter]):
                self.listaToknes.append([linea,columna,'',texto[self.counter]])
                columna += 1
                self.counter += 1
            else:
                isSign = False
                for clave in self.signos:
                    valor = self.signos[clave]
                    if re.search(valor,texto[self.counter]):
                        print("S0 -> S5: con " + texto[self.counter])
                        self.listaToknes.append([linea,columna,clave,valor.replace('\\','')])
                        self.counter += 1
                        columna += 1
                        isSign = True
                        break
                    #END
                if not isSign:
                    self.Errores.append([linea,columna,texto[self.counter]])
                    columna+= 1
                    self.counter += 1
        #for a in self.Errores:
            #print(a)
        self.ReporteTabla(self.Errores,dir)
        return self.listaToknes
    #END
    #S1
    def StateIdentifier(self,line,column,text,word):
        global columna,counter
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if re.search(r"[A-Za-z0-9\-]", text[self.counter]):
                print("S1 -> S1: con " + text[self.counter])
                return self.StateIdentifier(line,column,text,word+text[self.counter])
            else:
                print("S1 -> S0: con "+text[self.counter])
                return [line,column,'identificador',word]
            #END
        else:
            print("S1 -> S0: con "+text[self.counter])
            return [line,column,'identificador',word]
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
    #S2
    def StateNumber(self,line,column,text,word):
        global columna,counter
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if re.search(r"[0-9]", text[self.counter]):
                print("S2 -> S2: con "+text[self.counter])
                return self.StateNumber(line,column,text,word+text[self.counter])
            elif re.search(r"\.", text[self.counter]):
                print("S2 -> S5: con "+text[self.counter])
                return self.StateDecimal(line,column,text,word+text[self.counter])
            else:
                print("S2 -> S0: con "+text[self.counter])
                return [line,column,'ENTERO',word]
            #END
        else:
            print("S2 -> S0: con "+text[self.counter])
            return[line,column,'ENTERO',word]
    #END
    #S5
    def StateDecimal(self,line,column,text,word):
        global columna,counter
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if re.search(r"[0-9]", text[self.counter]):
                print("S5 -> S5: con "+text[self.counter])
                return self.StateDecimal(line,column,text,word+text[self.counter])
            else:
                print("S5 -> S0: con "+text[self.counter])
                return [line,column,'DECIMAL',word]
            #END
        else:
            print("S5 -> S0: con "+text[self.counter])
            return [line,column,'DECIMAL',word]
        #END
    #END
    #S3
    def StateComment(self,line,column,text,word,count):
        global counter, columna,Errores
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if re.search(r"\*", text[self.counter]):
                print("S3 -> S6: con "+text[self.counter])
                return self.StateTComment(line,column,text,word+text[self.counter],count)
            else:
                self.Errores.append([line,column,word])
                self.counter += 1
                columna += 1
            #END
        else:
            self.Errores.append([line,column,word])
            self.counter += 1
            columna += 1
        #END
    #END
    #S6
    def StateTComment(self,line,column,text,word,count):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if re.search(r"\*",text[self.counter]):
                print("S6 -> S7: con "+text[self.counter])
                return self.StateFComment(line,column,text,word+text[self.counter],count)
            else:
                print("S6 -> S6: con "+text[self.counter])
                return self.StateTComment(line,column,text,word+text[self.counter],count)
            #END
        else:
            columna = column + 1
            self.counter = count + 1
            self.Errores.append([line,column,word[0]])
        #END
    #END
    #S7
    def StateFComment(self,line,column,text,word,count):
        global counter,columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if re.search(r"\/", text[self.counter]):
                self.counter += 1
                columna += 1
                print("S7 -> S0: con "+text[self.counter])
                self.listaToknes.append([line,column,'COMENTARIO',word+text[self.counter-1]])
            elif re.search(r"\*", text[self.counter]):
                print("S7 -> S7: con "+text[self.counter])
                return self.StateFComment(line,column,text,word+text[self.counter],count)
            else:
                print("S7 -> S6: con "+text[self.counter])
                return self.StateTComment(line,column,text,word+text[self.counter],count)
            #END
        else:
            columna = column + 1
            self.counter = count + 1
            self.Errores.append([line,column,word[0]])
        #END
    #END    
    #S4
    def StateChain(self,line,column,text,word,count):
        global columna, counter
        columna += 1
        self.counter += 1
        if self.counter < len(text):
            if re.search(r"\"", text[self.counter]):
                self.counter += 1
                print("S4 -> S0: con "+text[self.counter])
                return [line,column,'CADENA',word+text[self.counter-1]]
            elif re.search(r"\n", text[self.counter]):
                self.counter = count + 1
                columna = column + 1
                print("S4 -> S0: con "+text[self.counter])
                return [line,column,'CADENA', word[0]]
            else:
                print("S4 -> S4: con "+text[self.counter])
                return self.StateChain(line,column,text,word+text[self.counter],count)
            #END
        else:
            self.counter = count + 1
            columna = column + 1
            print("S4 -> S0: con "+text[self.counter])
            return [line,column,'CADENA',word[0]]
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
        with open(path+"Reporte Errores css.css","w+") as file:
            file.seek(0,0)
            file.write(cadena)
            file.close()
        #END
    #END 
#END