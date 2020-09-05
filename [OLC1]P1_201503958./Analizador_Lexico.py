import re
class Analizador_Lexico:
    linea = 0
    columna = 0
    counter = 0
    Errores = []
      
    reservadas = {'var','this','class','math','true','false','PATHL','int','string','char','bollean','type','if','for','while','do','continue','break','return'}
    signos = {"LLAVEA":'{',"LLAVEC":'}',"CORA":'\[',"CORC":'\]',"PARA":'\(',"PARAC":' \)',"MENOS":'\-',"MULT":'\*',"PUNTOYC":'\;',"DOSPUN":'\:',"COMA":'\,',"PUNTO":'\.',"SUMA":'\+',"Negacion":'!',"AND":'&',"Barra":'\|',"COMSIMPLE":'\'',"COMDOBLE":'\"'}
    
    def inic (self,_valor):
        global linea ,columna,counter,Errores
        linea = 1
        columna = 1
        listaTokens = []

        while self.counter < len(_valor):

            if re.search(r"[A-Za-zñÑ]", _valor[self.counter]): 
                listaTokens.append(self.StateIdentifier(linea, columna, _valor, _valor[self.counter]))
            elif re.search(r"[0-9]", _valor[self.counter]): 
                listaTokens.append(self.StateNumber(linea,columna,_valor,_valor[self.counter]))
            elif re.search(r"\n",_valor[self.counter]):
                self.counter+=1
                linea = 1
                columna = 1
            elif re.search(r"[ \t]",_valor[self.counter]):
                self.counter +=1
                columna +=1
            elif re.search(r"\/",_valor[self.counter]):
                listaTokens.append(self.StateDiv(linea,columna,_valor,_valor[self.counter]))
            elif re.search(r"\"",_valor[self.counter]):
                listaTokens.append(self.StateChain(linea,columna,_valor,_valor[self.counter]))
                self.counter += 1
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
                if not isSign:
                    columna+= 1
                    self.counter += 1
                    self.Errores.append([linea,columna,_valor[self.counter]])
            #END
        #END   
        return listaTokens  
    #END

    def StateIdentifier(self,line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if re.search(r"[a-zA-Z_0-9ñÑ]", text[self.counter]):
                return self.StateIdentifier(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'identificador', word]
            #END
        else:
            return [line, column, 'identificador', word]
        #END
    #END

    def StateNumber(self,line,column,text,word):
        global columna, counter
        self.counter += 1
        if self.counter < len(text):
            if re.search(r"[0-9]",text[self.counter]):
                return self.StateNumber(line,column,text,word+text[self.counter])
            elif re.search(r"\.", text[self.counter]):
                return self.StateDecimal(line,column,text,word+text[self.counter])
            else:
                return[line,column,'Entero',word]
            #END
        #END
    #END

    def StateDecimal(self,line,column,text,word):
        global counter,columna
        self.counter += 1
        self.columna += 1
        if self.counter < len(text): 
            if re.search(r"[0-9]", text[self.counter]):
                return self.StateDecimal(line,column,text, word+text[self.counter])
            else:
                return [line, column, 'decimal', word]
            #END
        else:
            return [line, column, 'decimal', word]
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

    def StateDiv(self,line,column,text,word): 
        global columna,counter
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if re.search(r"\/", text[self.counter]):
                return self.StateSComent(line,column,text,word+text[self.counter])
            elif re.search(r"\*",text[self.counter]):
                count = self.counter-1
                return self.StateMComent(line,column,text,word+text[self.counter],count)
            else:
                return [line, column,'Division',word]
        else:
            return [line, column,'Division',word]
        #END
    #END

    def StateSComent(self, line, column, text,word):
        global columna, counter
        self.counter += 1
        columna += 1
        if self.counter<len(text):
            if re.search(r"\n", text[self.counter]):
                return [line,columna,'COMENTARIO_SIMPLE',word]
            else:
                return self.StateSComent(line,column,text,word+text[self.counter])
        else:
            return [line,columna,'COMENTARIO_SIMPLE',word]
        #END
    #END

    
    def StateMComent(self,line,column,text,word,count):
        global columna, counter,linea
        self.counter += 1
        columna += 1
        if self.counter <len(text):
            if re.search(r"\*", text[self.counter]):
                return self.StateMComnetFin(line,column,text,word+text[self.counter],count)
            elif re.search(r"\n",text [self.counter]):
                linea += 1
                columna = 1
                return self.StateMComent(line,column,text,word+text[self.counter],count)
            else: 
                return self.StateMComent(line,column,text,word+text[self.counter],count)
        else:
            self.counter = count + 1 
            return [line,column,'Division',word[0]]
    #END

    def StateMComnetFin(self,line,column,text,word,count):
        global columna, counter,linea
        self.counter += 1
        columna += 1
        
        if self.counter < len(text):
            if re.search(r"\*",text[self.counter]):
                self.counter -= 1
                return self.StateMComent(line,column,text,word+text[self.counter],count) 
            elif re.search(r"\/",text[self.counter]):
                self.counter +=1
                return[line,column,'ComentarioMultilinea',word]
            elif re.search(r"\n",text[self.counter]):
                linea += 1
                columna = 1
                return self.StateMComent(line,column,text,word+text[self.counter],count)
            else:
                return self.StateMComnetFin(line,column,text,word+text[self.counter],count)
            #END
        else:
            self.counter = count + 1 
            return [line,column,'Division',word[0]]
        #END
    #END
    def StateChain(self,line,column,text,word):
        global counter,columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if re.search(r"\n",text[self.counter]):
                return [line,column,'Cadena',word]
            elif re.search(r"\"",text[self.counter]):
                return [line,column,'Cadena',word+text[self.counter]]
            else:
                return self.StateChain(line,column,text,word+text[self.counter])
        #END
    #END   
#END