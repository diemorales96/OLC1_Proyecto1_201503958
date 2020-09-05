from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

from Analizador_Lexico import Analizador_Lexico

import sys

def analizar():
    _valor = entrada.get(1.0,END)
    print("Analizando: "+_valor)
    an = Analizador_Lexico()
    tokens = an.inic(_valor)
    an.reserved(tokens)
    for token in tokens:
        print(token)
#END  
  
#[fila,columna,token,valor]

def load_file():
           fname = askopenfilename(filetypes=(("HTML", "*.html"),
                                              ("CSS", "*.css"),
                                              ("Js","*.js") ))
           if fname:
               try:
                   archivo = open(fname)
                   texto = archivo.read()
                   print(texto)
                   entrada.insert(INSERT,texto)
                   archivo.close()
               except:                    
                   showerror("Open Source File", "Failed to read file\n'%s'" % fname)
               return
#END

def close_window (): 
    app.destroy()
#END


app = Tk()
app.title("Proyecto 1")
Vp = Frame(app)
menubar = Menu(app)

Vp.grid(column = 0, row = 0,padx =(50,50), pady=(10,10))

filemenu = Menu(menubar)
filemenu = Menu(menubar)
filemenu.add_command(label="Analizar",command = analizar)
filemenu.add_command(label="Abrir",command = load_file)
filemenu.add_command(label="Salir",command = close_window)

menubar.add_cascade(label="File", menu=filemenu)

app.config(menu=menubar)

entrada = Text(Vp,height=30,width = 100)
entrada.grid(column=2,row = 1)
app.mainloop()