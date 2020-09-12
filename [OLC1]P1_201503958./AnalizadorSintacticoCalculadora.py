
class AnalisisSintactico:
    listaTokens = []
    numPreanalisis = 0
    Errores = False
    preanalisis = []
    def parsear(self,l):
        self.listaTokens = l
        self.preanalisis = self.listaTokens[0]
        self.Errores = False
        while True:
            if self.preanalisis[2] != "ULTIMO":
                self.E()
            else :
                break
        return self.Errores
        #END
    #END
    
    def E(self):
        self.T()
        self.EP()
    #END

    def EP(self):
        if self.preanalisis[2] == "MAS":
            self.match("MAS")
            self.T()
            self.EP()
        elif self.preanalisis[2]=="MENOS":
            self.match("MENOS")
            self.T()
            self.EP()
        #END
    #END

    def T(self):
        self.F()
        self.TP()
    #END

    def TP(self):
        if self.preanalisis[2] =="MULT":
            self.match("MULT")
            self.F()
            self.TP()
        elif self.preanalisis[2] == "DIV":
            self.match("DIV")
            self.F()
            self.TP()
        #END
    #END

    def F(self):
        if self.preanalisis[2] == "PARA":
            self.match("PARA")
            self.E()
            self.match("PARC")
        elif self.preanalisis[2] == "identificador":
            self.match("identificador")
        else:
            self.match("numero")
        
        #END
    #END

    def match(self,p):
        if not p == self.preanalisis[2]:
            print("Se esperaba " + self.getTipoError(p))
            self.Errores = True
        #END
        if not self.preanalisis[2] == "ULTIMO":
            self.numPreanalisis += 1
            self.preanalisis = self.listaTokens[self.numPreanalisis]
    #END

    def getTipoError(self,p):
        if p == "numero":
            return "numero"
        elif p == "MAS":
            return "MAS"
        elif p == "MENOS":
            return "MENOS"
        elif p == "MULT":
            return "MULTIPLICACION"
        elif p == "DIV":
            return "DIVISION"
        elif p == "PARA":
            return "Parentesis Izquierdo"
        elif p == "PARC":
            return "Parentesis Derecho"
        elif p == "identificador":
            return "Identificador"
        else:
            return "desconocido"
#END