import re

##leer = input("fun: ")
##def linea_error_l(cadena):
  ##  if(llamado(cadena) == "Syntax Error l"):
   ##     return cadena

def llamado(cadena):
    ##expresion regular que identifica un llamado:
    exp = r'([a-zA-Z]+[a-zA-Z0-9_]*)[(]([a-zA-Z]+[a-zA-Z0-9_]*[ ]*)*[ ]*[)]'


    ##exp = r'([a-zA-Z]+[a-zA-Z0-9_]*[ ]*)[(][ ]*([a-zA-Z]+[a-zA-Z0-9_]*[ ]*)*[ ]*[)]'


    aux = cadena.split() ##guarda en aux una lista con cada palabra en la variable cadena y divide la cadena (teniendo en cuenta los espacios como divisores)
    
    resultado= ""  ##donde se van a concatenar los resultados traducidos
    ##print(aux)

    
    noerror = 0
    if(re.search(exp,cadena)):  ##verifica si la cadena cumple con la expresión regular que está en la variable operacion
        noerror = 1
    else:
        noerror = 2
        


    n=0
    
    if(noerror == 1):
        for x in aux:
            if(re.search(r'[a-zA-Z]+[a-zA-Z0-9_]*',x)): ##verifica si la cadena cumple con la expresión regular que está en la variable operacion


                palabra = aux[n] ##guarda la palabra actual del for
                letra = palabra[-1] ##guarda la ultima letra de esa palabra

                if(letra != ")"): ##así con cada palabra definida en estos if anidados por cada palabra que encuentre que coincida acumulará en la variable resultado la traducción correspondiente 
                    if(aux[n+1] == "(" or aux[n+1] == ")"):
                        resultado = resultado + " " + x
                    else:
                        resultado = resultado + " "+x+","
                else:
                    resultado = resultado + " " + x



            elif(x == "("): ##así con cada palabra definida en estos if anidados por cada palabra que encuentre que coincida acumulará en la variable resultado la traducción correspondiente 
                 resultado = resultado + x
            elif(x == ")"):
                resultado = resultado + x
                    


            n = n+1
        return resultado + ";" ##concatenación final
    else:
        return "Syntax Error l" ##error si la cadena no cumple con la expresión regular


def mostrar_llamado(cadena):
    print(llamado(cadena))


