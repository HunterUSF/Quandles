##############################################################################
#
# Version 10
# Added removeTrivial function - removes any row with only zero as entries.
#
# TODO:
# 	Determine which elements are torsion
#	Determine distinct generators for cocycles
# DONE:
#	Determine distinct generators for coboundaries. 
#	They are independent after used rowReduce function.
#
##############################################################################

from numpy import *
from sympy import *
from math import sqrt
from quandlelist import *



def computeCoeff(triple, matrix):
	### Equation obtained from evaluating element of Z^2 in 2-cocycle equation
	n = len(matrix)
	current_eq = []
	p, q, r = triple[0], triple[1], triple[2]
	a, b, c, d  = (p, r), (matrix[p, r], matrix[q, r]), (p, q), (matrix[p, q], r)
	constants = [a,b,c,d]
	for x in range(n):
		for y in range(n):
				if (x,y) in constants:
					if ((x,y) == a or (x,y) == b) and ((x,y) == c or (x,y) == d):
						current_eq.append(0)
					elif ((x,y) == a or (x,y) == b):
						current_eq.append(1)
					elif ((x,y) == c or (x,y) == d):
						current_eq.append(-1)
				else:
					current_eq.append(0)
	#print triple
	#equation = []
	#for i in range(0, len(current_eq)):
	#	if current_eq[i] != 0:
	#		equation.append("%d(%d,%d)" % (current_eq[i] , (i / 4), (i % 4)))
	#print equation, '\n'
	return current_eq

def listRelations(M):
	### Lists n^3 equations obtained by evaluating triples in 2-cocycle equation
	n = len(M)
	list_of_equations = []
	for x in range(n):
		for y in range(n):
			for z in range(n):
				triple = (x,y,z)
				if (x == y) or (y == z):
					pass
				else:
					list_of_equations.append(computeCoeff(triple, M))
	return list_of_equations


def computeCoboundary(M, n):
	### Given Cayley tables, computes the delta(chi_n)
	length = len(M)
	coboundary_row = []
	for i in range(length):
		for j in range(length):
			cob = chi(i,n) - chi( M[i,j],n )
			coboundary_row.append(cob)
	return coboundary_row


def matrixCoboundaries(M):
	### Lists coboundary computations in a matrix
	length = len(M)
	coboundary_matrix = []
	for i in range(length):
		coboundary_matrix.append(computeCoboundary(M,i))
	return coboundary_matrix


def chi(m,n):
	### Characteristic functions mapping the quandle to an abelian group
	if m == n:
		return 1
	else:
		return 0


def zeroDoubles(M):
	### Sets all entries in columns corresponding to an ordered pair of the form (x, x) to the zero
	shape = M.shape
	pairs = int(sqrt(M.shape[1])) + 1
	for i in range(shape[0]):
		for j in range(0, shape[1], pairs):
			M[i, j] = 0
			M[i, j] = 0
			M[i, j] = 0


def rowReduce(array, mod_num=0):
	### Row reduces over a group - n is the coefficients it checks
	M = array.copy()
	rows = M.shape[0]
	cols = M.shape[1]
	done_list = set()
	z = 1
	repeat = True
	while repeat == True:
		max_index = argmax(M)
		max_entry = M[max_index / cols][max_index % cols]
		min_index = argmin(M)
		min_entry = M[min_index / cols][min_index % cols]
		if z > max_entry or (abs(min_entry)) > z:
			repeat = False
		for j in range(cols):
			for i in range(rows):
				if i not in done_list:
					if M[i][j] == -z:
						# print "M[{}][{}] == {}".format(i, j, -z)
						store = M[i]
						for k in range(i+1, rows):
							if M[k][j] == -z:
								M[k] = M[k] - store
							if M[k][j] == z:
								M[k] = M[k] + store
						done_list.add(i)
					if M[i][j] == z:
						# print "M[{}][{}] == {}".format(i, j, z)
						store = M[i]
						for k in range(i+1, rows):
							if M[k][j] == z:
								M[k] = M[k] - store
							if M[k][j] == -z:
								M[k] = M[k] + store
						done_list.add(i)
		
		z += 1
	return M

def removeTrivial(array):
	### Removes trivial rows. Necessary quandle is not connected. Returns numpy.ndarray.
	eqlist = []
	M = list(array.copy())
	rows = array.shape[0]
	for i in range(rows):
		for entry in M[i]:
			if entry != 0:
				eqlist.append(M[i])
				break
	return eqlist

def sortDiagonal(array):
	# Sorts a matrix to diagonal.
	templist = []
	row_len = array.shape[1]
	for row in array:
		for col in range(row_len):
			if row[col] != 0:
				templist.append((col, row))
				break

	sorted_temp = sorted(templist, key=lambda tup: tup[0])

	diag_list = []
	for tup in sorted_temp:
		diag_list.append(tup[1])
	return diag_list


#########
#########
M = C3_1	# Computations based on choice for M
mod_num = 3	# Determined the group coefficents are in. 0 implies Z

###
relations = array(listRelations(M))
print "The relations obtained by plugging in triples:"
zeroDoubles(relations)
print relations
print


# ###
# # Only necessary when quandle is not connected
# relations = array(removeTrivial(relations))
# print "(If not connected quandle) Removed trivial rows:"
# print relations
# print


###
# Removes duplicate rows
equations_copy = []
rows = relations.shape[0]
for i in range(rows):
	store = relations[i]
	append = True
	for j in range(i+1, rows):
		if array_equal(store,relations[j]) or array_equal(store,-relations[j]):
			append = False
	if append == True:
		equations_copy.append(store)


relations = array(equations_copy)
print "We removed duplicate rows"
print Matrix(relations)
print


######
# Row reduce over a group.
relations = rowReduce(relations, mod_num)
print "Row reduced relations over a group:"
print relations
print

if mod_num != 0:
	relations = relations % mod_num
	print "Modded by %d:" % mod_num
	print relations
	print





relations = array(removeTrivial(relations)) 
print "Remove trivial rows:"
print relations
print

# relations = array(sortDiagonal(relations))
# print "Diagonalized list of relations:"
# print relations
# print


######
# Substitute into general 2-cocycle f 
variable_num = relations.shape[1]

variables = symbols('L10:%d'% (variable_num+10))
chis = symbols('c0:%d'% (variable_num))

function = 0
for i in range(variable_num):
		function += variables[i]*chis[i]


relation_equations = []
for row in relations:
	expr = 0
	for i in range(variable_num):
		expr += row[i]*variables[i]
	# print expr
	# solved_expr = solve(expr)[0]
	# print solved_expr
	# if solved_expr != 0:
	# 	function = function.subs(solved_expr)
	# print
	relation_equations.append(expr)

print relation_equations
print

solved_relations = solve(relation_equations)
print solved_relations
print

if type(solved_relations) == list:
	for r in solved_relations:
		function = function.subs(r)
else:
	function = function.subs(solved_relations)
print function
print




###### TODO: remove lambdas that are zero
torsion_variables = []	# Deleltes lambdas that are torsion
for j in range(0, variable_num, int(sqrt(variable_num)) + 1):
	torsion_variables.append(j)

for n in torsion_variables:
	function = function.subs(variables[n], 0)

print Poly(function, variables)
coc_gens = Poly(function, variables).coeffs()

for item in coc_gens:
	if mod_num != 0:
		print item.expand()
	else: print item
print
# for a in range(6):
# 	for b in range(a+1,6):
# 		print"equation {} + {}".format(a+1,b+1)
# 		print (coc_gens[a] + coc_gens[b]).expand(modulus=mod_num)
# 		print


# print "equation 1 + 2 + 3"		
# print (coc_gens[0] + coc_gens[1] + coc_gens[2]).expand(modulus=mod_num)
# print

# print "equation 1 + 2 + 4"		
# print (coc_gens[0] + coc_gens[1] + coc_gens[3]).expand(modulus=mod_num)
# print

# print "equation 1 + 3 + 4"		
# print (coc_gens[0] + coc_gens[2] + coc_gens[3]).expand(modulus=mod_num)
# print

# print "equation 2 + 3 + 4"		
# print (coc_gens[1] + coc_gens[2] + coc_gens[3]).expand(modulus=mod_num)
# print

# print "equation 1 + 2 + 3 + 4"		
# print (coc_gens[0] + coc_gens[1] + coc_gens[2] + coc_gens[3]).expand(modulus=mod_num)
# print

######
# Computes coboundary matrix
cobs = array(matrixCoboundaries(M))
print "Coboundary matrix:"
print cobs
print


if mod_num != 0:
	cobs = cobs % mod_num
	print "Coboundaries modded by %d:" % mod_num
	print cobs
	print

cobs = rowReduce(cobs)
print "Coboundaries reduced over a group:"
print cobs
print

if mod_num != 0:
	cobs = cobs % mod_num
	print "Reduced Coboundaries modded by %d:" % mod_num
	print cobs
	print


######
cob_gens =[]
for row in cobs:
	expr = 0
	for i in range(variable_num):
		expr = expr + row[i]*chis[i]
	cob_gens.append(expr)

for stuff in Poly(function.subs(solve(cob_gens)), variables).coeffs():
	print stuff.expand()







