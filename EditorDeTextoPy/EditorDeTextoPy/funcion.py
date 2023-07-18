import re

##leer = input("fun: ")


##fun = r'(FUNCION)[ ]*((ENTERO)|(REAL)|(BOOLEANO)|(CARACTER)|[ ]*)[ ]*([a-zA-Z]+[a-zA-Z0-9_]*)[(](((ENTERO)|(REAL)|(BOOLEANO)|(CARACTER))[ ]*([a-zA-Z]+[a-zA-Z0-9_]*[ ]*))*[ ]*[)]'
##fun = r'(FUNCION)[ ]*((ENTERO)|(REAL)|(BOOLEANO)|(CARACTER)|[ ]*)[ ]*([a-zA-Z]+[a-zA-Z0-9_]*[ ]*)[(][ ]*(((ENTERO)|(REAL)|(BOOLEANO)|(CARACTER))[ ]*([a-zA-Z]+[a-zA-Z0-9_]*[ ]*))*[ ]*[)]'
##dic = r'(FUNCION)|(ENTERO)|(REAL)|(BOOLEANO)|(CARACTER)'

def funciones(cadena):
    nombre = r'[a-zA-Z]+[a-zA-Z0-9_]*'
    fun = r'(FUNCION)[ ]*((ENTERO)|(REAL)|(BOOLEANO)|(CARACTER)|[ ]*)[ ]*([a-zA-Z]+[a-zA-Z0-9_]*)[(](((ENTERO)|(REAL)|(BOOLEANO)|(CARACTER))[ ]*([a-zA-Z]+[a-zA-Z0-9_]*[ ]*))*[ ]*[)][ ]*[a-zA-Z]+[a-zA-Z0-9_]*[ ]*(FINF)'
    ##fun = r'(FUNCION)[ ]*((ENTERO)|(REAL)|(BOOLEANO)|(CARACTER)|[ ]*)[ ]*([a-zA-Z]+[a-zA-Z0-9_]*)[(](((ENTERO)|(REAL)|(BOOLEANO)|(CARACTER))[ ]*([a-zA-Z]+[a-zA-Z0-9_]*[ ]*))*[ ]*[)]'
    resultado = "" ##donde se van a concatenar los resultados traducidos
    if(re.search(fun, cadena)): ##verifica si la cadena cumple con la expresión regular que está en la variable fun
        aux = cadena.split() ##guarda en aux una lista con cada palabra en la variable cadena y divide la cadena (teniendo en cuenta los espacios como divisores)
        
        n = 0  ## variable utilizada para identificar iteraciones en el for
        
        ##print(aux)
        flag_name = 0

        for x in aux:   


            """for y in aux:
                if(re.search(dic,y)):
                    flag_w = 1"""
            if(x == "FUNCION"):     ##así con cada palabra definida en estos if anidados por cada palabra que encuentre que coincida acumulará en resultado la traducción correspondiente 
                resultado = resultado
            elif(x == "FINF"):
                resultado = resultado
            elif(x == "REAL"):
                resultado = resultado+" "+"float"
            elif(x == "BOOLEANO"):
                resultado = resultado+" "+"bool"
            elif(x == "CARACTER"):
                resultado = resultado+" "+"char"
            elif(x == "ENTERO"):
                resultado = resultado+" "+"int"
            elif(re.search(nombre, x)):

                palabra = aux[n]    ##guarda la palabra actual del for
                letra = palabra[-1]  ##guarda la ultima letra de esa palabra

                ##palabra2 = aux[n]

                flag_p = palabra.count("(") ##cuenta cuantas veces tiene "(" en la cadena
                flag_pa = 0

                if(flag_p > 0): ## si se encuentra un "(" entra aquí

                    flag_name = 1

                    tipo = palabra.split(sep='(') ## en una lista cada palabra es reconocida teniendo en cuenta que el separador es "(" 
                    if(tipo[1] == "ENTERO"):    ##así con cada palabra definida en estos if anidados por cada palabra que encuentre que coincida acumulará en la variable resultado la traducción correspondiente 
                        resultado = resultado +" "+ tipo[0]+ "(" + "int"
                        flag_pa = 1
                    elif(tipo[1] == "REAL"):
                        resultado = resultado +" "+ tipo[0]+ "(" + "float"
                        flag_pa = 1
                    elif(tipo[1] == "BOOLEANO"):
                        resultado = resultado +" "+ tipo[0]+ "(" + "bool"
                        flag_pa = 1
                    elif(tipo[1] == "CARACTER"):
                        resultado = resultado +" "+  tipo[0]+ "(" + "char"
                        flag_pa = 1



                if(letra != ")" and flag_pa == 0):
                
                    if(aux[n+1] == "(" or aux[n+1] == ")" or flag_name == 0):
                        flag_name = 1
                        resultado = resultado + " " + x
                    else:
                        ##print("n: ",n)
                        ##print("x: "+x)
                        ##print("aux: " +aux[n+1])
                        resultado = resultado + " "+x+","
                else:
                    if(flag_pa == 0):
                        resultado = resultado + " " + x + "{"
            elif(x == "("): ##así con cada palabra definida en estos if anidados por cada palabra que encuentre que coincida acumulará en la variable resultado la traducción correspondiente 
                resultado = resultado+" "+x
            elif(x == ")"):
                resultado = resultado+" "+x
                
            n = n+1
        
        ##final = fun+" "+nombre+ "FINF"
        resultado = resultado[:-1] ##quita una coma(,) ultima de la cadena que genera el programa
        return resultado + "}" ##concatena al final de la cadena "}"

    else:
        return "Syntax Error f" ##error si la cadena no cumple con la expresion regular


##print(funciones(leer))

def mostrar_funcion(cadena):
    print(funciones(cadena))
