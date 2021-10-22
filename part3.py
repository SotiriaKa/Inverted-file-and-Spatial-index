#Sotiria Kastana, 2995

import sys
import time
import csv
import heapq
from heapq import merge

queries = sys.argv
query_range = queries[0:5]
query_tags = queries[5:len(queries)]

with open('Restaurants_London_England.tsv') as tsvfile:
	restaurants = list(tsvfile)
	
inverted = dict()
tags = ''
frequencies = []
sort_x = []	
sort_y = []
#arxikopoihsh 2d-array grid
dim_x, dim_y = 50, 50
grid = [[0 for x in range(dim_x)] for y in range(dim_y)] 
min_x = 0.0
max_x = 0.0
min_y = 0.0
max_y = 0.0
rx = 0.0
ry = 0.0
list_x = []
list_y = []

file = open('inverted_file.txt', 'w') 
file.write('tags:	list\n') 

def kwSpaSearchIF(qr,qk):
	minx = float(qr[1])
	maxx = float(qr[2])
	miny = float(qr[3])
	maxy = float(qr[4])	
	global inverted
	i = 0
	lentags = 0
	counter_tags = 0
	result_lines = []		
	list_if = []
	for i in range(0,len(qk)):
		if 	qk[i] in inverted:
			lines = inverted.get(qk[i])									
			result_lines = list(merge(lines, result_lines))				
	counter_similar = 1 												
	if len(qk) == 1:
		for j in range(0,len(result_lines)):
			loc = restaurants[result_lines[j]].split('\t')[1]
			location = loc[10:len(loc)]								
			restx = float(location.split(',')[0])
			resty = float(location.split(',')[1])
			if restx <= maxx and restx >= minx and resty <=maxy and resty >= miny:		
				list_if.append(restaurants[result_lines[j]])
	else:
		for j in range(1,len(result_lines)):
			if result_lines[j] == result_lines[j-1]:
				counter_similar += 1
				if counter_similar == len(qk):
					loc = restaurants[result_lines[j]].split('\t')[1]
					location = loc[10:len(loc)]								
					restx = float(location.split(',')[0])
					resty = float(location.split(',')[1])
					if restx <= maxx and restx >= minx and resty <=maxy and resty >= miny:		
						list_if.append(restaurants[result_lines[j]])
			else:
				counter_similar = 1											
	return list_if

def kwSpaSearchGrid(qr,qk):
	global restaurants
	global grid 
	global min_x 
	global max_x 
	global min_y 
	global max_y 
	global rx 
	global ry 
	global list_x
	global list_y
	global dim_x
	min_x_qr = float(qr[1])
	max_x_qr = float(qr[2])
	min_y_qr = float(qr[3])
	max_y_qr = float(qr[4])
	list_rests = []	
	list_grid = []
	first_x = 0
	last_x = 0
	first_y = 0
	last_y = 0	
	bool1 = 0
	bool2 = 0
	for i in range(0,dim_x):														#eite dim_x eite dim_y ine to idio 
		grid_min_x = rx*i+min_x		
		grid_max_x = grid_min_x + rx
		grid_min_y = ry*i+min_y
		grid_max_y = grid_min_y + ry
		if min_x_qr > grid_min_x and min_x_qr<=grid_max_x:
			first_x = i
		if max_x_qr > grid_min_x and max_x_qr<=grid_max_x:
			last_x = i
		if min_y_qr > grid_min_y and min_y_qr<=grid_max_y:
			first_y = i
		if max_y_qr > grid_min_y and max_y_qr<=grid_max_y:
			last_y = i			
	for x in range(first_x,last_x+1):
		for y in range(first_y,last_y+1):
			list_grid = []				
			list_grid = grid[x][y]
			if grid[x][y] != []:
				for lgrid in list_grid:
					if x== first_x or x == last_x or y == first_y or y == last_y:
						loc = restaurants[lgrid].split('\t')[1]
						location = loc[10:len(loc)]	
						restx = float(location.split(',')[0])
						resty = float(location.split(',')[1])
						if restx <= max_x_qr and restx >= min_x_qr and resty <=max_y_qr and resty >= min_y_qr:
							bool1 = 1
						else:
							bool1 = 0
						bool2 = 0
					else:
						bool2 = 1
					if bool1 == 1 or bool2 ==1:						
						counter_kw = 0
						for lqt in qk:
							tags = restaurants[lgrid].split('\t')[2]								
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
									counter_kw += 1
									break; 
						if counter_kw == len(qk):
							list_rests.append(restaurants[lgrid])
	return list_rests

def kwSpaSearchRaw(qr,qk):
	global restaurants
	list_raw = []
	minx = float(qr[1])
	maxx = float(qr[2])
	miny = float(qr[3])
	maxy = float(qr[4])
	for r in restaurants:
		counter_lqts = 0 																			#metritis pou tha metraei ta tag pou emfanistikan se kathe grammi
		tags = r.split('\t')[2]
		loc = r.split('\t')[1]
		location = loc[10:len(loc)]	
		restx = float(location.split(',')[0])
		resty = float(location.split(',')[1])
		for lqt in qk:
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
					break; 
		if counter_lqts == len(qk) and restx <= maxx and restx >= minx and resty <=maxy and resty >= miny:
			list_raw.append(r) 
	return list_raw

#dhmiourgia anestrammenou arxeiou
rest_line = 0
for rest in restaurants:
	tags = rest.split('\t')[2]
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
#dhmiourgia taksinomhmenwn listwn x k y
for rest in restaurants:
	loc = rest.split('\t')[1]
	location = loc[10:len(loc)]	
	sort_x.append(float(location.split(',')[0]))
	sort_y.append(float(location.split(',')[1]))
sort_x.sort()
sort_y.sort()
#dhmiourgia max,min x,y tou grid
min_x = sort_x[0]
max_x = sort_x[len(sort_x)-1]
min_y = sort_y[0]
max_y = sort_y[len(sort_y)-1]
#dhmiourgia 50 iswn megethwn se kathe diastasi
range_x = max_x-min_x
range_y = max_y-min_y
rx = range_x/50
ry = range_y/50
#dhmiourgia listwn ya x kai y opou kathe thesi exei to evros kathe diasthmatos ya ta 50 isoskelh megethi
lrx = min_x
rrx = min_x + rx
lry = min_y
rry = min_y + ry
for i in range(0,50):
	list_x.append([lrx, rrx])
	lrx = rrx	#left x
	rrx += rx 	#right x
	list_y.append([lry, rry])
	lry = rry	#left y
	rry += ry 	#right y
#dhmiourgia 2d-array grid
cr = 0
for i in range(0,dim_x):
	for j in range(0,dim_y):
		grid[i][j] = []
for rest in restaurants:
	loc = rest.split('\t')[1]
	location = loc[10:len(loc)]
	rest_x = float(location.split(',')[0])		
	rest_y = float(location.split(',')[1])
	for x in range(0,50):
		if rest_x >= list_x[x][0] and rest_x <= list_x[x][1]:
			break;
	for y in range(0,50):
		if rest_y >= list_y[y][0] and rest_y <= list_y[y][1]:
			break;
	grid[x][y].append(cr)
	cr += 1	
				
time_Raw_start = time.time()
l_query_tags = []
lenqueytags = 0
j=0
while lenqueytags<len(query_tags):
	q_tag = query_tags[j]
	if q_tag[0] == "'":
		j += 1
		if query_tags[j][len(query_tags[j])-1] == "'":	
			q_tag = q_tag[1:len(q_tag)] 	
			q_tag2 = query_tags[j]
			q_tag2 = q_tag2[0:(len(q_tag2)-1)] 			
			q_tag += ' '
			q_tag += q_tag2
			lenqueytags += 1
		else:
			while (query_tags[j][len(query_tags[j])-1] != "'"):
				q_tag2 = query_tags[j]
				q_tag += ' '
				q_tag += q_tag2
				lenqueytags += 1
				j += 1
			q_tag = q_tag[1:len(q_tag)] 	
			q_tag2 = query_tags[j]
			q_tag2 = q_tag2[0:(len(q_tag2)-1)] 			
			q_tag += ' '
			q_tag += q_tag2
			lenqueytags += 1	
	l_query_tags.append(q_tag)
	lenqueytags += 1 
	j+=1
l_Raw = [] 	
l_Raw = kwSpaSearchRaw(query_range,l_query_tags)
time_Raw = time.time()-time_Raw_start
print('kwSpaSearchRaw: '+str(len(l_Raw))+' results, cost = '+str(time_Raw)+' seconds'+'\n')
for lr in range(0,len(l_Raw)): 
	print(l_Raw[lr])
print('______________________________________________________________________')
time_IF_start = time.time()
l_IF = []
l_IF = kwSpaSearchIF(query_range,l_query_tags)
time_IF = time.time()-time_IF_start
print('kwSpaSearchIF: '+str(len(l_IF))+' results, cost = '+str(time_IF)+' seconds'+'\n')
for ifs in range(0,len(l_IF)): 
	print(l_IF[ifs])
print('______________________________________________________________________')	
list_Grid = []
Grid_time_start = time.time()
list_Grid = kwSpaSearchGrid(query_range,l_query_tags)
Grid_time= time.time() - Grid_time_start
print('kwSpaSearchGrid: '+str(len(list_Grid))+' results, cost = '+str(Grid_time)+' seconds')
for lg in list_Grid:
	print(lg)