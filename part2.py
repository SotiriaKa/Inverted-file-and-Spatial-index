#Sotiria Kastana, 2995

import sys
import time
import csv
import heapq
from heapq import merge

query_range = sys.argv	

sort_x = []																				#listes pou tha apothikevoun tis taksinomhmenes syntetagmenes
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

with open('Restaurants_London_England.tsv') as tsvfile:
	restaurants = list(tsvfile)

def spaSearchGrid(qr):
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
	global dim_y
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
	for i in range(0,dim_x):
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
	# for i in range (0,dim_x):
		# if min_x_qr > list_x[i][0] and min_x_qr<=list_x[i][1]:
			# first_x = i
		# if max_x_qr > list_x[i][0] and max_x_qr<=list_x[i][1]:
			# last_x = i
	# for j in range (0,dim_y):
		# if min_y_qr > list_y[j][0] and min_y_qr<=list_y[j][1]:
			# first_y = j
		# if max_y_qr > list_y[j][0] and max_y_qr<=list_y[j][1]:
			# last_y = j		
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
							list_rests.append(restaurants[lgrid])
					else:
						list_rests.append(restaurants[lgrid])
	return list_rests	

def spaSearchRaw(qr):
	global restaurants
	minx = float(qr[1])
	maxx = float(qr[2])
	miny = float(qr[3])
	maxy = float(qr[4])
	list_rests = []
	for rest in restaurants:
		loc = rest.split('\t')[1]
		location = loc[10:len(loc)]														#gt dn theloume na exei to 'location: '
		restx = float(location.split(',')[0])
		resty = float(location.split(',')[1])
		if restx <= maxx and restx >= minx and resty <=maxy and resty >= miny:
			list_rests.append(rest)
	return list_rests
	
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
list_x = []
list_y = []
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
cr = 0																					#metritis grammwn/ kathe estiatorio se poia grammi einai
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
	
print('bounds: '+str(min_x)+' '+str(max_x)+' '+str(min_y)+' '+str(max_y))
print('widths: '+str(range_x)+' '+str(range_y))
for x in range(0,dim_x):
	for y in range(0,dim_y):
		if grid[x][y] != []:
				print(str(x)+' '+str(y)+' '+str(len(grid[x][y])))
				
list_Raw = []
Raw_time_start = time.time()
list_Raw = spaSearchRaw(query_range)
Raw_time= time.time() - Raw_time_start
print('spaSearchRaw: '+str(len(list_Raw))+' results, cost = '+str(Raw_time)+' seconds')
for lr in list_Raw:
	print(lr)
print('______________________________________________________________________')
list_Grid = []
Grid_time_start = time.time()
list_Grid = spaSearchGrid(query_range)
Grid_time= time.time() - Grid_time_start
print('spaSearchGrid: '+str(len(list_Grid))+' results, cost = '+str(Grid_time)+' seconds')
for lg in list_Grid:
	print(lg)