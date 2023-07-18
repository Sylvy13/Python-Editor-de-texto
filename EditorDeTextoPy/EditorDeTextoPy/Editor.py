from tkinter import * 
from collections import deque
from tkinter.filedialog import askopenfile, asksaveasfile
import tkinter as tk
from CiclosConClase import validarCiclos
import condicionales as con
import variables as va
import run as fun
import os

 

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget
        
    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)

class Window:
    def __init__(self, master):
        self.master = master
        self.master.option_add("*Font", "Verdana 12")

        self.Main = Frame(self.master)
        

        
        self.stack = deque(maxlen = 10)  #Creacion y configuracion de la ventana del editor
        self.stackcursor = 0
 
        self.L1 = Label(self.Main, text = "EDITOR DE TEXTO")
        self.L1.pack(padx = 5, pady = 5)
 
        self.T1 = Text(self.Main, width = 90, height = 25)
        self.T2 = Text(self.Main, width = 90, height = 10, state='disable')
        self.listado = TextLineNumbers(width=30, height = 500)
        self.listado.attach(self.T1)
        self.listado.place(x=0, y=45)
        #---------

        self.v1 = Scrollbar(orient="vertical", command=self.T1.yview)
        self.v1.pack(side=RIGHT, fill='y')
        self.T1.configure(yscrollcommand=self.v1.set)

        self.T1.tag_configure("red", foreground = "red", font = ("Verdana", "12", "bold"))
        self.T1.tag_configure("orange", foreground = "orange", font = ("Verdana", "12", "bold"))
        self.T1.tag_configure("blue", foreground = "blue", font = ("Verdana", "12", "bold"))
        self.T1.tag_configure("purple", foreground = "purple", font = ("Verdana", "12", "bold"))  #Configuracion de las etiquetas que permiten
        self.T1.tag_configure("green", foreground = "green", font = ("Verdana", "12", "bold"))    #resaltar las palabras reservadas
        self.T1.tag_configure("gold", foreground = "gold", font = ("Verdana", "12", "bold"))
        self.T1.tag_configure("brown", foreground = "brown", font = ("Verdana", "12", "bold"))
        self.T1.tag_configure("error", foreground= "white", background= "red")
        
 
        self.tags = ["orange", "blue", "purple", "green", "red", "gold", "brown"]
 
        self.wordlist = [ ["RETORNA", "FSI", "SI", "SINO","FSINO","ENTONCES", "SEGUN", "CASO", "ROMPER", "HAZ", "HACER", "MIENTRAS", "DEOTROMODO", "FSEGUN", "FINM","FUNCION", "PARA", "HASTA", "FINP", "FHAZ", "FPARA", "IMPRIMIR", "LEER", "FINF"],
                          ["ENTERO", "CARACTER", "REAL", "BOOLEANO"],
                          ["INICIO", "FINAL"],                          #Conjuntos de las palabras reservadas
                          ["VERDADERO", "FALSO"],
                          ["&&", "||", ">", "<", ">=", "<=", "!=", "==", "!"]]
 
        self.T1.bind("<Return>", lambda event: self.indent(event.widget))
         
        self.T1.pack(side=TOP,padx = 5, pady = 5)
        self.T2.pack(side=BOTTOM,padx = 5, pady = 5)
 
        #---------

        self.menu = Menu(self.Main)
        self.menu.add_command(label = "Abrir", command = self.print_stack)
        self.menu.add_command(label = "Deshacer", command = self.undo)          
        self.menu.add_command(label = "Rehacer", command = self.redo)
 
        self.master.config(menu = self.menu)
 
        self.B1 = Button(self.Main, text = "Guardar", width = 8, command = self.save)
        self.B1.pack(padx = 5, pady = 5, side = LEFT)
        
        self.B2 = Button(self.Main, text = "Limpiar", width = 8, command = self.clear)
        self.B2.pack(padx = 5, pady = 5, side = LEFT)
                                                                                        #Creacion de los botones que realizan algunas
        self.B3 = Button(self.Main, text = "Deshacer", width = 8, command = self.undo)  #de las funciones del editor
        self.B3.pack(padx = 5, pady = 5, side = LEFT)
 
        self.B4 = Button(self.Main, text = "Rehacer", width = 8, command = self.redo)
        self.B4.pack(padx = 5, pady = 5, side = LEFT)

        self.B4 = Button(self.Main, text = "Verificar", width = 8, command = self.verificar)
        self.B4.pack(padx = 5, pady = 5, side = LEFT)
 
        self.Main.pack(padx = 5, pady = 5)
 

    def redrawLineNumber(self):
        self.listado.redraw()


    def verificar(self):                        #Funcion que se encargara de verificar que el texto ingresado
        self.T2.configure(state='normal')       #este correcto mediante los automatas diseñados y programados                                  
        texto1 = self.T1.get("1.0", "end")      #por los otros grupos 
        x = texto1.split("\n")
        x.pop(len(x)-1)
        self.T2.delete("1.0","end")
        noReconocidas = []
        

        if(x[0] != "" or x[len(x)-1] != ""):
            while (x[len(x)-1] == ""):
                x.pop(len(x)-1)


            inicio = x[0].replace(" ", "")
            final = x[len(x)-1].replace(" ", "")

            if inicio !="INICIO": 
                self.T2.insert(INSERT, "No inicia\n")    
                self.error(1)           
                return 0                #Editor v2

            if final !="FINAL":
                self.T2.insert(INSERT, "No Finaliza")
                self.error(len(x))
                return 0                #Editor v2
            

            x.pop(0)
            x.pop(len(x)-1) 

            y = x.copy()

            text4 = fun.run(x)

            text1 = validarCiclos(x) 
            text1.mapCiclos()
           
            if(text1.errores):
                for a, b in zip(text1.lines, text1.errores):
                    self.error(b[1])
                    self.T2.config(state="normal")
                    self.T2.insert(INSERT, b)
                    self.T2.insert(INSERT, "\n")
                    self.T2.config(state="disable")

            text2 = va.automatas_Variables(x)     #Validacion de las variables
            if(len(text2) >= 2):
                if(va.lee_entero(text2[1])):
                    self.error(text2[1])
                    self.T2.config(state="normal")
                    self.T2.insert(INSERT, text2[0]+"\n" )
                    self.T2.config(state="disable")
    
            text3 = con.validarCondicionales(x)     #validacion de los condicionales
            if(not text3[0]):
                a = text3[1]
                for linea in a:
                    
                    self.error(linea[1]+1)
                    self.T2.config(state="normal")
                    self.T2.insert(INSERT, linea[0]+" "+str(linea[1]+1))
            

            if((not text1.errores) and (len(text2) != 2 or (len(text2) == 2 and not va.lee_entero(text2[1]))) and (text3[0])):
                
                traduccionCiclos = validarCiclos(text4)
                traduccionCiclos.mapCiclos()                 #Editor v2
                traduccionVariables = va.automatas_Variables(traduccionCiclos.lines)
                traduccionCondicionales = con.validarCondicionales(traduccionVariables)

                cont=1
                correccion = 1

                try:
                    i = y.index("")
                    y.remove("")
                except ValueError:
                    correccion = 0
                    i = 0

                for lines1, lines2 in zip(traduccionCondicionales[1], y):
                    if(lines1 == (lines2+" ")):
                        if(lines1 != "" and lines1 != " "):
                            if(cont >= i+1):
                                noReconocidas.append(cont+correccion)
                            elif(cont < i+1):
                                noReconocidas.append(cont)
                    cont +=1

                if(noReconocidas):
                    for line in noReconocidas:
                        self.error(line+1)
                        self.T2.config(state="normal")
                        self.T2.insert(INSERT, "Linea no reconocida # "+str(line+1)+"\n")
                        self.T2.config(state="disable")
                    
                    return 0

                self.T2.config(state="normal")
                self.T2.insert(INSERT, "Traduciendo...")
                self.T2.config(state="disable")


                files = [('Archivo C', '*.c')]
                file = asksaveasfile(filetypes = files, defaultextension = files)
                f = open(file.name, "w")
                
                f.write("#include <stdio.h>\n\nmain(){\n")
                for line in traduccionCondicionales[1]:
                    f.write(line + "\n")

                f.write("}")
                os.startfile(file.name)
                
            
        elif(x[0] == ""):
            self.error(1)
            self.T2.config(state="normal")
            self.T2.insert(INSERT, "No inicia \nNo finaliza")
            self.T2.config(state="disable")
        
        self.T2.config(state='disable')

    def error(self, linea):
        inicio = str(float(linea))
        print(inicio)
        self.T1.tag_add("error", inicio, inicio + "+1line")

    def tagHighlight(self):
        start = "1.0"                   #Funcion que se encarga de identificar las palabras
        end = "end"                     #reservadas y resaltarlas segun las etiquetas previamente
                                        #definidas
        for mylist in self.wordlist:
            num = int(self.wordlist.index(mylist))
 
            for word in mylist:
                self.T1.mark_set("matchStart", start)
                self.T1.mark_set("matchEnd", start)
                self.T1.mark_set("SearchLimit", end)
 
                mycount = IntVar()
                 
                while True:
                    index= self.T1.search(word,"matchEnd","SearchLimit", count=mycount, regexp = False)
 
                    if index == "": break
                    if mycount.get() == 0: break
 
                    self.T1.mark_set("matchStart", index)
                    self.T1.mark_set("matchEnd", "%s+%sc" % (index, mycount.get()))
 
                    preIndex = "%s-%sc" % (index, 1)
                    postIndex = "%s+%sc" % (index, mycount.get())
                     
                    if self.check(index, preIndex, postIndex):
                        self.T1.tag_add(self.tags[num], "matchStart", "matchEnd")
                         
 
    def check(self, index, pre, post):
        letters1 = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
                   "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

        letters2 = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
                   "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

        if self.T1.get(pre) == self.T1.get(index):
            pre = index
        else:
            if self.T1.get(pre) in letters1:
                return 0
            elif self.T1.get(pre) in letters2:    #Funcion que se encarga de validar las letras
                return 0                          #en una cadena para evitar resaltar palabras 
        if self.T1.get(post) in letters1:         #que contienen palabras reservadas
            return 0
        elif self.T1.get(post) in letters2:
            return 0
        return 1
 
 
    def scan(self):
        start = "1.0"
        end = "end"
        mycount = IntVar()
                                            #Funcion para resaltar comentarios y cadenas
        regex_patterns = [r'".*"', r'#.*']  #mediante expresiones regulares
 
        for pattern in regex_patterns:
            self.T1.mark_set("start", start)
            self.T1.mark_set("end", end)
 
            num = int(regex_patterns.index(pattern))
 
            while True:
                index = self.T1.search(pattern, "start", "end", count=mycount, regexp = True)
 
                if index == "": break
 
                if (num == 1):
                    self.T1.tag_add(self.tags[5], index, index + " lineend")
                elif (num == 0):
                    self.T1.tag_add(self.tags[6], index, "%s+%sc" % (index, mycount.get()))
 
                self.T1.mark_set("start", "%s+%sc" % (index, mycount.get()))
 
 
    def indent(self, widget):       
 
        index1 = widget.index("insert")      #Funcion que permite separar bloques de codigo
        index2 = "%s-%sc" % (index1, 1)      #mediante indentado
        prevIndex = widget.get(index2, index1)
 
        prevIndentLine = widget.index(index1 + "linestart")
        print("prevIndentLine ",prevIndentLine)
        prevIndent = self.getIndex(prevIndentLine)
        print("prevIndent ", prevIndent)
 
 
        if prevIndex == ":":
            widget.insert("insert", "\n" + "     ")
            widget.mark_set("insert", "insert + 1 line + 5char")
 
            while widget.compare(prevIndent, ">", prevIndentLine):
                widget.insert("insert", "     ")
                widget.mark_set("insert", "insert + 5 chars")
                prevIndentLine += "+5c"
            return "break"
         
        elif prevIndent != prevIndentLine:
            widget.insert("insert", "\n")
            widget.mark_set("insert", "insert + 1 line")
 
            while widget.compare(prevIndent, ">", prevIndentLine):
                widget.insert("insert", "     ")
                widget.mark_set("insert", "insert + 5 chars")
                prevIndentLine += "+5c"
            return "break"
 
 
    def getIndex(self, index):
        while True:
            if self.T1.get(index) == " ":       #Funcion directamente relacionada a la anterior
                index = "%s+%sc" % (index, 1)   #que permite obtener la ubicacion del ultimo indentado
            else:                               
                return self.T1.index(index)
            
                    
    def update(self):
        self.stackify()
        self.tagHighlight()                 #Funcion que contiene las 3 funciones que
        self.scan()                         #permiten la actualizacion del texto segun se 
        self.redrawLineNumber()              #ingresa
        self.T1.tag_remove("error", "1.0", "end")           
                                                            
    def save(self):     #Funcion que se encarga de guardar el texto en txt.
                                
        files = [('Text Document', '*.txt')]
        file = asksaveasfile(filetypes = files, defaultextension = files)
        f = open(file.name, "a")                
        f.write(self.T1.get("1.0", "end"))   
 
    def clear(self):            #Funcion para borrar todo el texto
        self.T1.delete("1.0", "end")
 
    def stackify(self):                                     #Funcion que guarda los ultimos cambios 
        self.stack.append(self.T1.get("1.0", "end - 1c"))   #aplicados al texto 
        if self.stackcursor < 9: self.stackcursor += 1
 
    def undo(self):
        if self.stackcursor != 0:       #Funcion la cual mediante los cambios almacenados
            self.clear()                #por la funcion anterior deshace lo ultimo que se agrego
            if self.stackcursor > 0: self.stackcursor -= 1
            self.T1.insert("0.0", self.stack[self.stackcursor])
 
    def redo(self):                                 
        if len(self.stack) > self.stackcursor + 1:  #Funcion la cual mediante los cambios almacenados
            self.clear()                            #por la funcion anterior rehace lo ultimo que se elimino
            if self.stackcursor < 9: self.stackcursor += 1
            self.T1.insert("0.0", self.stack[self.stackcursor])
 
    def print_stack(self):  #Funcion de prueba para mostrar el funcionamiento
        filename = askopenfile(mode='r', filetypes=[('Texto', '*.txt')])

        if filename == None:
            return 0

        self.T1.delete("0.0", END)
        f = open(filename.name, "r")
        text = f.read()
        self.T1.insert("0.0", text)
        self.update()


root = Tk()
root.title("Editor de texto")
window = Window(root)
root.geometry("1024x800")
root.bind("<Key>", lambda event: window.update())
root.bind("<B1-Motion>", lambda event: window.redrawLineNumber())
root.bind("<Button-1>", lambda event: window.redrawLineNumber())
root.bind("<MouseWheel>", lambda event: window.redrawLineNumber())
root.mainloop()