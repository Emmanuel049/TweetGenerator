import sys
import random
LIMITE_TWEET = 280

def main(ruta, ruta_guardar):
    """Recibe una ruta con con el archivo con el formato (usuario\ttweet) y una ruta (con el archivo creado) para guardar los favoritos. Ordena el funcionamiento del programa."""
    orden_ingresada = sys.argv
    tweets = devolver_tweets_ordenados(ruta)
    if not tweets:
        return
    try:
        if orden_ingresada[1] == "generar":
            if len(orden_ingresada) > 2:
                lista_usuarios = devolver_lista_usuarios(orden_ingresada,tweets)
                if not bool(lista_usuarios):
                    return
            else:
                lista_usuarios = []
            cadenas = generar_seguimiento_cadenas(lista_usuarios,tweets)
            tweet_aleatorio = generar_tweet(cadenas)
            imprimir_tweet(tweet_aleatorio)
            agregar_favoritos(tweet_aleatorio, ruta_guardar)
            return
        if orden_ingresada[1] == "trending":
            if len(orden_ingresada) != 3:
                print ("Ingrese solo un parámetro luego de trending que indique la cantidad de trendings a recibir.")
                return
            if not orden_ingresada[2].isdigit():
                print ("Debe indicar un número de trendings a recibir.")
                return
            trendings = contar_trendings(tweets)
            lista_trendings = ordenar_trendings(trendings)
            imprimir_trendings(lista_trendings,orden_ingresada)
            return
        if orden_ingresada[1] == "favoritos":
            if len(orden_ingresada) > 3:
                print("Ingresó mas campos que los requeridos, por favor ingrese solo un número o no ingrese nada después de favoritos.")
                return
            if len(orden_ingresada) == 3 and not orden_ingresada[2].isdigit():
                print("Por favor ingrese un número luego de favoritos.")
                return
            favoritos = leer_favorito(ruta_guardar)
            imprimir_favoritos(favoritos, orden_ingresada)
            return
        print("Comando inválido, intente nuevamente")
    except IndexError:
        print("Ingrese un comando!")
                
def devolver_tweets_ordenados(ruta):
    """La función recibe la ruta y devolverá un diccionario con todos los usuarios y sus tweets correspondientes en una lista."""
    print("Procesando tweets...")
    tweets = {}
    try:
        with open(ruta, "r", encoding = "utf-8") as archivo:
            for linea in archivo:
                campo = linea.rstrip("\n").split("\t")
                pos_usuario = 0
                pos_tweet = 1
                tweets[campo[pos_usuario]] = tweets.get(campo[pos_usuario], [])
                tweets[campo[pos_usuario]].append(campo[pos_tweet])
        if not bool(tweets):
            print ("No hay tweets que mostrar.")
            return tweets
        return tweets
    except:
        print("El archivo no puede ejecutarse.")
        return tweets
        
def devolver_lista_usuarios(orden, tweets):
    """En caso de pasarse el comando 'generar', valida que los usuarios sean los correctos y que no se ingrese un usuario más de una vez, de lo contrario le avisará al usuario. Recibe la validación anterior y el diccionario de tweets y devuelve los usuarios."""
    lista_usuarios = []
    for usuario in orden[2:]:
        if usuario in tweets:
            if usuario in lista_usuarios:
                print("Ingresó el mismo usuario 2 veces")
                return []
            lista_usuarios.append(usuario)
        else:
            print("Ingresó un usuario inválido: {}".format(usuario))
            return []
    return lista_usuarios
    
def generar_seguimiento_cadenas(usuarios, tweets):
    """Procesa las cadenas en los tweets de los usuarios, recibiendo los usuarios y el diccionario de tweets, luego devuelve las cadenas con una lista de sus 'siguientes' y sus apariciones."""
    print("Procesando tweets por usuario...")
    pos_siguientes = 0
    pos_apariciones = 1
    if len(usuarios) == 0:
        usuarios_generar = tweets
    else:
        usuarios_generar = usuarios
    palabras_siguientes = {}
    for usuario in usuarios_generar:
        for tweet in tweets[usuario]:
            palabras = tweet.split(" ")
            for i in range(len(palabras)):
                comprobacion = palabras_siguientes.get(palabras[i],-1)
                if comprobacion == -1:
                    if i != len(palabras)-1:
                        palabras_siguientes[palabras[i]] = [[palabras[i+1]],1]
                    else:
                        palabras_siguientes[palabras[i]] = [[],1]
                else:
                    palabras_siguientes[palabras[i]][pos_apariciones] += 1
                    if i != len(palabras)-1:
                        palabras_siguientes[palabras[i]][pos_siguientes].append(palabras[i+1]) 
    return palabras_siguientes    #El diccionario de palabras_siguientes tiene implementado como valor en cada una de sus claves una lista, la cual tiene como valores en su primer campo una lista con las palabras siguientes a la misma (de no poseer ninguna estará vacía) y como segundo parámetro la cantidad de apariciones de la palabra clave

def generar_tweet(cadenas):
    """Recibe el diccionario de las cadenas con sus 'siguientes' y sus apariciones para generar el tweet de manera aleatoria en base al criterio establecido de cadenas de markov. Devuelve el tweet aleatorio."""
    print("Generando tweet...\n")
    cadena_total = ""
    lista_aleatoria = []
    for palabra in cadenas:
        for i in range(cadenas[palabra][1]):
            lista_aleatoria.append(palabra)
    cadena_aleatoria = random.choice(lista_aleatoria)
    cadena_total += cadena_aleatoria + " "
    while True:
        if not bool(cadenas[cadena_aleatoria][0]):
            break
        cadena_aleatoria = random.choice(cadenas[cadena_aleatoria][0])
        if (len(cadena_aleatoria) + len(cadena_total)) + 1 > LIMITE_TWEET:
            break
        cadena_total += cadena_aleatoria + " "
    return cadena_total

def imprimir_tweet(tweet_aleatorio):
    """Recibe el tweet aleatorio generado en la función previa y lo imprime."""
    print ("{}\n".format(tweet_aleatorio))

def agregar_favoritos(tweet_aleatorio, ruta_guardar):
    """Recibe el tweet aleatorio generado previamente y la ruta del archivo de almacenaje de favoritos. Pregunta al usuario si quiere guardar el tweet generado aleatoriamente en el archivo, si se ingresa una respuesta no válida se le preguntará de nuevo. Si se agrega un tweet a favoritos correrá todos los otros tweets un 'escalón' más abajo"""
    respuesta = input ("Desea agregar el tweet a favoritos? (s/n): ")
    while True:
        if respuesta.lower() == "s":
            try:
                with open(ruta_guardar, "r", encoding = "utf-8") as lectura:
                    lista_tweets = []
                    for linea in lectura:
                        lista_tweets.append(linea.rstrip("\n"))
                    lista_tweets = lista_tweets[::-1]
                with open(ruta_guardar, "w", encoding = "utf-8") as escritura:
                    lista_tweets.append(tweet_aleatorio)
                    lista_tweets = lista_tweets[::-1]
                    for x in lista_tweets:
                        escritura.write(x + "\n")
                print ("Tweet guardado a favoritos!")
                return
            except:
                with open(ruta_guardar, "w", encoding = "utf-8") as escritura:
                    escritura.write(tweet_aleatorio + "\n")
                print ("Tweet guardado a favoritos!")
                return
        if respuesta.lower() == "n":
            print ("Programa finalizado.")
            return
        if respuesta.lower() != "n" and respuesta.lower() != "s":
            respuesta = input ("Ingrese un comando válido! Quiere guardar el tweet a favoritos? (s/n): ")

def contar_trendings(tweets):
    """Recibe el diccionario de tweets establecido previamente y cuenta la cantidad de trendings en el mismo, luego devuelve un diccionario con los trendings encontrados."""
    print ("Recogiendo hashtags...")
    trendings = {}
    for x in tweets:
        for i in range(len(tweets[x])):
            lista = tweets[x][i].split(" ")
            for y in lista:
                if y[0] == "#":
                    trendings[y] = trendings.get(y, 0) +1
    return trendings
  
def ordenar_trendings(trendings):
    """Recibe el diccionario de trendings y devuelve una lista ordenada con sus apariciones de mayor a menor."""
    lista_ordenada = []
    for x in trendings:
        tupla = (trendings[x],x)
        lista_ordenada.append(tupla)
    lista_ordenada.sort()
    lista_ordenada = lista_ordenada[::-1]
    return lista_ordenada
	
def imprimir_trendings(lista_trendings, orden):
    """Recibe la lista de trendings ordenada e imprime de orden descendente la cantidad de trendings indicada al comienzo de la ejecución, de ser mayor a la cantidad total imprime todos."""
    print ("Imprimiendo trendings...")
    print ()
    if int(orden[2]) >= len(lista_trendings):
        cantidad = len(lista_trendings)
    else:
        cantidad = int(orden[2])
    for i in range (cantidad):
        print (lista_trendings[i][1])
    print("\nFinalizando programa...")

def leer_favorito(ruta_guardar):
    """Recibe la ruta de guardado de archivos favoritos y si no se ingresó un número se devolverán todos los tweets guardados como favoritos, sino se devolverá solo la cantidad indicada."""
    try:
        with open(ruta_guardar, "r", encoding = "utf-8") as favoritos:
            lista_favoritos = []
            for linea in favoritos:
                lista_favoritos.append(linea.rstrip("\n"))
            return lista_favoritos
    except:
        print("No hay tweets guardados previamente a favoritos.")
		
def imprimir_favoritos(favoritos, orden):
    """Recibe la lista de tweets favoritos y los imprime."""
    print("Imprimiendo favoritos...\n")
    if len(orden) == 2 or int(orden[2]) >= len(favoritos):
        for x in favoritos:
            print(x)
    if int(orden[2]) < len(favoritos):
        for i in range(int(orden[2])):
            print(favoritos[i])
    print("\nFinalizando programa...")

main("tweets.csv", "favoritos.csv")