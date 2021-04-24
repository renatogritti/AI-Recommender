# Import Libraries

import pandas as pd
from math import sqrt

# load Database Function to memory
from loaddb import *

# Setup logging
import logging
logging.basicConfig(filename='euclid.log', level= logging.ERROR)

# Carregar Bases de dados
basepeople = loaddatabase('people')
baseitem = loaddatabase('item')


##################################################################
# Euclidian distance
##################################################################
def euclidiana(base, usuario1, usuario2):
	si = {}
	for item in base[usuario1]:
		if item in base[usuario2]: si[item] = 1

	if len(si) == 0: return 0

	soma = sum([pow(base[usuario1][item] - base[usuario2][item], 2)
		for item in base[usuario1] if item in base[usuario2]])
	return 1/(1 + sqrt(soma))

##################################################################
# Get Similar (People or Items)
##################################################################
def getSimilares(base, usuario):
	similaridade = [(euclidiana(base, usuario, outro), outro)
					for outro in base if outro != usuario]
	similaridade.sort()
	similaridade.reverse()
	return similaridade[0:30]
	
##################################################################
# Get Recommendation by People
##################################################################
def getRecomendacoesUsuario(base, usuario):
	totais={}
	somaSimilaridade={}
	for outro in base:
		if outro == usuario: continue
		similaridade = euclidiana(base, usuario, outro)

		if similaridade <= 0: continue

		for item in base[outro]:
			if item not in base[usuario]:
				totais.setdefault(item, 0)
				totais[item] += base[outro][item] * similaridade
				somaSimilaridade.setdefault(item, 0)
				somaSimilaridade[item] += similaridade
	rankings=[(total / somaSimilaridade[item], item) for item, total in totais.items()]
	rankings.sort()
	rankings.reverse()
	return rankings[0:30]
         

##################################################################
# For BATH include in Cache
##################################################################
def calculaItensSimilares(base):
	result = {}
	for item in base:
		notas = getSimilares(base, item)
		result[item] = notas
	return result

##################################################################
# Get Recommendation by Items
##################################################################
def getRecomendacoesItens(baseUsuario, similaridadeItens, usuario):
	notasUsuario = baseUsuario[usuario]
	notas={}
	totalSimilaridade={}
	for (item, nota) in notasUsuario.items():
		for (similaridade, item2) in similaridadeItens[item]:
			if item2 in notasUsuario: continue
			notas.setdefault(item2, 0)
			notas[item2] += similaridade * nota
			totalSimilaridade.setdefault(item2,0)
			totalSimilaridade[item2] += similaridade
	rankings=[(score/totalSimilaridade[item], item) for item, score in notas.items()]
	rankings.sort()
	rankings.reverse()
	return rankings
	

