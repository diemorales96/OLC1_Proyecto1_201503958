from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

class Ejemplo2:

    def __init__(self, window):
        self.ventana = window
        self.ventana.title("Proyecto 1")
        self.menubar = Menu(self.ventana)
        frame = LabelFrame(self.ventana, text = '')
        frame.grid(row=0,column=0,columnspan=20,pady=20)

        #############################################_MENU_#############################################
        
        
        self.menu = Menu(self.menubar)
        self.menu.add_command(label = "analizar", command = self.analizar)

        self.menubar.add_cascade(label= "File", menu=self.menu)
      
        self.ventana.config(menu = self.menubar)
        ############################################_ENTRADA_############################################
        Label(frame,text='Archivo de Entrada:').grid(row=3,column=5)
        self.entrada = Text(frame, height=30, width=60)
        self.entrada.grid(row=4,column=5)

        Label(frame,text='   =>   ').grid(row=4,column=15)

        Label(frame,text='Resultado:').grid(row=3,column=16)
        self.salida = Text(frame, height=30, width=60)
        self.salida.grid(row=4,column=16)

        Label(frame,text='              ').grid(row=3,column=20)
    #END


    def fileMenu(self):
        filename = askopenfilename()

        archivo = open(filename,"r")
        texto = archivo.read()
        archivo.close()

        self.entrada.insert(INSERT,texto)
        return
    #END


    def analizar(self):
        texto = self.entrada.get("1.0",END)
        print("analizando: "+texto)

        self.printSalida()
    #END


    def printSalida(self):
        texto = "Finalizo el analisis"
        self.salida.insert(INSERT,texto)

        messagebox.showerror("Error", "Texto a mostrar:\n")
    #END


    def terminar(self):
        self.ventana.destroy()
        return
    #END
#END

###################################################################################################
if __name__ == '__main__':
    window = Tk()
    app = Ejemplo2(window)
    window.mainloop()