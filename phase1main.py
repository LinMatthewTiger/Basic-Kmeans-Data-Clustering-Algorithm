# Matthew Lin
# This is a basic k-means algorithm for multidimensional vectors
# Run using anaconda command prompt. Enter "python phase1main.py iris_bezdek.txt 3 100 0.0001 3"
# LIBRARIES-----------------------------------------------------------------------
from random import randint
import math
import copy
import sys

# FUNCTIONS---------------------------------------------------------------------

# FILE READER
def init(filename):
	numbers = []
	file = open(filename,'r')
	for line in file:
		items = line.split()
		for item in items:
			numbers.append(float(item))
	return numbers

# FIND EUCLIDEAN DISTANCE
def euclideanDist(x, y):
	distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))
	return distance

# ADD 2 VECTORS TOGETHER
def addvectors(data, cluster, dim):
	temp = []
	for i in range(dim):
		temp.append(0)
	for i in range(dim):
		temp[i] = data[i] + cluster[i]
	return temp

# DIVIDE 2 VECTORS
def dividevectors(cluster, todivide):
	for index1, i in enumerate(cluster):
		for index2, j in enumerate(i):
			if(todivide[index1] == 0):
				todivide[index1] += 1
			cluster[index1][index2] = cluster[index1][index2]/todivide[index1]
	return cluster

# MAIN()----------------------------------------------------------------------------------------------------------
# Declare run counter
countrun = 0
SSCBest = 0
RunBest = 0

# ARGUMENTS
file = sys.argv[1] # iris_bezdek.txt
numofclus= int(sys.argv[2]) # 3
maxiter= int(sys.argv[3]) # 100
converg = float(sys.argv[4]) # 0.0001
runs = int(sys.argv[5]) # 3

# Pull data from file and utilize number of points and dimension inputs
data = init(file)
numofpoints = int(data[0])
data.pop(0)
dim = int(data[0])
data.pop(0)

# Initalize write file
newfile = "output_" + file
output = open(newfile, 'w')
output.write(file + " " + str(numofclus) + " " + str(maxiter) + " " + str(converg) + " " + str(runs))

# Sublist the data based on dim 
data = [data[i:i+dim] for i in range(0,len(data), dim)]

# LOOP FOR NUMBER OF RUNS
while True:
	print("\nRun:", countrun + 1)
	print("-----------------------")
	output.write("\n\nRun: " + str(countrun + 1))
	output.write("\n-----------------------")
	# Declared variables
	SSC = 1.0
	T = 0.0
	clusters = []
	clusters_update = []
	divisor = []
	loops = 0

	# Generate random cluster values
	for i in range(numofclus):
		clusters.append(data[randint(0,numofpoints-1)]) 

	# LOOP UNTIL CONVERGENCE OR MAX ITERATIONS
	while True:
		# Reset values for multiple iterations
		divisor = []
		smallest = 0
		temp_SSC = 0.0

		#Declare divisor array used for calcuating means
		for i in range(numofclus):
			divisor.append(0)

		# Array copy and initalizing
		clusters_update = copy.deepcopy(clusters)
		for index1, cluster in enumerate(clusters_update):
			for index2, value in enumerate(cluster):
				clusters_update[index1][index2] = 0

		#K-MEANS
		for point in data: # For every point
			for index, cluster in enumerate(clusters): # For every cluster, compare the distance between all the points
				if(index == 0): # If smallest point is first value
					save = index 
					smallest = euclideanDist(point,cluster)
				elif(smallest > euclideanDist(point,cluster)): 
					save = index #Save the cluster index of the smallest value
					smallest = euclideanDist(point,cluster) #Save value of the smallest distance for SSC

			divisor[save] += 1 #Increment corresponding value for divisor
			temp_SSC += smallest * smallest #Square the smallest distance for SSC
			clusters_update[save] = addvectors(clusters_update[save], point, dim) #Add the vectors to prepare for finding means
		
		clusters_update = dividevectors(clusters_update, divisor) #Divide, find means to relocate clusters
		clusters = copy.deepcopy(clusters_update) # Copy the updated clusters for convergence and multiple iterations

		#Calcuate T
		T = math.fabs(SSC-temp_SSC)/SSC
		#Copy SSC for next iterations
		SSC = temp_SSC
		#Print SSC
		print("Iteration", loops + 1, ": SSC =" ,SSC)
		output.write("\nIteration " + str(loops + 1) + " : SSC = " + str(SSC))

		#Increment iteration
		loops += 1

		#Conditionals for breaking loop when nessecary
		if(loops >= maxiter or T < converg):
			break

	# Find and Save best run
	if(countrun == 0):
		SSCBest = SSC
		RunBest = countrun + 1
	elif(SSCBest > SSC):
		SSCBest = SSC
		RunBest = countrun + 1
	#Run until declared runs
	countrun += 1
	if(countrun >= runs):
		break

# Print Best Run
print("\n\nBest Run:",RunBest ,": SSC =",SSCBest)
output.write("\n\n\nBest Run: "  + str(RunBest) + " : SSC = " + str(SSCBest))
