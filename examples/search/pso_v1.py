#----------------------------------------------------------------------
# Import PySwarms
import pyswarms as ps
#-----------------------------------------------
# Random search case
from pyswarms.utils.search import RandomSearch
#-----------------------------------------------
# Grid search case
#from pyswarms.utils.search import GridSearch
#-----------------------------------------------
import numpy as np # Import modules
import subprocess
import sys
import os
import datetime # for results folder
#----------------------------------------------------------------------
# Usage: command:
# 1. pip3 install pyswarms==1.3.0
# 2. rewrite skdef.hsd.tmp_pso and prepare band_check folder (e.g., see Mg folder)
# 3. rewrite initial parameters and boundaries in this file
# 4. python3 pso_v1.py
#----------------------------------------------------------------------
file_tmp = 'skdef.hsd.tmp_pso'
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
hwb  =  0.37 # search range [-x*hwb:+x*hwt]
hwt  =  0.37 # search range [-x*hwb:+x*hwt]
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
x0c  =  7.0 # sigma of density
x1c  = 14.0 # r0 of density
#---------------------------
x2c  =  7.0 # simga of S
x3c  =  6.3 # r0 of S
#---------------------------
x4c  =  7.0 # simga of P
x5c  =  7.2 # r0 of P
#---------------------------
x6c  =  7.0 # simga of D
x7c  =  7.2 # r0 of D
#---------------------------
x8c  =  4.56 # y1 of S
x9c  = 10.39 # y2 of S
x10c = 23.69 # y3 of S
#---------------------------
x11c =  4.56 # y1 of P
x12c = 10.39 # y2 of P
x13c = 23.69 # y3 of P
#---------------------------
x14c =  6.22 # y1 of D or D
x15c = 14.69 # y2 of D or D
x16c = 35.09 # y3 of D or D
#---------------------------
print("------------------------")
print("initial parameters:   x0c  x1c  x2c  x3c  x4c  x5c  x6c  x7c   x8c   x9c"
  +"  x10c  x11c  x12c  x13c  x14c  x15c  x16c")
print("initial parameters: ",x0c,x1c,x2c,x3c,x4c,x5c,x6c,x7c,x8c,x9c,x10c,x11c,x12c,x13c,x14c,x15c,x16c)
#------------------------------------------------

#------------------------------------------------
n_gene = 17 # number of parameters, number of individual +1
min_ind = np.ones(n_gene) * -1.0
max_ind = np.ones(n_gene) *  1.0
#---------------------------
# sigma of density
min_ind[0] = float(x0c) - float(x0c)*hwb
max_ind[0] = float(x0c) + float(x0c)*hwt
#min_ind[0] =  2.0; max_ind[0] = 17.0
#---------------------------
# r0 of density
min_ind[1] = float(x1c) - float(x1c)*hwb
max_ind[1] = float(x1c) + float(x1c)*hwt
#min_ind[1] =  2.4; max_ind[1] = 29.0
#---------------------------
# sigma of S orbitals
min_ind[2] = float(x2c) - float(x2c)*hwb
max_ind[2] = float(x2c) + float(x2c)*hwt
#min_ind[2] =  2.0; max_ind[2] = 17.0
#---------------------------
# r0 of S orbitals
min_ind[3] = float(x3c) - float(x3c)*hwb
max_ind[3] = float(x3c) + float(x3c)*hwt
#min_ind[3] =  2.4; max_ind[3] = 29.0
#---------------------------
# sigma of P orbitals
min_ind[4] = float(x4c) - float(x4c)*hwb
max_ind[4] = float(x4c) + float(x4c)*hwt
#min_ind[4] =  2.0; max_ind[4] = 17.0
#---------------------------
# r0 of P orbitals
min_ind[5] = float(x5c) - float(x5c)*hwb
max_ind[5] = float(x5c) + float(x5c)*hwt
#min_ind[5] =  2.4; max_ind[5] = 29.0
#---------------------------
# sigma of D orbitals
min_ind[6] = float(x6c) - float(x6c)*hwb
max_ind[6] = float(x6c) + float(x6c)*hwt
#min_ind[6] =  2.0; max_ind[6] = 17.0
#---------------------------
# r0 of D orbitals
min_ind[7] = float(x7c) - float(x7c)*hwb
max_ind[7] = float(x7c) + float(x7c)*hwt
#min_ind[7] =  2.4; max_ind[7] = 29.0
#---------------------------
# Slater-Type Orbitals of S: y1
min_ind[8] = float(x8c) - float(x8c)*hwb
max_ind[8] = float(x8c) + float(x8c)*hwt
#---------------------------
# Slater-Type Orbitals of S: y2
min_ind[9] = float(x9c) - float(x9c)*hwb
max_ind[9] = float(x9c) + float(x9c)*hwt
#---------------------------
# Slater-Type Orbitals of S: y3
min_ind[10] = float(x10c) - float(x10c)*hwb
max_ind[10] = float(x10c) + float(x10c)*hwt
#---------------------------
# Slater-Type Orbitals of P: y1
min_ind[11] = float(x11c) - float(x11c)*hwb
max_ind[11] = float(x11c) + float(x11c)*hwt
#---------------------------
# Slater-Type Orbitals of P: y2
min_ind[12] = float(x12c) - float(x12c)*hwb
max_ind[12] = float(x12c) + float(x12c)*hwt
#---------------------------
# Slater-Type Orbitals of P: y3
min_ind[13] = float(x13c) - float(x13c)*hwb
max_ind[13] = float(x13c) + float(x13c)*hwt
#---------------------------
# Slater-Type Orbitals of D: y1
min_ind[14] = float(x14c) - float(x14c)*hwb
max_ind[14] = float(x14c) + float(x14c)*hwt
#---------------------------
# Slater-Type Orbitals of D: y2
min_ind[15] = float(x15c) - float(x15c)*hwb
max_ind[15] = float(x15c) + float(x15c)*hwt
#---------------------------
# Slater-Type Orbitals of D: y3
min_ind[16] = float(x16c) - float(x16c)*hwb
max_ind[16] = float(x16c) + float(x16c)*hwt
#---------------------------
pbounds = {
  # min
  ( float(min_ind[0]),  float(min_ind[1]), # density: sigma (x0), r0 (x1)
    float(min_ind[2]),  float(min_ind[3]), # S: sigma (x2), r0 (x3)
    float(min_ind[4]),  float(min_ind[5]), # P: sigma (x4), r0 (x5)
    float(min_ind[6]),  float(min_ind[7]), # D: sigma (x6), r0 (x7)
    float(min_ind[8]),  float(min_ind[9]),  float(min_ind[10]), # S (STO): y1s(x8),  y2s(x9),  y3s(x10)
    float(min_ind[11]), float(min_ind[12]), float(min_ind[13]), # P (STO): y1p(x11), y2p(x12), y3p(x13)
    float(min_ind[14]), float(min_ind[15]), float(min_ind[16])),# D (STO): y1d(x14), y2d(x15), y3d(x16)
  # max
  ( float(max_ind[0]),  float(max_ind[1]), # density: sigma (x0), r0 (x1)
    float(max_ind[2]),  float(max_ind[3]), # S: sigma (x2), r0 (x3)
    float(max_ind[4]),  float(max_ind[5]), # P: sigma (x4), r0 (x5)
    float(max_ind[6]),  float(max_ind[7]), # D: sigma (x6), r0 (x7)
    float(max_ind[8]),  float(max_ind[9]),  float(max_ind[10]), # S (STO): y1s(x8),  y2s(x9),  y3s(x10)
    float(max_ind[11]), float(max_ind[12]), float(max_ind[13]), # P (STO): y1p(x11), y2p(x12), y3p(x13)
    float(max_ind[14]), float(max_ind[15]), float(max_ind[16])) # D (STO): y1d(x14), y2d(x15), y3d(x16)
  }# boundary
print("------------------------")
print("boundary of parameters: ",pbounds)
print("------------------------")
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
def descripter(x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16):
  
  print("------------------------")
  global count
  count += 1
  print(count)
  
  nop = len(x0)
  print("n_particles =",nop)
  y = np.zeros(nop)
  
  for i in range(nop):
    print("------------------------")
    print("now_particles = ",i)
  
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
    sx0  = "{:.1f}".format(x0[i]+R1)
    sx1  = "{:.1f}".format(x1[i]+R1)
    #-------------------------------
    # S orbital
    sx2  = "{:.1f}".format(x2[i]+R1)
    sx3  = "{:.1f}".format(x3[i]+R1)
    #-------------------------------
    # P orbital
    sx4  = "{:.1f}".format(x4[i]+R1)
    sx5  = "{:.1f}".format(x5[i]+R1)
    #-------------------------------
    # D orbital
    sx6  = "{:.1f}".format(x6[i]+R1)
    sx7  = "{:.1f}".format(x7[i]+R1)
    #-------------------------------
    # Slater-Type Orbitals of S
    sx8  = "{:.2f}".format(x8[i]+R2)
    sx9  = "{:.2f}".format(x9[i]+R2)
    sx10 = "{:.2f}".format(x10[i]+R2)
    #-------------------------------
    # Slater-Type Orbitals of P
    sx11 = "{:.2f}".format(x11[i]+R2)
    sx12 = "{:.2f}".format(x12[i]+R2)
    sx13 = "{:.2f}".format(x13[i]+R2)
    #-------------------------------
    # Slater-Type Orbitals of D
    sx14 = "{:.2f}".format(x14[i]+R2)
    sx15 = "{:.2f}".format(x15[i]+R2)
    sx16 = "{:.2f}".format(x16[i]+R2)
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
          subprocess.run("mv "+file_inp+" ./"+element+"/results/"+file_inp+"_No"+str(count)+"-"+str(i), shell=True)
          subprocess.run("cp ./"+element+"/comp_band.png ./"+element+"/results/comp_band_No"+str(count)+"-"+str(i)+".png", shell=True)
        except ValueError as error:
          etav = 9.999
          sdtv = 9.999
          sdtv3kbt = 9.999
      else:
        etav = 9.999
        sdtv = 9.999
        sdtv3kbt = 9.999
    else:
      etav = 9.999
      sdtv = 9.999
      sdtv3kbt = 9.999

    print("------------------------")
    print("iter:",count," - ",i)
    print("------------------------")
    print("target:",etav)
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
    subprocess.run("echo No."+str(count)+"-"+str(i)+": "+str(etav)
      +", "+sx0+", "+sx1 # Density
      +", "+sx2+", "+sx3 # S orbital
      +", "+sx4+", "+sx5 # P orbital
      +", "+sx6+", "+sx7 # D orbital
      +", "+sx8+", "+sx9+", "+sx10   # Slater-Type Orbitals of S
      +", "+sx11+", "+sx12+", "+sx13 # Slater-Type Orbitals of P
      +", "+sx14+", "+sx15+", "+sx16 # Slater-Type Orbitals of D
      +", "+str(sdtv)+", "+str(sdtv3kbt) # Evaluate values
      +" >> Evalute.txt", shell=True)
    y[i] = etav

  return y
#----------------------------------------------------------------------
# fitting parameters
#-------------------
def descripter_pso(x):
  return descripter(x[:,0], x[:,1], x[:,2], x[:,3], x[:,4], x[:,5], x[:,6], x[:,7], x[:,8], x[:,9], 
    x[:,10], x[:,11], x[:,12], x[:,13], x[:,14], x[:,15], x[:,16])
#-------------------
# Fix random value for test
#np.random.seed(0)
#----------------------------------------------------------------------
random_search="yes"
#----------------------------------------------------------------------
if random_search=="yes" :
  #-------------------------------
  # Random search case
  print("Random search: ", random_search)
  # Set-up choices for the parameters
  options = { 'c1': (0.2,0.8), 'c2': (0.3,0.6), 'w': (0.5,1.0), 'k': (1,3), 'p': (1,3) }
  #-------------------------------
  # Create a RandomSearch object
  # n_selection_iters is the number of iterations to run the searcher
  # iters is the number of iterations to run the optimizer
  g = RandomSearch(ps.single.LocalBestPSO, n_particles=24,
    dimensions=(n_gene), options=options, objective_func=descripter_pso,bounds=pbounds,
    iters=10, n_selection_iters=100)
  best_score, best_options = g.search()
  #-------------------------------
  # Show optimized values
  print("best score: ", best_score)
  print("c1 = ", best_options['c1'])
  print("c2 = ", best_options['c2'])
  print(" w = ", best_options['w'])
  print(" k = ", best_options['k'])
  print(" p = ", best_options['p'])
  #-------------------------------
else:
  #-------------------------------
  # Initialize swarm
  options = {'c1': 0.5, 'c2': 0.3, 'w':0.9, 'k': 2, 'p': 2}
  # c1=weight of local, c2=weight of global, w=inertia term (0.0-1.0)
  #------------------------------------------------------------------
  # The PySwarms hyperparameters is a parameter in the Particle Swarm Optimization (PSO) algorithm that 
  #   is a factor by which the difference between the current velocity and the global best position is multiplied when 
  #   updating the particle velocity1. The larger this value, the more the particle velocity changes and 
  #   the wider the search range. On the other hand, if you set it to a small value,
  #   the search range becomes narrower and you are more likely to fall into a local solution.
  #------------------------------------------------------------------
  
  # Call instance of PSO with bounds argument
  optimizer = ps.single.GlobalBestPSO(n_particles=24,
    dimensions=(n_gene),options=options,bounds=pbounds)
  
  # Perform optimization
  cost, pos = optimizer.optimize(objective_func=descripter_pso, iters=600)
  #-------------------------------
  # Obtain the cost history
  optimizer.cost_history
  # Obtain the position history
  optimizer.pos_history
  # Obtain the velocity history
  optimizer.velocity_history
  #-------------------------------
  optimizer.mean_pbest_history
  optimizer.mean_neighbor_history
  #-------------------------------
  # Show optimized values
  print("cost: ", cost)
  # Show optimized coordinaties
  print("position:", pos)
  #-------------------------------
  #----------------------------------------------------------------------
  # Memo: Grid search case
  #options = {"c1": [0.3, 0.5, 0.8], "c2": [0.3, 0.5, 0.8], "w": [0.2, 0.3, 0.5]}
  #g_search = GridSearch(ps.single.GlobalBestPSO, n_particles=30,dimensions=(n_gene),
  #  options=options,objective_func=descripter,iters=200)
  #best_score, best_options = g_search.search()
  #----------------------------------------------------------------------
#----------------------------------------------------------------------
subprocess.run("sort -k 2 Evalute.txt > Evalute_sort.txt", shell=True)