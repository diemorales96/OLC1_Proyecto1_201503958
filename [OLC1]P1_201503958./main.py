from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter import Tk, Menu, messagebox, filedialog, ttk, Label, scrolledtext, INSERT, END, Button, Scrollbar, RIGHT, Y, Frame, Canvas, HORIZONTAL, VERTICAL, simpledialog, Text


from Analizador_Lexico import Analizador_Lexico
from Analizador_html import Analizador_html
from Analizador_css import Analizador_css
from Analizador_calculadora import Analizador_calculadora

import re
import sys
import os

extencion = []

def analizar():
    try:
        ext = extencion[1]
    except:
        ext = "other"
    #END

    _valor = entrada.get(1.0,END)
    if ext != "rmt":
        cadena = _valor.strip('\n')
    
        cad = cadena.split("\n")
        count = 0
        ruta = []
        cadena = ""
    
        for a in cad:
            if a.strip(' ').startswith('//') and count < 2:
                ruta.append(a)
                count +=1
            else:
                cadena = cadena + a+"\n"
            #END
        #END
        s = "pathl" in ruta[0].lower()
        if s == True:
            rut = ruta[0].split(":")
        else:
            rut = ruta[1].split(":")
        #END

        #rut = ruta[0].split(":")
        dir = rut[1].strip(' ')
    #END
    else:
        cadena = _valor
    if ext == "js":
        an = Analizador_Lexico()
        tokens = an.inic(cadena,dir)
        an.reserved(tokens)
        resultado = ""
        for token in tokens:
            resultado = resultado + token[3]
        #END
        salida.delete(1.0,END)
        salida.insert(INSERT,resultado)
        creararchivo(dir,resultado,ext)
        print("archivo creado")
    elif ext == "html":
        html = Analizador_html()
        tokens = html.icic(cadena,dir)
        html.reserved(tokens)
        resultado = ""
        for token in tokens:
            resultado = resultado + token[3]
        #END
        salida.delete(1.0,END)
        salida.insert(INSERT,resultado)
        creararchivo(dir,resultado,ext)
        print("archivo creado")
    elif ext == "css":
        css = Analizador_css()
        tokens = css.inic(cadena,dir)
        css.reserved(tokens)
        resultado = ""
        for token in tokens:
            resultado = resultado + token[3]
        #END
        salida.delete(1.0,END)
        salida.insert(INSERT,resultado)
        creararchivo(dir,resultado,ext)
        print("archivo creado")
    elif ext == "rmt":
        rmt = Analizador_calculadora()
        tokens = rmt.inic(cadena)
        
    else:
        messagebox.showerror("Error", "Tipo de archivo incorrecto")
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
                                              ("RMT", "*.rmt"),
                                              ("Js","*.js") ))
           if fname:
               try:
                   entrada.delete(1.0,END)
                   global extencion
                   archivo = open(fname)
                   texto = archivo.read()
                   extencion = fname.split(".")
                   print(extencion[1])
                   entrada.insert(INSERT,texto)
                   archivo.close()
               except:                    
                   showerror("Open Source File", "Failed to read file\n'%s'" % fname)
               return
#END

def new():
    global extencion 
    entrada.delete(1.0,END)
    extencion.clear()
#END

def save():
    global extencion
    fguardar = open(extencion[0]+extencion[1],"w+")
    fguardar.write(entrada.get(1.0,END))
    fguardar.close()
    print("Archivo Guardado")    
#END

def saveAs():
    global extencion
    guardar = filedialog.asksaveasfilename(title = "Guardar Archivo")
    fguardar = open(guardar, "w+")
    fguardar.write(entrada.get(1.0, END))
    fguardar.close()
    extencion.clear()
    extencion = guardar.split(".")
    print("Archivo Guardado")     
#END

def close_window (): 
    app.destroy()
#END


app = Tk()
app.title("Proyecto 1")
Vp = Frame(app)
menubar = Menu(app)

Vp.grid(column = 0, row = 0,padx =(70,70), pady=(10,10))

filemenu = Menu(menubar)
filemenu = Menu(menubar)
filemenu.add_command(label="Nuevo",command = new)
filemenu.add_command(label="Abrir",command = load_file)
filemenu.add_command(label="Guardar", command = save)
filemenu.add_command(label="Guardar Como",command = saveAs)
filemenu.add_command(label="Ejecutar Analizar",command = analizar)
filemenu.add_command(label="Salir",command = close_window)

menubar.add_cascade(label="File", menu=filemenu)

app.config(menu=menubar)

entrada = Text(Vp,height=30,width = 70)
entrada.grid(column=2,row = 1)
salida = Text(Vp,height=30,width = 70)
salida.grid(column = 3, row = 1)
app.mainloop()