#----------------------------------------------------------------------
import random
from deap import creator, base, tools, algorithms
#-----------------------------------------------
import numpy as np # Import modules
import subprocess
import sys
import os
import datetime # for results folder
#----------------------------------------------------------------------
# Usage: command:
# 0. pip3 install -U deap==1.4.1 --user
# 1. rewrite skdef.hsd.tmp_ga and prepare band_check folder (e.g., see Mn folder)
# 2. rewrite initial parameters and boundaries in ga_v1.py
# 3. python3 ga_v1.py
# 4. sort -k 2 Evalute.txt >> Evalute_sort.txt
#----------------------------------------------------------------------
file_tmp = 'skdef.hsd.tmp_ga'
file_inp = 'skdef.hsd'
file_msd = 'msd.dat'

#cif2cell_adress = "cif2cell"

subprocess.run("export OMP_NUM_THREADS=1", shell=True)
sub_num_core = subprocess.run("grep 'core id' /proc/cpuinfo | sort -u | wc -l", shell=True, stdout=subprocess.PIPE)
print("CPU: ",str(sub_num_core.stdout).lstrip("b'").rstrip("\\n'"))
num_core = int(str(sub_num_core.stdout).lstrip("b'").rstrip("\\n'"))
dftbp_adress = "mpirun -np "+str(num_core)+" dftb+"
#skprogs_adress = "/home/ubuntu/skprogs-v.0.2.1/sktools/src/sktools/scripts/skgen.py" # Linux
skprogs_adress = "/mnt/d/skprogs-v.0.2.1/sktools/src/sktools/scripts/skgen.py" # WSL2
#pwscf_adress = "mpirun -np "+str(num_core)+" pw.x"

#----------------------------------------------------------------------
# set initial parameters and boundaries
#----------------------------------------------------------------------
element = "Mn"
atomic_number = 25.0 # In this code, this value is used as a parameter of the radial wave function.
#---------------------------
# The parameters of the radial wave function.
#y0s = 0.5 # S orbitals
#y0p = 0.5 # P orbitals
#y0d = 1.5 # D orbitals
y0s = 2.0 # S orbitals, TM: 2.0
y0p = 2.0 # P orbitals, TM: 2.0
y0d = 2.5 # D orbitals, TM: 2.5
#--------
# The parameters of the radial wave function.
#ylasts = atomic_number      # S orbitals
#ylastp = atomic_number      # P orbitals
#ylastd = atomic_number*2.0  # D orbitals
ylasts = atomic_number*2.0  # S orbitals, TM: x2.0
ylastp = atomic_number*2.0  # P orbitals, TM: x2.0
ylastd = atomic_number*3.0  # D orbitals, TM: x2.0
#---------------------------

#------------------------------------------------
# Note: Empirically, setting a value around 0.3 will significantly reduce the number of failures.
hwb  =  0.5 # search range [-x*hwb:+x*hwt]
hwt  =  1.0 # search range [-x*hwb:+x*hwt]
#---------------------------
hwb_sto = 0.07 # search range [-x*hwb:+x*hwt]
hwt_sto = 0.07 # search range [-x*hwb:+x*hwt]
#---------------------------
# Note
# 1. A value around sigma = 7.0 is often good.
# 2. It is often good for r0 for the S orbit to be slightly (about 0.7 ?) smaller than for the P or D orbits.
# 3. In the radial wave function, calculations can be converged over a fairly wide range for the S orbit, 
#   but of course the P orbit is more limited than the S orbit. When increasing the value, 
#   start from the value at which the P orbit begins to converge. Conversely, when decreasing the value, 
#   start from the value at which the P orbit begins to converge.
# 4. In transition metals, it is often sufficient to adjust the P orbital last.
# 5. The radial wave function only slightly moves the position of each orbit. 
#---------------------------
x0  =  7.0 # sigma of density
x1  = 14.0 # r0 of density
#---------------------------
x2  =  7.0 # simga of S
x3  =  6.3 # r0 of S
#---------------------------
x4  =  7.0 # simga of P
x5  =  7.2 # r0 of P
#---------------------------
x6  =  7.0 # simga of D
x7  =  7.2 # r0 of D
#---------------------------
x8  =  4.56 # y1 of S
x9  = 10.39 # y2 of S
x10 = 23.69 # y3 of S
#---------------------------
x11 =  4.56 # y1 of P
x12 = 10.39 # y2 of P
x13 = 23.69 # y3 of P
#---------------------------
x14 =  6.22 # y1 of D or D
x15 = 14.69 # y2 of D or D
x16 = 35.09 # y3 of D or D
#---------------------------
print("------------------------")
print("initial parameters:   x0  x1  x2  x3  x4  x5  x6  x7   x8   x9"
  +"  x10  x11  x12  x13  x14  x15  x16")
print("initial parameters: ",x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16)
x = [x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16]
#------------------------------------------------

#------------------------------------------------
if os.path.exists("./Evalute.txt"):
  subprocess.run("cd ./"+element+" ; cp ./../Evalute.txt ./results/Evalute.txt ; cd ../", shell=True)
  subprocess.run("cd ./"+element+" ; cp ./../Evalute_sort.txt ./results/Evalute_sort.txt ; cd ../", shell=True)
  now = datetime.datetime.now()
  subprocess.run("cd ./"+element+" ; mv results results_{0:%Y%m%d-%H%M%S}".format(now)+" ; cd ../", shell=True)
subprocess.run("cd ./"+element+" ; mkdir results ; cd ../", shell=True)
subprocess.run("cd ./"+element+" ; chmod +x *.sh ; cd ../", shell=True)
#-------------------------------
subprocess.run("echo \"#No.: ETA [eV], sigma_den, r0_den, simga_s, r0_s, sigma_p, r0_p, sigma_d, r0_d,"
  +" stos(y1s), stos(y2s), stos(y3s), stop(y1p), stop(y2p), stop(y3p), stod(y1d), stod(y2d), stod(y3d), sdt, sdt3kbt"
  +" \" > Evalute.txt", shell=True)
subprocess.run("echo \"#| iter | ETA | x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 |"
  +" x9 | x10 | x11 | x12 | x13 | x14 | x15 | x16 | SDT | SDT(3kbT) |\" >> Evalute.txt", shell=True)
#------------------------------------------------

#------------------------------------------------
# set initial values
etav = 0.0
stdv = 0.0
stdv3kbt = 0.0
#------------------------------------------------

count = 0
#----------------------------------------------------------------------
# Set as a minimization problem (-1.0 minimizes, 1.0 maximizes)
creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
#---------------------------
# Definition of individual (just specify the list type, the contents of the genes will be added later)
creator.create("Individual", list, fitness=creator.FitnessMax)
#---------------------------
# Use functions in the DEAP Toolbox for crossover, selection, mutation, etc.
toolbox = base.Toolbox()

#------------------------------------------------
print("------------------------")
n_gene = 17 # number of parameters
min_ind = np.ones(n_gene) * -1.0
max_ind = np.ones(n_gene) *  1.0
#---------------------------
for i in range(0,8):
  min_ind[i] = float(x[i]) - float(x[i])*hwb
  max_ind[i] = float(x[i]) + float(x[i])*hwt
  print("search area of paramter "+str(i)+": "+str(min_ind[i])+" | "+str(max_ind[i]))
for i in range(8,n_gene):
  min_ind[i] = float(x[i]) - float(x[i])*hwb_sto
  max_ind[i] = float(x[i]) + float(x[i])*hwt_sto
  print("search area of paramter "+str(i)+": "+str(min_ind[i])+" | "+str(max_ind[i]))
#----------------------------------------------------------------------
# Create a create_ind_uniform function to define boundaries (minimum, maximum) for later use.
def create_ind_uniform(min_ind, max_ind):
  ind = []
  for min, max in zip(min_ind, max_ind):
    ind.append(random.uniform(min, max))
  return ind
#----------------------------------------------------------------------
# Set the alias of "create_ind_uniform" as "create_ind". 
# The genetic content of each individual is determined within the boundaries (minimum, maximum).
toolbox.register("create_ind", create_ind_uniform, min_ind, max_ind)
#---------------------------
# Set a function called "individual". The genes included in each individual are determined using "create_ind."
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.create_ind)
#---------------------------
# Prepare a function to set the number of individuals in the population
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
#----------------------------------------------------------------------
# Definition of objective function. Be sure to add a , after return.
#---------------------------
def evalOneMax(individual):
  
  print("------------------------")
  global count
  count += 1
  print(count)
  
  if os.path.exists(element+"-"+element+".skf"):
    print("------------------------")
    print("Delete old "+element+"-"+element+".skf file")
    subprocess.run("rm -f "+element+"-"+element+".skf", shell=True)
  
  subprocess.run("cp "+" "+file_tmp+" "+file_inp, shell=True)
  
  #-------------------------------
  # Additional additions are due to rounding.
  R1 = 0.05
  R2 = 0.005
  # The number of valid digits is limited based on literature and preliminary grid search results.
  # It is more important to expand the search range than to search in more detailed steps.
  # Rather than searching in even smaller steps, it is important to widen the search range or 
  #   change the initial values to make sure that the solution does not fall into a locally optimal solution.
  #-------------------------------
  # Density
  sx0  = "{:.1f}".format(individual[0]+R1)
  sx1  = "{:.1f}".format(individual[1]+R1)
  #-------------------------------
  # S orbital
  sx2  = "{:.1f}".format(individual[2]+R1)
  sx3  = "{:.1f}".format(individual[3]+R1)
  #-------------------------------
  # P orbital
  sx4  = "{:.1f}".format(individual[4]+R1)
  sx5  = "{:.1f}".format(individual[5]+R1)
  #-------------------------------
  # D orbital
  sx6  = "{:.1f}".format(individual[6]+R1)
  sx7  = "{:.1f}".format(individual[7]+R1)
  #-------------------------------
  # Slater-Type Orbitals of S
  sx8  = "{:.2f}".format(individual[8]+R2)
  sx9  = "{:.2f}".format(individual[9]+R2)
  sx10 = "{:.2f}".format(individual[10]+R2)
  #-------------------------------
  # Slater-Type Orbitals of P
  sx11 = "{:.2f}".format(individual[11]+R2)
  sx12 = "{:.2f}".format(individual[12]+R2)
  sx13 = "{:.2f}".format(individual[13]+R2)
  #-------------------------------
  # Slater-Type Orbitals of D
  sx14 = "{:.2f}".format(individual[14]+R2)
  sx15 = "{:.2f}".format(individual[15]+R2)
  sx16 = "{:.2f}".format(individual[16]+R2)
  #-------------------------------
  
  #-------------------------------
  # Density
  subprocess.call("sed -i s/sigma_den/"+sx0+"/g "+file_inp, shell=True)
  subprocess.call("sed -i s/r0_den/"+sx1+"/g "+file_inp, shell=True)
  #-------------------------------
  # S orbital
  subprocess.call("sed -i s/sigma_s/"+sx2+"/g "+file_inp, shell=True)
  subprocess.call("sed -i s/r0_s/"+sx3+"/g "+file_inp, shell=True)
  #-------------------------------
  # P orbital
  subprocess.call("sed -i s/sigma_p/"+sx4+"/g "+file_inp, shell=True)
  subprocess.call("sed -i s/r0_p/"+sx5+"/g "+file_inp, shell=True)
  #-------------------------------
  # D orbital
  subprocess.call("sed -i s/sigma_d/"+sx6+"/g "+file_inp, shell=True)
  subprocess.call("sed -i s/r0_d/"+sx7+"/g "+file_inp, shell=True)
  #-------------------------------
  # Slater-Type Orbitals of S
  stos_all = str(y0s)+" "+sx8+" "+sx9+" "+sx10+" "+str(ylasts)
  subprocess.call("sed -i s/stos/\""+stos_all+"\"/g "+file_inp, shell=True)
  #-------------------------------
  # Slater-Type Orbitals of P
  stop_all = str(y0p)+" "+sx11+" "+sx12+" "+sx13+" "+str(ylastp)
  subprocess.call("sed -i s/stop/\""+stop_all+"\"/g "+file_inp, shell=True)
  #-------------------------------
  # Slater-Type Orbitals of D
  stod_all = str(y0d)+" "+sx14+" "+sx15+" "+sx16+" "+str(ylastd)
  subprocess.call("sed -i s/stod/\""+stod_all+"\"/g "+file_inp, shell=True)
  #-------------------------------
  
  subprocess.run("export OMP_NUM_THREADS="+str(num_core), shell=True)
  skgen = subprocess.run("python3 "+str(skprogs_adress)+" -o slateratom -t sktwocnt sktable -d "+element+" "+element, shell=True, stdout=subprocess.PIPE)
  subprocess.run("export OMP_NUM_THREADS=1", shell=True)
  
  if os.path.exists(element+"-"+element+".skf"):
    subprocess.run("cd ./"+element+" ; ./run.sh ; cd ../", shell=True)
    evaluate = subprocess.run("awk '{if(NR==10){printf \"%s\",$3}}' ./"+element+"/"+file_msd, shell=True, stdout=subprocess.PIPE)
    evaluate_sdt = subprocess.run("awk '{if(NR==4){printf \"%s\",$3}}' ./"+element+"/"+file_msd, shell=True, stdout=subprocess.PIPE)
    evaluate_sdt3kbt = subprocess.run("awk '{if(NR==8){printf \"%s\",$3}}' ./"+element+"/"+file_msd, shell=True, stdout=subprocess.PIPE)
    if evaluate.returncode == 0:
      try:
        etav = float(str(evaluate.stdout).lstrip("b'").rstrip("\\n'"))
        sdtv = float(str(evaluate_sdt.stdout).lstrip("b'").rstrip("\\n'"))
        sdtv3kbt = float(str(evaluate_sdt3kbt.stdout).lstrip("b'").rstrip("\\n'"))
        y = etav
        subprocess.run("mv "+file_inp+" ./"+element+"/results/"+file_inp+"_No"+str(count), shell=True)
        subprocess.run("cp ./"+element+"/comp_band.png ./"+element+"/results/comp_band_No"+str(count)+".png", shell=True)
      except ValueError as error:
        y = 9.999
        etav = 9.999
        sdtv = 9.999
        sdtv3kbt = 9.999
    else:
      y = 9.999
      etav = 9.999
      sdtv = 9.999
      sdtv3kbt = 9.999
  else:
    y = 9.999
    etav = 9.999
    sdtv = 9.999
    sdtv3kbt = 9.999

  print("------------------------")
  print("iter:",count)
  print("------------------------")
  print("target:",str(y))
  print("------------------------")
  print("Density")
  print("set parameters, sigma_den = x0: "+sx0)
  print("set parameters, r0_den = x1: "+sx1)
  print("------------------------")
  print("S orbital")
  print("set parameters, sigma_s = x2: "+sx2)
  print("set parameters, r0_s = x3: "+sx3)
  print("------------------------")
  print("P orbital")
  print("set parameters, sigma_p = x4: "+sx4)
  print("set parameters, r0_p = x5: "+sx5)
  print("------------------------")
  print("D orbital")
  print("set parameters, sigma_d = x6: "+sx6)
  print("set parameters, r0_d = x7: "+sx7)
  print("------------------------")
  print("Slater-Type Orbitals of S")
  print("set parameters, y1s = x8: "+sx8)
  print("set parameters, y2s = x9: "+sx9)
  print("set parameters, y3s = x10: "+sx10)
  print("------------------------")
  print("Slater-Type Orbitals of P")
  print("set parameters, y1p = x11: "+sx11)
  print("set parameters, y2p = x12: "+sx12)
  print("set parameters, y3p = x13: "+sx13)
  print("------------------------")
  print("Slater-Type Orbitals of D")
  print("set parameters, y1d = x14: "+sx14)
  print("set parameters, y2d = x15: "+sx15)
  print("set parameters, y3d = x16: "+sx16)
  print("------------------------")
  subprocess.run("echo No."+str(count)+": "+str(etav)
    +", "+sx0+", "+sx1 # Density
    +", "+sx2+", "+sx3 # S orbital
    +", "+sx4+", "+sx5 # P orbital
    +", "+sx6+", "+sx7 # D orbital
    +", "+sx8+", "+sx9+", "+sx10   # Slater-Type Orbitals of S
    +", "+sx11+", "+sx12+", "+sx13 # Slater-Type Orbitals of P
    +", "+sx14+", "+sx15+", "+sx16 # Slater-Type Orbitals of D
    +", "+str(sdtv)+", "+str(sdtv3kbt) # Evaluate values
    +" >> Evalute.txt", shell=True)

  # Be sure to add "," after return.
  return y,
#----------------------------------------------------------------------
# fitting parameters
#----------------------------------------------------------------------
def cxTwoPointCopy(ind1, ind2):
  size = len(ind1)
  cxpoint1 = random.randint(1, size)
  cxpoint2 = random.randint(1, size-1)
  if (cxpoint2 >= cxpoint1):
    cxpoint2 += 1
  else:
    cxpoint1, cxpoint2 = cxpoint2, cxpoint1

  ind1[cxpoint1:cxpoint2], ind2[cxpoint2:cxpoint2] = ind2[cxpoint1:cxpoint2].copy(), ind1[cxpoint1:cxpoint2].copy()

  return ind1, ind2
#----------------------------------------------------------------------
def mutUniformDbl(individual, min_ind, max_ind, indpb):
  size = len(individual)
  for i, min, max in zip(xrange(size), min_ind, max_ind):
    if (random.random() < indpb):
      individual[i] = random.uniform(min, max)
  return indivisual,
#----------------------------------------------------------------------
# Setting the function you want to evaluate (objective function)
toolbox.register("evaluate", evalOneMax)
#-------------------------------
# Crossover function settings. Adopts a method called blend crossover
toolbox.register("mate", tools.cxTwoPoint)
#-------------------------------
# Setting up the mutation function. indpb is the probability that each gene will mutate. 
# mu and sigma are the mean and standard deviation of the mutations. (e.g., 0.01, 0.05)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
#-------------------------------
# Select parents who will leave children to the next generation using a tournament method
# (tornsize is the number of individuals participating in each tournament)
toolbox.register("select", tools.selTournament, tournsize=3)
#----------------------------------------------------------------------
def main():
  random.seed(64) # Setting random numbers (fixing random numbers)
  pop = toolbox.population(n=50) # Number of individuals in the population
  hof = tools.HallOfFame(1, similar=np.array_equal)
  stats = tools.Statistics(lambda ind: ind.fitness.values)
  stats.register("avg", np.mean)
  stats.register("std", np.std)
  stats.register("min", np.min)
  stats.register("max", np.max)
  # Adopting the simplest evolution strategy called Simple GA
  algorithms.eaSimple(pop, toolbox, 
    cxpb=0.6,    # crossover probability (e.g, 0.6, 0.5-0.9)
    mutpb=0.005, # probability that an individual will mutate (e.g, 0.005, 0.1-0.2)
    ngen=500,    # Number of generations
    stats=stats, halloffame=hof)
  return pop, stats, hof
#----------------------------------------------------------------------
if (__name__ == "__main__"):
  main()
#----------------------------------------------------------------------

# Select the best individual from the final population (pop)
best_ind = tools.selBest(pop, 1)[0]

# Show results
print("The best individual is %s, the value of the objective function at that time is %s" % (best_ind, best_ind.fitness.values))
#----------------------------------------------------------------------
subprocess.run("sort -k 2 Evalute.txt > Evalute_sort.txt", shell=True)