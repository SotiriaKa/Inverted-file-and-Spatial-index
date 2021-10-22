#Sotiria Kastana, 2995

import sys
import time
import csv
import heapq
from heapq import merge

query_tags = sys.argv

with open('Restaurants_London_England.tsv') as tsvfile:
	restaurants = list(tsvfile)

inverted = dict()
tags = ''
frequencies = []
file = open('inverted_file.txt', 'w') 
file.write('tags:	list\n') 
	
def kwSearchIF(list_query_tags):
	global inverted
	result_lines = []																	#lista se afksousa seira pou tha kratithoun oles oi listes
	list_if = []
	for lqt in list_query_tags:
		if 	lqt in inverted:
			lines = inverted.get(lqt)													#h lista pou exei parei kathe fora apo to leksiko
			result_lines = list(merge(lines, result_lines))								#kathe fora kanei merge to apotelesma me tin nea lista
	counter_similar = 1																	#ksekinaei apo 1 giati thewreite oti exei hdh mia eggrafh
	if len(list_query_tags) == 1:
		for j in range(0,len(result_lines)):
			list_if.append(restaurants[result_lines[j]])
	else:
		for j in range(1,len(result_lines)):											#ksekinaei apo 1 gt periexei hdh thn 1h eggrafi 
			if result_lines[j] == result_lines[j-1]:
				counter_similar += 1
				if counter_similar == len(list_query_tags):								
					list_if.append(restaurants[result_lines[j]])
			else:
				counter_similar = 1									
	return list_if

def kwSearchRaw(list_query_tags):
	global restaurants
	list_raw = []
	for r in restaurants:
		counter_lqts = 0 																#metritis pou tha metraei ta tags pou emfanistikan se kathe grammh
		tags = r.split('\t')[2]
		for lqt in list_query_tags:
			i = 0
			lentags = 5	
			while lentags<len(tags):
				tag = tags[6:len(tags)].split(',')[i]		
				if '\n' in tag :
					without_nl = len(tag)-1  
					tag = tag[0:without_nl] 
					lentags +=1 
				i +=1
				lentags += len(tag) + 1
				if lqt == tag:
					counter_lqts += 1
					break; 																#gt profanws an ena tag vrethei dn yparxei periptosi na ksanayparxei,opote pame sto epomeno
		if counter_lqts == len(list_query_tags):
			list_raw.append(r) 															#append giati simainei oti ola ta tags pou thelw periexonte sth grammh
	return list_raw

#dhmiourgia leksikou 
rest_line = 0
for rest in restaurants:
	tags = rest.split('\t')[2]
	i = 0
	lentags = 5 																		#ksekinaei apo 5 gt pairnei to 'tags:' pou vgazo parakatw
	while lentags<len(tags):
		tag = tags[6:len(tags)].split(',')[i]		
		if '\n' in tag :																#h periptosi poy ine i teleftaia etiketa tis eggrafis
			without_nl = len(tag)-1 													#to mikos tou tag xoris to newline, gia na min to emfanizei k afto
			tag = tag[0:without_nl] 													#to tag xoris to newline
			lentags +=1 																#+1 gia na metrisoume k ton xaraktira new line
		i +=1
		lentags += len(tag) + 1 														#+1 gt vazo kai to comma(,) pou i split to vgazei
		lines = []
		if tag in inverted:
			lines = inverted.get(tag)			
		lines.append(rest_line)
		inverted.update({tag : lines})		
	rest_line += 1
	
#dhmiourgia inverted arxeiou
for inv in inverted:
	frequencies.append(len(inverted.get(inv)))
	file.write(inv+': '+str(inverted.get(inv))+'\n')
	
frequencies.sort()
print('number of keywords: '+str(len(inverted)))
print('frequencies: '+str(frequencies)+'\n')

time_Raw_start = time.time()
l_query_tags = []
lenqueytags = 1 																		#ksekinaei apo ena gia to 1o orisma pou dn metraw pou ine to script	
j = 1 																					#gt dn thelo to script	
while lenqueytags<len(query_tags):
	q_tag = sys.argv[j]
	if q_tag[0] == "'":
		j += 1
		if sys.argv[j][len(sys.argv[j])-1] == "'":										#dld an i defteri leksi teleionei se ', px 'late night'
			q_tag = q_tag[1:len(q_tag)] 												#dld xoris to '
			q_tag2 = sys.argv[j]
			q_tag2 = q_tag2[0:(len(q_tag2)-1)] 											#dld xoris to '		
			q_tag += ' '
			q_tag += q_tag2
			lenqueytags += 1
		else:
			while (sys.argv[j][len(sys.argv[j])-1] != "'"):
				q_tag2 = sys.argv[j]
				q_tag += ' '
				q_tag += q_tag2
				lenqueytags += 1
				j += 1
																						#dld otan tha ftasei sti teleftea leksi, me to ' sto telos
			q_tag = q_tag[1:len(q_tag)] 												
			q_tag2 = sys.argv[j]
			q_tag2 = q_tag2[0:(len(q_tag2)-1)] 			
			q_tag += ' '
			q_tag += q_tag2
			lenqueytags += 1			
	l_query_tags.append(q_tag)	
	lenqueytags += 1 																	#prostheto ena ya kathe comma (,)
	j+=1	

l_Raw = [] 	
l_Raw = kwSearchRaw(l_query_tags)
time_Raw = time.time()-time_Raw_start
print('kwSearchRaw: '+str(len(l_Raw))+' results, cost = '+str(time_Raw)+' seconds'+'\n')
for lr in range(0,len(l_Raw)): 
	print(l_Raw[lr])
print('______________________________________________________________________')
time_IF_start = time.time()
l_IF = []
l_IF = kwSearchIF(l_query_tags)	
time_IF = time.time()-time_IF_start
print('kwSearchIF: '+str(len(l_IF))+' results, cost = '+str(time_IF)+' seconds'+'\n')
for ifs in range(0,len(l_IF)): 
	print(l_IF[ifs])