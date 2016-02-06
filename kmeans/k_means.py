import sys
import math
import re
import copy
from sys import argv


#funcion para determinar que la linea es valida
# es valida si contiene el numero de atributos correctos
def valid_line(s_line):
	r_value = False
	if len(s_line)==len(atributes):
		r_value = True
	return r_value

#funcion auxiliar para copiar los atributos a la variable global atributes
def atr_copy(my_list):
	for e in my_list:
		atributes.append(e)

#READ FILE DEL EJERCICIO

def read_file(filename):
	line_number = 0
	ret_instances = []
	with open(filename,'r') as file_obj:
		for line in file_obj:
			line_list = line[:-2].split(',')
			# quita dos caracteres del final de cada linea, aparecen \r\n
			# \r es el carry return
			if line_number==0 :
				atributes = atr_copy(line_list)
				# almacenamos una copia de los atributos en una variable global
			elif valid_line(line_list) :
				aux_elements = []				
				for e in line_list:
					aux_elements.append(int(e))
				ret_instances.append(aux_elements)
			else:
				print "Error en la linea " + str(line_number)
			line_number+=1
	return ret_instances

#INICIALIZAR DISTANCIAS MINIMAS
# inicializamos el diccionario con el valor maximo de los float
def init_dist_min(n_inst):
	dist_mins = {}
	for n in range(n_inst):
		dist_mins[n]=sys.float_info.max
	#print dist_mins
	return dist_mins


#DISTANCIA
def distancia(instancia_a, instancia_b):
	if len(instancia_a)==len(instancia_b):
		if distancia_tipo == 'EUCLIDEA':
			dist = 0
			for a in range(len(atributes)):
				dist += (instancia_a[a]-instancia_b[a]) * (instancia_a[a]-instancia_b[a])
			dist = math.sqrt(dist)
			return dist
	else:
		print 'INSTANCIAS CON DIMENSIONES ERRONEAS'
		return -1

#CENTROIDES ALEJADOS
# el algoritmo de obtener los centroides mas alejados
def cent_alejados(k, instancias):
	# centoide inicial es el 0
	centroides_index = [0]

	# todas las distancias minimas son el maximo double
	distancias_minimas = init_dist_min(len(instancias))

	# recorremos la lista de centroides para buscar la instancia cuya minima distancia sea maxima
	while len(centroides_index)<k:
		#print distancias_minimas
		#print '+++++++++++'
		distancia_maxima = -1
		indice_maximo = -1
		for i in distancias_minimas.keys():
			dist = distancia(instancias[i],instancias[centroides_index[len(centroides_index)-1]])
			#print 'distancia :- ' + str(i) + ' a '+ str(centroides_index[len(centroides_index)-1]) + ' ' + str(dist)
			if dist<distancias_minimas[i]:
#				print 'sustituimos '+ str(i)
				distancias_minimas[i]=dist
			if distancias_minimas[i]>distancia_maxima:
				distancia_maxima = distancias_minimas[i]
				indice_maximo = i
		centroides_index.append(indice_maximo)
#		print '#####################################'
#
#	print distancias_minimas
#	print centroides_index
	centroides = []
	for c in centroides_index:
		centroides.append(instancias[c])
	return centroides


#VERIFICA QUE LOS CENTROIDES TENGAN N ATRIBUTOS
# al insertar centroides a mano hay que verificarlos
# son correctos si tienen el numero adecuado de atributos
def centroides_correctos (k, centroides_ini):
	ret_val = k == len(centroides_ini)
	for c in centroides_ini:
		ret_val = ret_val and len(c)==len(atributes)
	print 'Los centroides correctos = ' + str(ret_val)
	return ret_val

# CLUSTERING BUILD
def clustering_build(instancias,centroides_aux):
	ret_cluster = {}
	for n in range(len(centroides_aux)):
		ret_cluster[n]=[]

	#recorro las instancias
	for i in instancias:
		#para cada instancia debo estudiar la distancia a cada centroide
		dist_min = sys.float_info.max
		centroide_cercano = -1

		for c in range(len(centroides_aux)):
			dist = distancia(i,centroides_aux[c])
			if dist<dist_min:
				dist_min = dist
				centroide_cercano = c

		# una vez determinado el centroide mas cercano
		ret_cluster[centroide_cercano].append(i)

	return ret_cluster

# MEDIA CENTROIDE
# de una lista de instancias calculamos un centroide con valores medios
def media_centroide(lista_instancias):
	#teniendo una lista de instancias calculamos la instancia -media-
	ret_media = copy.deepcopy(lista_instancias[0])

	# usamos el rango para poder referirnos mejor a las instancias de las listas, y para preservar el orden
	for i in range(1,len(lista_instancias)):
		#print lista_instancias[i]
		for a in range(len(ret_media)):
			# cada campo de la instancia se suma con su homonimo de la otra
			ret_media[a] += lista_instancias[i][a] 
	for b in range(len(ret_media)):
		#para obtener la media dividimos entre el numero de instancias sumadas
		ret_media[b] /= len(lista_instancias)  

	return ret_media


# ACTUALIZA CENTROIDES
# construimos una lista de centroides a partir del estado actual del clustering
def actualiza_centroides(clustering_aux):
	ret_centroids = []
	for c in range(len(clustering_aux.keys())):
		ret_centroids.append(media_centroide(clustering_aux[c]))
	return ret_centroids

# ACTUALIZA CONJUNTOS
# la idea es reagrupar las instancias segun que centroide le pille mas cerca
# si alguna cambia de grupo hay que transmitirlo en la variable next_iteration
def actualiza_conjuntos(clustering_aux, centroides_aux):
	next_iteration = False

	new_clustering = {}
	for n in range(len(centroides_aux)):
		new_clustering[n]=[]

	for centroide in clustering_aux.keys():
#		print 'centroide actual + ' + str(centroides_aux[centroide])
		for instancia in clustering_aux[centroide]:
#			print instancia
			dist_min = distancia(instancia, centroides_aux[centroide])
#			print 'distancia actual - ' +str(dist_min)
			cent = -1 # variable para almacenar el posible nuevo conjunto al que desplazar la instania si toca
			for k in range(len(centroides_aux)): # contrastamos la distancia de la instancia con los centroides
				dist = distancia(instancia, centroides_aux[k])
#				print 'distancia con el centroide ' + str(k) + ' :::: ' + str(dist)
				if(dist < dist_min): # l instancia puede ir a otro conjunto con un centroide mas cercano
					cent = k # recordamos el posible nuevo centroide al que llevar la instancia
					dist_min = dist
			if cent != -1 : # toca cambiar la instancia de conjunto
				new_clustering[cent].append(instancia)
				next_iteration = True
				#print 'soy la instancia '+ str(instancia) + ' y ME ESTOY MOVIENDO!!!'
			else: # cent == -1 - significa que no ha habido ninguna distancia menor con ningun otro centroide de otro conjunto
				new_clustering[centroide].append(instancia)
				#print 'soy la instancia '+ str(instancia) + ' y NO ME MUEVO!'


	return (new_clustering,next_iteration)


#ALGORITMO DE KMEANS
# contiene el bucle que recoloca los centroides y los conjuntos hasta que no se producen cambios
def kmeans_core(k,instancias, centroides_ini):
	next_iteration = True

	#estructura auxiliar de centroides
	centroides_aux = copy.deepcopy(centroides_ini)

	# diccionario {conjunto : instancias }
	clustering_aux = clustering_build(instancias,centroides_aux)


	# variable de contar iteraciones
	iter_counter = 0
	# iteracion del algoritmo
	while next_iteration :
		# primero actualizamos el valor de los centroides
		centroides_aux = actualiza_centroides(clustering_aux)
		# con los nuevos valores de los centroides reestructuramos los clusters y evaluamos si hay que repetir la tarea
		(clustering_aux,next_iteration) = actualiza_conjuntos(clustering_aux, centroides_aux)
		# llevamos un control de las iteraciones que hacemos
		iter_counter += 1

	print iter_counter
	# arreglo de la salida
	return clustering_aux,centroides_aux

#KMEANS
def kmeans(k, instancias, centroides_ini=None):
	salida = (None,None)
	if k > len(instancias):
		print 'EL NUMERO DE CENTROIDES SUGERIDO ES MAYOR AL NUMERO DE INSTANCIAS'
	elif k == len(instancias):
		print 'HAY TANTOS CENTROIDES COMO INSTANCIAS'
	elif centroides_ini!=None and not centroides_correctos(k,centroides_ini):
		print 'FALLAN LOS CENTROIDES INICIALES'
	else:
		if centroides_ini==None:
			print 'CONSTRUIMOS CENTROIDES INICIALES'
			centroides_ini = cent_alejados(k, instancias)
		salida = kmeans_core(k, instancias, centroides_ini)
		print len(salida)
	return salida
			

# CENTROIDES IN
# funcion para distinguir los centroides iniciales a partir de lo que introduzca el usuario
def centroides_in(cent_str):

	# Aqui la idea es dividir la cadena que tiene la forma
	# '[[3366,5403,12974,4400,5977,1744],[112151,29627,18148,16745,4948,8550],[7588,1897,5234,417,2208,254]]'
	# en una asi
	# ['3366,5403,12974,4400,5977,1744', '112151,29627,18148,16745,4948,8550', '7588,1897,5234,417,2208,254']
	# que podamos convertir en una lista de centroides asi
	# [[3366,5403,12974,4400,5977,1744],[112151,29627,18148,16745,4948,8550],[7588,1897,5234,417,2208,254]]

	cent_lst = re.split('\[\[|\],\[|\]\]',cent_str)[1:-1]  # de esta forma ignoramos las dos cadenas vacias que se quedan a los extremos
	centroides_lst = []
	for c in cent_lst:
		centroide = []
		centroide_lst = c.split(',')
		for a in centroide_lst:
			centroide.append(int(a))
		centroides_lst.append(centroide)

	return centroides_lst


#MAIN
# contamos el numero de argumentos de entrada para poder determinar las opciones de ejecucion

n_argumentos = len(argv)
if n_argumentos==3 or n_argumentos==4:

	#VARIABLES GLOBALES
	atributes = []

	distancia_tipo = 'EUCLIDEA'

	

	if n_argumentos == 3:
		script, datafile, k_str = argv
		k_var = int(k_str)
		instances = read_file(datafile)
		conjuntos,centroides = kmeans(k_var,instances)
	elif n_argumentos == 4:
		script, datafile, k_str, cent_str = argv
		centroides_iniciales = centroides_in(cent_str)
		if centroides_iniciales == None:
			print 'FALLO EN CENTROIDES INICIALES'
		k_var = int(k_str)
		instances = read_file(datafile)
		conjuntos,centroides = kmeans(k_var,instances, centroides_iniciales)

	print 'conjuntos'
	print len(conjuntos)
	print '+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-'
	print '+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-'
	print '+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-'
	print '+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-'
	print 'centroides'
	print centroides


	#############
	#############
	#############
	#
	# COHESION
	#

else:
	print 'Necesitas 3 o 4 argumentos'


# EJEMPLO

# python k_means.py customers.csv 3
#
# DA 18 ITERACIONES HASTA QUE SE DETIENE

# python k_means.py customers.csv 3 [[3366,5403,12974,4400,5977,1744],[112151,29627,18148,16745,4948,8550],[7588,1897,5234,417,2208,254]]
#
# DA 10 ITERACIONES HASTA QUE SE DETIENE