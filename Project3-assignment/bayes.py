'''
Quyen Mac
Project 3
ECE 4524
'''

from collections import defaultdict
import os

''' main function'''
def bayes(file_name):
	# initialize global variables
	global num, return_val, val_list, keep_track, solved, tempchildren, empty_dict, total

	# parse file
	var_dict, var_prob, parent_child = parser(file_name)
	print var_dict
	print var_prob
	print parent_child

	os.system('clear')
	while (True):
		print "Choosing from at least one the following variables, enter the correct values to the corresponding variable and separate by commas."
		print "For example: WEATHER = TRUE, FIRE = NONE\n"
		print "Enter 'quit' to end the program\n"
		print "From the following list: "
		print var_dict
		user_input = raw_input("Separate the '=' with spaces in between. Please enter your values to calculate the probablity: ").upper()
		if (user_input == "QUIT"):
			os.system('clear')
			break
		else:
			is_valid, ret_vals = valid_input(user_input, var_dict)
			if (is_valid == False):
				# invalid input
				os.system('clear')
				print "INVALID INPUT! Please enter the correct input.\n"
			else:
				# valid input, parse the inputs.
				p_list, index = joint_prob(ret_vals, parent_child, var_prob, var_dict)
				summ = calculate(p_list, index, var_prob)

				print "\nThe summation of your input, " + user_input + " , is: \n"
				print summ
				print "\n"

''' calculate the joint probability, returns the probability list and index '''
def joint_prob(ret_vals, parent_child, var_prob, var_dict):
	index = dict()
	p_list = list()
	keys = ret_vals.keys()
	joint_sum = 1
	for k, v in ret_vals.iteritems():
		prob = dict()
		for par, child in parent_child.iteritems():
			if par == k:
				# get list of probabilities
				p_list = get_prob(k, v, var_prob, ret_vals, child, var_dict, p_list, parent_child, index)

	# do while. looks for remaining probability functions
	need = double_check(p_list[0], parent_child)
	for i in need:
		for k in i:
			p_list = get_prob(k, i, var_prob, ret_vals, parent_child[k], var_dict, p_list, parent_child, index)

	while need != []:
		need = double_check(p_list[0], parent_child)
		for i in need:
			for k in i:
				p_list = get_prob(k, i, var_prob, ret_vals, parent_child[k], var_dict, p_list, parent_child, index)

	
	return p_list, index

# calculate the values
def calculate(p_list, index, var_prob):
	summation = 0
	for p in p_list:
		summ = 1
		for j in p:
			for k, v in j.iteritems():
				if isinstance(v, dict):
					# look into big dictionary
					for kk, vv in var_prob.iteritems():
						if kk == k:
							for l in vv:
								for kkk, vvv in l.iteritems():
									if kkk == index[k]:
										for x in vvv:
											for c, b in x.iteritems():
												if c == str(v):
													summ *= float(b)

				else:
					# node with no parent
					for kk, vv in var_prob.iteritems():
						if kk == k:
							# equal names
							for e in vv:
								for kkk, vvv in e.iteritems():
									if kkk == v:
										summ *= float(vvv)
		summation += summ

	return summation

# checks for missing probability functions, returns a list of it
def double_check(pl, parent_child):
	needToAdd = list()
	for p in pl:

		for k, v in p.iteritems():
			if isinstance(v, dict):
				for kk, vv in v.iteritems():
					if in_array(kk, pl) == False:
						d = dict()
						d[kk] = k 
						needToAdd.append(d)
	return needToAdd

# if the item is in the array list
def in_array(name, pl):
	for p in pl:
		for k, v in p.iteritems():
			if name == k:
				return True

	return False

# main method that splits up the probabilities
def get_prob(name, val, var_prob, ret_vals, child, var_dict, p_list, parent_child, index):
	for k, v in var_prob.iteritems():
		if k == name:
			# get each value from table
			for q in v:
				# second pass, after finding the incomplete probability list
				if isinstance(val, dict):
					values = q.values()
					for i in values:
						prob = dict()
						pList = list()
						childcopy = list(child)
						pList2 = list()
						if isinstance(i, list):
							# get probability list from recursion
							probList =  recursion(child[0], childcopy, var_dict, ret_vals, prob, pList)
							if p_list == []:
								for p in probList:
									newList = list()
									d = dict()
									d[name] = p
									newList.append(d)
									pList2.append(newList)

							else:
								for p in probList:
									newList = list()
									d = dict()
									d[name] = p
									newList.append(d)
									for o in p_list:
										pList2.append(newList + o)

							index[name] = val
						else:
							# update values
							for x in p_list:
								for y in x:
									for v, b in y.iteritems():
										if v in val.values():
											for gg, hh in b.iteritems():
												if gg == name:
													tempD = dict()
													tempD[name] = hh
													newList = list()
													newList.append(tempD)
													pList2.append(newList + x)
								
							index[name] = val
						return pList2
				else:
					# calculates the first probability list
					temp = list()
					temp.append(val)
					if q.keys() == temp:
						values = q.values()
						for i in values:
							prob = dict()
							pList = list()
							childcopy = list(child)
							pList2 = list()
							if isinstance(i, list):
								# get probability list
								probList =  recursion(child[0], childcopy, var_dict, ret_vals, prob, pList)
								if p_list == []:
									for p in probList:
										newList = list()
										d = dict()
										d[name] = p
										newList.append(d)
										pList2.append(newList)

								else:
									for p in probList:
										newList = list()
										d = dict()
										d[name] = p
										newList.append(d)
										for o in p_list:
											pList2.append(newList + o)

								# keep an index of names and their value
								index[name] = val
								
							else:
								# leaf node
								if p_list == []:
									tempD = dict()
									tempD[name] = val
									newList = list()
									newList.append(tempD)
									pList2.append(newList)

								else:
									pList2 = p_list
									for x in pList2:
										tempD = dict()
										tempD[name] = val
										x.append(tempD)
								index[name] = val

							return pList2


''' recursive function that gets each possibly combinations of a probability '''
def recursion(start, child, var_dict, ret_vals, prob, pList):
	temp = list(child)
	foo = var_dict[start]
	for f in foo:
		prob[start] = f
		if len(child) > 1:
			del child[0]
			pList = recursion(child[0], child, var_dict, ret_vals, prob, pList)
		elif child[0] != start:
			# go back up the recursion
			child = temp
			del child[0]
			pList = recursion(child[0], child, var_dict, ret_vals, prob, pList)
			
		else:
			# store the probability into a list
			if in_list(ret_vals, prob):

				pList.append(prob.copy())
	return pList

# checks if the probability is valid
def in_list(ret_vals, prob):
	for k, v in prob.iteritems():
		if k in ret_vals:
			if v != ret_vals[k]:
				return False
	return True
		
# checks user input
def valid_input(user_input, var_names):
	ret_vals = dict()
	word = user_input.split(",")
	for x in word:
		y = x.split()
		if (y[0] not in var_names):
			return False, ret_vals
		for k, v in var_names.iteritems():
			if k == y[0] and y[2] not in v:
				return False, ret_vals
		ret_vals[y[0]] = y[2]
	return True, ret_vals

'''
parses the bif file
all of the parsing is stored into dictionaries
stacked upon each other
'''
def parser(file_name):
	myfile = open(file_name, 'r')

	line_list = list()
	var_dict = dict()

	for line in myfile:
		line_list.append(line)

	myfile.close()
	var_key = ""
	prob_key = ""
	probabilities = list()
	var_val = list(defaultdict(list))

	temp_dict = defaultdict(list)
	parent_child = dict()

	var_val_list = list()
	var_val_dict = dict()

	solve_prob = False

	# parse the variables and probability
	for line in line_list:
		tokens = line.split()

		if len(tokens) != 0:
			# if variable node
			if tokens[0] == "variable":
				var_key = tokens[1]
			# get values under variable node
			elif tokens[0] == "type":
				t = int(tokens[3])
				for x in xrange(6, 6+t):
					if tokens[x].endswith(','):
						tokens[x] = tokens[x][:-1]
					# assign temp value for value
					temp_dict[tokens[x]].append(0)

					var_val.append(temp_dict.copy())
					var_val_list.append(tokens[x])

					temp_dict = defaultdict(list)
					
				var_dict[var_key] = var_val
				var_val_dict[var_key] = var_val_list
				
				# empty list
				var_val = list(dict())
				var_val_list = list()
			# if probability node
			elif tokens[0] == "probability":
				prob_key = tokens[2]
				for x in xrange(4, len(tokens) - 1):
					if x != "{" and x != "," and x != ")":
						if tokens[x].endswith(',') or tokens[x].endswith(")"):
							tokens[x] = tokens[x][:-1]
						if (tokens[x] != ""):
							probabilities.append(tokens[x])
				parent_child[prob_key] = probabilities

				solve_prob = True
			# get values of probability node
			elif tokens[0] == "table":
				count = 1
				for key, value in var_dict.iteritems():
					if key == prob_key:
						for val in value:
							for k in val:
								if tokens[count].endswith(',') or tokens[count].endswith(";"):
									tokens[count] = tokens[count][:-1]
								val[k] = tokens[count]
								count += 1
				solve_prob = False
			# get values from probability node
			elif tokens[0] != "}":
				if solve_prob:
					prob_vars = list()
					prob_num = list()
					

					for key, value in var_dict.iteritems():
						if key == prob_key:
							# iterate through each value in key

							# get the values from line
							for i in xrange(0, len(probabilities)):
								if tokens[i].startswith("("):
									tokens[i] = tokens[i][1:]
								if tokens[i].endswith(",") or tokens[i].endswith(")"):
									tokens[i] = tokens[i][:-1]
								prob_vars.append(tokens[i])

							# get the numbers from line
							for i in xrange(len(probabilities), len(value) + len(probabilities)):
								if tokens[i].endswith(",") or tokens[i].endswith(";"):
									tokens[i] = tokens[i][:-1]
								prob_num.append(tokens[i])

							copyDict = var_val_dict.copy()
							tempDict = dict()
							tempDict2 = dict()
							for i in xrange(0, len(probabilities)):
								tempDict[probabilities[i]] = prob_vars[i]
							
							count = 0

							for i in value:
								for y, m in i.iteritems():
									tempDict2[str(tempDict)] = prob_num[count]
									count += 1
									if m[0] == 0:
										i[y].remove(0)
									i[y].append(tempDict2)
									tempDict2 = dict()
			# stop getting values form probability list
			elif tokens[0] == "}":
				solve_prob = False
				probabilities = list()

				
	# returns one big dictionary, a dictionary with the variable and probability value,
	# and a dictionary with parent and child value
	return var_val_dict, var_dict, parent_child

if __name__ == '__main__':

    filename = "burglar-alarm.bif"
    bayes(filename)