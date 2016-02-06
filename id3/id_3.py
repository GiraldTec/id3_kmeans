import sys
import math
import re
import copy
from sys import argv


#INSERT ATRIBUTE
# si una categoria de un atributo no existe en el diccionario la insertamos
def insert_atribute(lista, diccionario):
	atributes_sets = []
	# es una lista de tuplas (atributo, set sin repeticion de valores )
	for a in diccionario.keys():
		atributes_sets.append((a,set(diccionario[a][1])))
	for i in range(len(lista)):
		if not lista[i] in atributes_sets[i][1]:
			#print 'EL VALOR DEL ATRIBUTO NO ESTA EN EL DICCIONARIO'
			diccionario[atributes_sets[i][0]][1].append(lista[i])



# INSERT CLASS
def insert_class(clase, lista):
	set_clases = set(lista)
	if not clase in set_clases:
		#print 'EL VALOR DE LA CLASE NO ESTA EN LA LISTA'
		lista.append(clase)

#READ FILE DEL EJERCICIO
def read_file(filename):
	atributes_dict = {}
	line_number = 0
	atr_number = 0
	instances = []
	clases = []
	with open(filename,'r') as file_obj:
		for line in file_obj:
			line_list = line[:-1].split(',')
			if line_number==0 :
				for atr_index in range(len(line_list)-1):
					atributes_dict[line_list[atr_index]] = (atr_index,[])
				atr_number = len(line_list)
				#print atributes_dict
			elif len(line_list)==atr_number :
				insert_atribute(line_list[:-1], atributes_dict)
				insert_class(line_list[len(line_list)-1], clases)
				instances.append(copy.deepcopy(line_list))
			else:
				print "Error en la linea " + str(line_number)
			line_number+=1
	return (instances,atributes_dict,clases)

# POPULAR
# para determinar la clase popular de un conjunto de instancias
def popular(instancias):
	aux_dict = {}
	for i in instancias:
		clase = i[len(i)-1]
		if clase in aux_dict.keys():
			aux_dict[clase] += 1
		else:
			aux_dict[clase] = 1

	popularidad = -1
	popular = ''
	for c in aux_dict.keys():
		if aux_dict[c]>popularidad:
			popular = c
			popularidad = aux_dict[c]

	return popular

# SAME CLASS
# funcion para determinar que las instancias de un conjunto comparten clase
def same_class(instancias):
	clase_cero = instancias[0][len(instancias[0])-1]
	indice = 1
	misma_clase = True
	while misma_clase and indice<len(instancias):
		if instancias[indice][len(instancias[indice])-1] != clase_cero:
			misma_clase = False
		else:
			indice += 1
	return misma_clase

# ENTROPIA
# funcion para calcular la entropia de un conjunto de instancias
def entropia(lista):
	if lista == []:
		return 0.0

	clases_dict = {}
	num_instancias = len(lista)
	for i in lista:
		clase = i[len(i)-1]
		if not clase in clases_dict.keys():
			clases_dict[clase] = 1
		else:
			clases_dict[clase] += 1

	ret_entropia = 0
	# implementamos el sumatorio que nos calcula la entropia con la formula
	# sum[1..k]( Si/N * log_2( Si/N ) )
	for c in clases_dict.keys():
		veces_clase = clases_dict[c]
		si_entre_N = float(veces_clase) / float(num_instancias)
		ret_entropia += -( si_entre_N * math.log( si_entre_N, 2))
	return ret_entropia

# ENTROPIA PARTICIONADO
# funcion que nos ayuda a obtener una particion del conjunto de instancias a partir de un atributo especifico
# devuelve:
# - entropia media de la particion
# - particion en una lista de tuplas ( valor_del_atributo, lista de instancias )
def entropia_particionado(instancias, pos_cand):
	print '+++++particioonadoo++++'
	print instancias
	print pos_cand
	aux_particiones = {}
	# es un diccionario con la forma { valor_del_atributo : [particion de instancias]}
	num_instancias = float(len(instancias))

	for i in instancias:
		print i
		print pos_cand
		atrib_valor = i[pos_cand]
		if not atrib_valor in aux_particiones.keys():
			aux_particiones[atrib_valor] = [i]
		else:
			aux_particiones[atrib_valor].append(i)

	ret_entropia = 0.0
	ret_tuplas = []
	ret_particiones = []
	
	for p in aux_particiones.keys():
		entropia_part = entropia(aux_particiones[p])
		ret_entropia += len(aux_particiones[p])/num_instancias * entropia_part
		ret_tuplas.append((p,aux_particiones[p]))

	print 'devolvemos las tuplas: '
	print ''
	print ''
	print ret_tuplas
	print ''
	print ''

	return ret_entropia, ret_tuplas


# QUITAR DE LA LISTA
# es una tarea de eliminar el candidato de la lista de candidatos
def quitar_de_lista(candidato, lista):
	ret_lista = []
	for c in lista:
		if c!=candidato:
			ret_lista.append(c)
	return ret_lista



# SELECCIONA ATRIBUTO
# HACEMOS LOS CALCULOS DE LA ENTROPIA Y DEVOLVEMOS EL ATRIBUTO QUE MEJOR SESGUE EL CONJUNTO
def selecciona_atributo(instancias, candidatos, atrib_dict):
	print 'seleccionemos atributo'
	print instancias
	ret_atributo = ''
	ret_particiones = []
	entropia_ini = entropia(instancias)
	ganancia_max = 0.0

	for c in candidatos:
		posicion_cand = atrib_dict[c][0]
		print 'mi lista de instancias '+ str(instancias)
		entropia_part , particiones_aux = entropia_particionado(instancias, posicion_cand)
		print particiones_aux
		print 'entropia ini = '+ str(entropia_ini)
		print 'entropia part = '+ str(entropia_part)

		ganancia_info  = entropia_ini - entropia_part
		print ganancia_info
		if ganancia_info > ganancia_max:
			ganancia_max = ganancia_info
			ret_atributo = c
			print str(ret_atributo) + ' es el atributo seleccionado!'
			print particiones_aux
			ret_particiones = particiones_aux

	# finalmente eliminamos el candidato que nos ramifica el arbol
	ret_candidatos = quitar_de_lista(ret_atributo, candidatos)

	return ret_atributo, ret_candidatos, ret_particiones

# ARBOL === ( _atributo_ , [ (_valor1_, ARBOL), (_valor2_, ARBOL), ... ] )
# ARBOL === [ _clase_ ]
# Esa es la estructura que emplearemos


# ID3
def id3(instancias, atrib_dict, clases, candidatos):

	popular_class = popular(instancias)


	if same_class(instancias):
		# devolvemos la clase de la primera instancia
		return instancias[0][ len(instancias[0])-1 ] 

	if candidatos == []:
		return popular_class

	# la funcion selecciona_atributo nos devuelve
	# - El nombre del atributo elegido
	# - La nueva lista de candidatos
	# - Una lista con los subconjuntos de instancias en forma [ ( atrib_valor , [sublista] ) , ... ]
	(atributo_name,new_candidatos, particiones) = selecciona_atributo(instancias,candidatos, atrib_dict)
	print 'Hemos generado las particiones con el atributo : ' + atributo_name
	print particiones
	print '+++++++++++'
	print '+++++++++++'
	hijos = []
	for par in particiones:
		atrib_valor, sublista = par
		if sublista == []:
			hijos.append( [atrib_valor, (popular_class) ] )
		else:
			print 'esto es recursividad'
			print ' esto es una sublista : ' + str(sublista)
			print '--------------------'
			print '--------------------'
			hijos.append( [atrib_valor, id3(sublista,atrib_dict,clases,new_candidatos) ] )
	return (atributo_name,hijos)

# CUENTA
def cuenta(dict, valor):
	if not valor in dict.keys():
		dict[valor] = 1
	else:
		dict[valor] += 1

	return dict, dict[valor]


# DOT RECURSIVO
# funcion recursiva que recorre los arboles y devuelve una lista de nodos y una lista de aristas
def dot_recursivo(arbol, dict_contador):
	# empleamos un diccionario que nos ayude a contar el numero de nodos distintos que hay con una misma etiqueta
	print 'ARBOL DE TIPO'
	print type(arbol)
	if type(arbol) is tuple :
		# se trata de un nodo con hijos
		nodo = arbol[0]
		dict_contador, veces_nodo = cuenta(dict_contador, nodo)
		lista_hijos = arbol[1]
		ret_nodos = [('nodo', nodo, veces_nodo)] # los nodos son tuplas del estilo ('clase',valor, numero) ('nodo', valor, numero)
		ret_aristas = [] # las aristas son tuplas (padre, hijo, valor_atributo)
		# la lista de hijos es:
		# [ [valor1_atributo, hijo1], [valor2_atributo, hijo2], ... ]
		for hijo in lista_hijos:
			valor_hijo, arbol_hijo = hijo
			nodos_hijo, aristas_hijo, dict_contador = dot_recursivo(arbol_hijo, dict_contador)
			nodo_hijo = nodos_hijo[0]
			if aristas_hijo == []:
			# en caso de que el arbol hijo sea un nodo hoja sin aristas
				ret_nodos.append(nodo_hijo)
				ret_aristas.append((nodo+str(veces_nodo), nodo_hijo[1]+str(nodo_hijo[2]), valor_hijo))

			else:
			# en caso de que el hijo sea un nodo interior
				ret_nodos += nodos_hijo
				ret_aristas.append((nodo+str(veces_nodo), nodo_hijo[1]+str(nodo_hijo[2]), valor_hijo))
				ret_aristas += aristas_hijo

		return ret_nodos,ret_aristas, dict_contador
		
	elif type(arbol) is str :
		# se trata de un nodo hoja
		dict_contador, veces_nodo = cuenta(dict_contador, arbol)

		return ([('clase',arbol, veces_nodo)],[], dict_contador)

	else:
		print 'Hay algo mal en el arbol'
		print arbol
# DOT
# recorremos la estructura del arbol para obtener de esa forma el equivalente en formato DOT
def dot(arbol):

	lista_nodos, lista_aristas, dict_contador = dot_recursivo(arbol, {})

	print lista_nodos
	print '++++++++++++'
	print '++++++++++++'
	print '++++++++++++'
	print lista_aristas

	nombre_out = 'salida.txt'
	file_out = open(nombre_out, 'w')

	file_out.write('digraph salida {\n')

	# escribimos en el fichero de salida los nodos
	for nodo in lista_nodos:
		if nodo[0]=='nodo':
			file_out.write(nodo[1]+str(nodo[2])+' [label="'+nodo[1].upper()+'",shape="box"];\n')
		elif nodo[0]=='clase':
			file_out.write(nodo[1]+str(nodo[2])+' [label="'+nodo[1].upper()+'"];\n')

	# escribimos en el fichero las aristas
	for arista in lista_aristas:
		file_out.write(arista[0]+' -> '+arista[1]+' [label="'+arista[2]+'"];\n')

	file_out.write('}\n')
	file_out.close()

# MAIN
# contamos el numero de argumentos de entrada para poder determinar las opciones de ejecucion
n_argumentos = len(argv)
if n_argumentos==2:

	script, datafile = argv
	instancias, diccionario, clases = read_file(datafile)

	arbol_clasif = id3(instancias, diccionario, clases,diccionario.keys())

	print '################'
	print arbol_clasif


	formato_dot = dot(arbol_clasif)