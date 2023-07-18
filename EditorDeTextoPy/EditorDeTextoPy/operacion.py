import re

##leer = input("fun: ")

def operacion(cadena):
    ##expresion regular que identifica una operacion:
    operacion = r'(([a-zA-Z]+[a-zA-Z0-9_]*[ ]*[=])|((RETORNA)[ ]*))([ ]*(([a-zA-Z]+[a-zA-Z0-9_]*)|([0-9]+)))(([ ]*[-+*/%])([ ]*(([a-zA-Z]+[a-zA-Z0-9_]*)|([0-9]+))))+' 
    
    resul = "" ##donde se van a concatenar los resultados traducidos
    if(re.search(operacion, cadena)): ##verifica si la cadena cumple con la expresión regular que está en la variable operacion
        c = cadena.split() ##guarda en aux una lista con cada palabra en la variable cadena y divide la cadena (teniendo en cuenta los espacios como divisores)
        ##print(c)
        for x in c:
            if(x == "RETORNA"): ##así con cada palabra definida en estos if anidados por cada palabra que encuentre que coincida acumulará en resultado la traducción correspondiente 
                resul = resul + " "+"RETURN"
            else:
                resul = resul + " "+x
                
        resul = resul +";" ##concatenación final

        ##print(resul) 
        return resul ##retorna la cadena traducida
    else:
        return "Syntax Error o" ##error si la cadena no cumple con la expresion regular

def mostrar_operacion(cadena):
    print(operacion(cadena))
