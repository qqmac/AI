'''
Quyen Mac
ECE 4524
Project 4
'''

import math
import sys
import copy
import re
from collections import defaultdict

# global variables
tree_dict = dict(list())
print_dict = list()
found = False
stop = False
final_name = list()

sys.setrecursionlimit(150000)

def predict(txtfile, input_data, dtree):
	attr_list = parse_file(txtfile)
	csv_list = parse_file(input_data)
	tree_list = parse_tree(dtree)
	csv_list = csv_list[:-1]

	attr_name = list()
	for i in attr_list:
		attr_name.append(i[0])

	new_csv = find_prediction(tree_list, csv_list, attr_list)
	for i in new_csv:
		del i[len(i) - 2]
	for i in new_csv:
		print i
	
	
'''top level learning function'''
def train(txt_file, csv_file, dtree_output, debug = 0):
	global final_name

	attr_list = parse_file(txt_file)
	csv_list = parse_file(csv_file)

	attr_name = list()
	for i in attr_list:
		attr_name.append(i[0])

	attr_dict = dict()
	new_attr_list = list()
	for csv in csv_list:
		for i in xrange(len(csv)):
			attr_dict[attr_name[i]] = csv[i]
		new_attr_list.append(attr_dict)
		attr_dict = dict()

	goal_list = list()
	for csv in csv_list:
		goal_list.append(csv[len(csv) - 1])


	# truncate class label
	attr_name = attr_name[:-1]
	attr_list = attr_list[:-1]
	new_attr_list = new_attr_list[:-1]
	goal_listname = goal_list[-1:]

	final_name = list(attr_name)

	decision_tree_learning(attr_name, attr_list, new_attr_list, goal_list)

	write_file(dtree_output)

# assign goals
def find_prediction(tree_list, csv_list, attr_list):
	found = list()
	
	for k, v in tree_list.iteritems():
		if v == "True":
			try:
				c = int(k)
				csv_list[int(k)].append("Yes")
			except Exception:
				pass
			
		elif v == "False":
			try:
				c = int(k)
				csv_list[int(k)].append("No")
			except Exception:
				pass

	return csv_list
	
''' parse tree txt file'''
def parse_tree(txtfile):
	myfile = open(txtfile, 'r');

	line_list = list()
	tokens = list()
	for line in myfile:
		line = line.strip()
		line_list.append(line.replace(' ', ''))

	found = list()
	goal_list = dict()
	key = ""
	for i in line_list:
		if i == "True" or i == "False":
			key = i
		if i.isdigit() and i not in found:
			goal_list[i] = key
			found.append(i)

	
	return goal_list

'''read file'''
def parse_file(txt_file):
	myfile = open(txt_file, 'r');

	line_list = list()
	tokens = list()
	for line in myfile:
		line = line.strip()
		line_list.append(line.replace(' ', '').split(','))

	return line_list

def write_file(txtfile):
	global print_dict
	with open(txtfile, "w") as f:
		for line in print_dict:
			f.write(str(line))
			f.write("\n")

	
	f.close()

''' runs decision tree learner'''
def decision_tree_learning(attr_name, attr_list, new_attr_list, goal_list):
	global tree_dict
	# get list of attribute names that does not end in Yes or No
	names = start_names(attr_list)
	
	child_list = list()
	# names with no yes/no, list of names, list of name + attr, list of dict
	pointer = None
	
	final_tree = tree(names, attr_name, new_attr_list, goal_list, attr_list, pointer)
	print_tree(final_tree)
		
	
'''print tree, stores into stringlist'''
def print_tree(final_tree):

	global print_dict, final_name
	if isinstance(final_tree, dict):
		# indent += "\t"
		for x in final_tree:
			# print x
			if x in final_name:
				print_dict.append("ROOT: " + x)
			else:
				print_dict.append("SUBTREE: " + x)

			print_tree(final_tree[x])
	elif isinstance(final_tree, list):
		for f in final_tree:
			try:
				print_dict.append("CHILD: " + f.get_attr_name())
				print_dict.append(f.get_goal())
			except Exception:
				# print_dict.append(f.get_goal())
				pass
			print_tree(f)
	else:
		f = final_tree.__iter__()

		for i in f:
			print_dict.append(i)


'''tree iterator'''
def tree(names, attr_name, new_attr_list, goal_list, attr_list, pointer):
	global tree_dict, found
	''' until all names are read'''
	if len(names) != 0:
		big_data = dict()
		big_data2 = dict()
		#iterate through "valid" names, use entropy to set the root
		gain = list()

		for each in names:
			for attr in attr_list:
				# get the children attributes
				
				if attr[0] == each:	
					data_list = list()
					data_list2 = list()
					for x in xrange(1, len(attr)):
						dat = Data(goal_list)
						dat.add_example(new_attr_list, each, attr[x])
						data_list.append(dat)
					# calculate entropy
					big_data[each] = data_list

					gain.append((entropy(data_list), each))
		# this will be the root of the tree
		high_gain = highest_gain(gain)
		# remove name from all attributes
		for i in xrange(len(attr_name)):
			if attr_name[i] == high_gain:
				del attr_name[i]
				break
		# remove from name list
		for i in xrange(len(names)):
			if names[i] == high_gain:
				del names[i]
				break


		# add root node to tree_dict
		if pointer == None:
			tree_dict[high_gain] = big_data[high_gain]
		else:
			found = False
			new_node = dict()
			new_node[high_gain] = big_data[high_gain]
			recurse_tree(tree_dict, pointer, new_node)

		# get tree and leaf nodes
		treeN, leafN = which_childen(big_data[high_gain])

		# update names list
		names = new_names(attr_list, attr_name, names, leafN)

		for done in treeN:
			tree(names, attr_name, new_attr_list, goal_list, attr_list, done)


	return tree_dict

# gets the children that are tree nodes and leaf nodes
def which_childen(children):
	leafN = list()
	treeN = list()
	for i in children:
		if i.is_tree():
			treeN.append(i.get_attr_name())
		else:
			leafN.append(i.get_attr_name())
	return treeN, leafN

# recursively update tree
def recurse_tree(d, attr, new_node):
	global found, stop
	if found:
		return d

	if type(d) == type({}):
		for k in d:
			if found:
				return d
			x = recurse_tree(d[k], attr, new_node)
			d[k] = x
	elif isinstance(d, list):
		c = d
		for i in c:
			if found:
				return d
			try:
				x = recurse_tree(i, attr, new_node)
			except ValueError:
				pass
			if found:
				try:
					n = dict()
					n[x] = new_node
					d.append(n)
					stop = True
				except Exception:
					""
				return d
	elif isinstance(d, int):
		pass
	else:
		# is a Data node
		if found:
			return d
			
		if d.get_attr_name() == attr:
			found = True
			return d.get_attr_name()
		else:
			# child data node
			return d.get_attr_name()

	return d

# get the highest gain
def highest_gain(gain):
	if len(gain):
		ret_val = max(gain)[1]
	else:
		return None

	return ret_val

# entropy value
def entropy(data_list):
	'''Return B(p/p+n) - Remainder(attr)'''
	pos = 0
	neg = 0
	for dat in data_list:
		
		pos = pos + dat.get_positive()
		neg = neg + dat.get_negative()

	q = float(pos) / float(pos + neg)
	try:
		b = -(q * math.log(q, 2) + (1 - q) * math.log( (1 - q), 2) )
	except ValueError:
		b = 0

	rem = 0

	for dat in data_list:
		try:
			q = float( dat.get_positive()) / float(dat.get_positive() + dat.get_negative())
			b = -(q * math.log(q, 2) + (1 - q) * math.log( (1 - q), 2) )
			rem = rem + ( float(dat.get_positive() + dat.get_positive()) / float(pos + neg) * b)
		except ValueError:
			""

	return b - rem

def start_names(attr_list):
	ret_val = list()
	for each in attr_list:
		# check to see if attribute is > 3
		if len(each) > 3:
			ret_val.append(each[0])

	return ret_val

def new_names(attr_list, attr_name, names, leafN):
	count = 0
	for each in attr_list:
		if each[0] in attr_name and each[0] not in names:
			names.append(each[0])
		count += 1
	return names

'''holds the examples'''
class Data():
	''' default constructor '''
	def __init__(self, goal_list):
		self.positive = list()
		self.negative = list()
		self.attrList = list()
		self.goal_list = goal_list
		self.leafNode = False
		self.treeNode = False
		self.num = []
		self.yes = None
		self.no = None
		self.pos = 0
		self.neg = 0
		self.attr = ""

	def add_example(self, new_attr_list, name, attribute):
		# add the examples according to the attribute name
		# keep track of pos and neg
		count = 0
		for each in new_attr_list:
			for k, v in each.iteritems():
				if k == name and v == attribute:
					self.num.append(count)
					if self.goal_list[count] == "Yes":
						self.pos = self.pos + 1
					else:
						self.neg = self.pos + 1

					self.attrList.append(each)
			count += 1
		self.attr = attribute

	# return true if yes, false if no
	def get_goal(self):
		self.is_leaf()
		return self.yes

	def return_print(self):
		ret_val = list()
		count = 0
		for each in self.attrList:
			ret_val.append(self.goal_list[count])
			count += 1

		return ret_val

	def is_leaf(self):
		if self.pos == 0 and self.neg > 0:
			self.leafNode = True
			self.treeNode = False
			self.no = True
			self.yes = False
		elif self.neg == 0 and self.pos > 0:
			self.leafNode = True
			self.treeNode = False
			self.no = False
			self.yes = True
		else:
			self.treeNode = True
			self.leafNode = False
		return self.leafNode

	def is_tree(self):

		if self.pos == 0 and self.neg > 0:
			self.leafNode = True
			self.treeNode = False
			self.yes = True
			self.no = False
		elif self.neg == 0 and self.pos > 0:
			self.leafNode = True
			self.treeNode = False
			self.no = False
			self.yes = True
		else:
			self.treeNode = True
			self.leafNode = False
	

		return self.treeNode

	def get_plurarity(self):
		return (self.pos >= self.neg)

	def get_positive(self):
		return self.pos

	def get_negative(self):
		return self.neg

	def __iter__(self):
		return iter(self.num)

	def get_list(self):
		return self.attrList

	def get_attr_name(self):
		return self.attr


if __name__ == '__main__':
	# train("training_attributes.txt", "restaurant.csv", "decision_tree.txt")
	predict("training_attributes.txt", "training_data.csv", "decision_tree.txt")