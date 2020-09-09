from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

from Analizador_Lexico import Analizador_Lexico
from Analizador_html import Analizador_html

import re
import sys
import os

extencion = []

def analizar():
    ext = extencion[1]
    _valor = entrada.get(1.0,END)
    cadena = _valor.strip('\n')
    #print("Analizando: "+ cadena)
    cad = cadena.split("\n")
    count = 0
    ruta = []
    cadena = ""
    for a in cad:
        if a.strip(' ').startswith('//',0) and count < 2:
            ruta.append(a)
            count +=1
        else:
            cadena = cadena + a+"\n"
    #print("ruta 1:" + ruta[0])
    #print("ruta 2:" + ruta[1])
    
    rut = ruta[0].split(":")
    dir = rut[1].strip(' ')
    #print(dir)
    if ext == "js":
        an = Analizador_Lexico()
        tokens = an.inic(cadena,dir)
        an.reserved(tokens)
        resultado = ""
        for token in tokens:
            #print(token)
            resultado = resultado + token[3]
        #print(resultado)

        creararchivo(dir,resultado,ext)
        print("archivo creado")
    elif ext == "html":
        html = Analizador_html()
        tokens = html.icic(cadena,dir)
        html.reserved(tokens)
        resultado = ""
        for token in tokens:
            #print(token)
            resultado = resultado + token[3]
        creararchivo(dir,resultado,ext)
        print("archivo creado")
    #END
#END  
  
def creararchivo(path,resultado,ext):
    try:
        os.stat(path.strip())
    except:
        os.makedirs(path.strip())
    
    with open(path+"Archivo Limpio."+ext,"w+") as file:
        file.seek(0,0)
        file.write(resultado)
        file.close()
    #END 
#END

def load_file():
    
           fname = askopenfilename(filetypes=(("HTML", "*.html"),
                                              ("CSS", "*.css"),
                                              ("Js","*.js") ))
           if fname:
               try:
                   global extencion
                   archivo = open(fname)
                   texto = archivo.read()
                   #print(texto)
                   extencion = fname.split(".")
                   print(extencion[1])
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