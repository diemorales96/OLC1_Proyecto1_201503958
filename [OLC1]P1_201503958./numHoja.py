
class numHoja:

    def __init__(self, cont):
        self.cont = self.limpiar(cont) + 1
    #END


    def getNum(self):
        self.cont = self.cont - 1
        return self.cont
    #END


    def limpiar(self, cont):
        return len(cont.replace(".","").replace("|","").replace("*","").replace("?",""))
    #END
