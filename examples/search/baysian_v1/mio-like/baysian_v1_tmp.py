#----------------------------------------------------------------------
from bayes_opt import BayesianOptimization
#from bayes_opt import UtilityFunction # for ucb
#-----------------------------------------------
# Saving progress
from bayes_opt.logger import JSONLogger
from bayes_opt.event import Events
# Loading progress
from bayes_opt.util import load_logs
#-----------------------------------------------
# Sequential Domain Reduction
from bayes_opt import SequentialDomainReductionTransformer
#-----------------------------------------------
import numpy as np
import subprocess
import sys
import os
import datetime # for results folder
#----------------------------------------------------------------------
# Usage: command:
# 1. pip3 install bayesian-optimization==1.4.3
# 2. rewrite skdef.hsd.tmp_baysian and prepare band_check folder (e.g., see Mg folder)
# 3. rewrite initial parameters and boundaries in this file
# 4. python3 baysian_v1.py
#----------------------------------------------------------------------
file_tmp = 'skdef.hsd.tmp_baysian'
file_inp = 'skdef.hsd'
file_msd = 'msd.dat'

#cif2cell_adress = "cif2cell"

subprocess.run("export OMP_NUM_THREADS=1", shell=True)
sub_num_core = subprocess.run("grep 'core id' /proc/cpuinfo | sort -u | wc -l", shell=True, stdout=subprocess.PIPE)
print("CPU: ",str(sub_num_core.stdout).lstrip("b'").rstrip("\\n'"))
num_core = int(str(sub_num_core.stdout).lstrip("b'").rstrip("\\n'"))
dftbp_adress = "mpirun -np "+str(num_core)+" dftb+"
#skprogs_adress = "/home/user/skprogs-v.0.2.1/sktools/src/sktools/scripts/skgen.py" # Linux
#skprogs_adress = "/home/inukai/skprogs/sktools/src/sktools/scripts/skgen.py" # Linux
skprogs_adress = "/home/inukai/skprogs/sktools/src/sktools/scripts/skgen.py" # Linux
#skprogs_adress = "/mnt/d/skprogs-v.0.2.1/sktools/src/sktools/scripts/skgen.py" # WSL2
#
#pwscf_adress = "mpirun -np "+str(num_core)+" pw.x"

#----------------------------------------------------------------------
# set initial parameters and boundaries
#----------------------------------------------------------------------
element = "element_Xx"
atomic_number = atomic_number_Yy # In this code, this value is used as a parameter of the radial wave function.
#---------------------------

#------------------------------------------------
# Note: Empirically, setting a value around 0.3 will significantly reduce the number of failures.
#---------------------------
hwb_den = 10.0 # search range [-x*hwb:+x*hwt]
hwt_den = 14.0 # search range [-x*hwb:+x*hwt]
#---------------------------
hwb_wav = (2/3) # search range [-x*hwb:+x*hwt]
hwt_wav = (4/3) # search range [-x*hwb:+x*hwt]
#---------------------------
x0  = x0_Zz # r0 of density
x1  = x1_Zz # r0 of S, P, D and F
#---------------------------
print("------------------------")
print("initial parameters:   x0  x1")
print("initial parameters: ",x0,x1)
x = [x0,x1]
#------------------------------------------------

#------------------------------------------------
n_gene = 2 # number of parameters, number of individual +1
min_ind = np.ones(n_gene) * -1.0
max_ind = np.ones(n_gene) *  1.0
#---------------------------
# sigma of density
min_ind[0] = float(x0) - hwb_den
max_ind[0] = float(x0) + hwt_den
#---------------------------
# r0 of density
min_ind[1] = float(x1)*hwb_wav
max_ind[1] = float(x1)*hwt_wav
#---------------------------
if min_ind[0] < 2.0:
  min_ind[0] = 2.0
if min_ind[1] < 2.0:
  min_ind[1] = 2.0
#---------------------------
pbounds = {
   'x0': (float(min_ind[0]),float(max_ind[0])),
   'x1': (float(min_ind[1]),float(max_ind[1]))
}# boundary
print("------------------------")
print("boundary of parameters: ",pbounds)
print("------------------------")
#------------------------------------------------

#------------------------------------------------
if os.path.exists("./Evalute.txt"):
  subprocess.run("cd ./"+element+" ; cp ./../Evalute.txt ./results/Evalute.txt ; cd ../", shell=True)
  subprocess.run("cd ./"+element+" ; cp ./../Evalute_sort.txt ./results/Evalute_sort.txt ; cd ../", shell=True)
  subprocess.run("cd ./"+element+" ; cp ./../logs.json ./results/logs.json ; cd ../", shell=True)
  now = datetime.datetime.now()
  subprocess.run("cd ./"+element+" ; mv results results_{0:%Y%m%d-%H%M%S}".format(now)+" ; cd ../", shell=True)
subprocess.run("cd ./"+element+" ; mkdir results ; cd ../", shell=True)
subprocess.run("cd ./"+element+" ; chmod +x *.sh ; cd ../", shell=True)
#-------------------------------
subprocess.run("echo \"#No.: ETA [eV], r0_den, r0_wav,"
  +" sdt, sdt3kbt"
  +" \" > Evalute.txt", shell=True)
subprocess.run("echo \"#| iter | 1/target | x0 | x1 | x2 |  SDT | SDT(3kbT) |\" >> Evalute.txt", shell=True)
#------------------------------------------------

#------------------------------------------------
# set initial values
etav = 0.0
stdv = 0.0
stdv3kbt = 0.0
#------------------------------------------------

count = 0
#----------------------------------------------------------------------
def descripter(x0,x1): # mio
  
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
  # I realized later that {:.f} rounds it up. On the other hand, int() is truncated.
  #-------------------------------
  fine_step = "yes"
  if fine_step == "no": # 0.2 step for sigma.
    print("0.2 step for sigma")
    #-------------------------------
    # Density
    #--------- 0.1 step
    sx0  = "{:.1f}".format(x0+R1)
    #-------------------------------
    # S, P, D and F orbitals
    #--------- 0.1 step
    sx1  = "{:.1f}".format(x1+R1)
    #-------------------------------
  else:
    print("sigma and r0: 0.1 step")
    #-------------------------------
    # Density
    sx0  = "{:.1f}".format(x0+R1)
    #-------------------------------
    # S, P, D and F orbitals
    sx1  = "{:.1f}".format(x1+R1)
  #-------------------------------
  
  #-------------------------------
  # Sigma
  sigma_value = 2
  subprocess.call("sed -i s/sigma/"+str(sigma_value)+"/g "+file_inp, shell=True)
  #-------------------------------
  # Density
  subprocess.call("sed -i s/r0_den/"+sx0+"/g "+file_inp, shell=True)
  #-------------------------------
  # S, P, D and F orbitals
  subprocess.call("sed -i s/r0_wav/"+sx1+"/g "+file_inp, shell=True)
  #-------------------------------
  
  subprocess.run("export OMP_NUM_THREADS="+str(num_core), shell=True)
  skgen = subprocess.run("python3 "+str(skprogs_adress)+" -o slateratom -t sktwocnt sktable -d "+element+" "+element, shell=True, stdout=subprocess.PIPE)
  subprocess.run("export OMP_NUM_THREADS=1", shell=True)
  
  if os.path.exists(element+"-"+element+".skf"):
    subprocess.run("mv ./"+element+"-"+element+".skf ./"+element+"/"+element+"-"+element+".skf", shell=True)
    if os.path.exists("./"+element+"/run_v2.sh"):
      subprocess.run("cd ./"+element+" ; ./run_v2.sh ; cd ../", shell=True)
    else:
      subprocess.run("cd ./"+element+" ; ./run.sh ; cd ../", shell=True)
    evaluate = subprocess.run("awk '{if(NR==10){printf \"%s\",$3}}' ./"+element+"/"+file_msd, shell=True, stdout=subprocess.PIPE)
    evaluate_sdt = subprocess.run("awk '{if(NR==4){printf \"%s\",$3}}' ./"+element+"/"+file_msd, shell=True, stdout=subprocess.PIPE)
    evaluate_sdt3kbt = subprocess.run("awk '{if(NR==8){printf \"%s\",$3}}' ./"+element+"/"+file_msd, shell=True, stdout=subprocess.PIPE)
    if evaluate.returncode == 0:
      try:
        etav = float(str(evaluate.stdout).lstrip("b'").rstrip("\\n'"))
        sdtv = float(str(evaluate_sdt.stdout).lstrip("b'").rstrip("\\n'"))
        sdtv3kbt = float(str(evaluate_sdt3kbt.stdout).lstrip("b'").rstrip("\\n'"))
        subprocess.run("mv "+file_inp+" ./"+element+"/results/"+file_inp+"_No"+str(count), shell=True)
        subprocess.run("cp ./"+element+"/comp_band.png ./"+element+"/results/comp_band_No"+str(count)+".png", shell=True)
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
  
  y = 1.0/etav
  
  print("------------------------")
  print("iter:",count)
  print("------------------------")
  print("target:",str(y))
  print("------------------------")
  print("Density")
  print("set parameters, r0_den = x1: "+sx0)
  print("------------------------")
  print("S, P, D and F orbital")
  print("set parameters, r0_wav = x3: "+sx1)
  print("------------------------")
  print("Next values")
  print("| iter | target | x0 | x1 |")
  subprocess.run("echo No."+str(count)+": "+str(etav)
    +", "+sx0 # Density
    +", "+sx1 # S, P, D and F orbitals
    +", "+str(sdtv)+", "+str(sdtv3kbt) # Evaluate values
    +" >> Evalute.txt", shell=True)

  return y
#----------------------------------------------------------------------
# fitting parameters
#-------------------
# Note
#gamma_osc: 0.5-0.7: shrinkage parameter for oscillation. Typically [0.5-0.7]. Default = 0.7
#gamma_pan: panning parameter. Typically 1.0. Default = 1.0
#eta: zoom parameter. Default = 0.9
#minimum_window: Default = 0.0
bounds_transformer = SequentialDomainReductionTransformer(gamma_osc=0.7, gamma_pan=1.0, eta=0.9, minimum_window=0.0)
#-------------------
if os.path.exists("./logs.json"):
  print("# New optimizer is loaded with previously seen points")
  print("If you want to search without using past data, please delete logs.json.")
  new_optimizer = BayesianOptimization(f=descripter, pbounds=pbounds, verbose=2, random_state=7, bounds_transformer=bounds_transformer, allow_duplicate_points=True)
  load_logs(new_optimizer, logs=["./logs.json"]);
  logger = JSONLogger(path="./logs", reset=False) # Results will be saved in ./logs.json
  new_optimizer.subscribe(Events.OPTIMIZATION_STEP, logger)
  new_optimizer.maximize(init_points=11, n_iter=(300*1)) # 300 cycle / 6 h
  new_optimizer.set_gp_params(alpha=1e-3) # The greater the whitenoise, the greater alpha value.
else:
  #optimizer = BayesianOptimization(f=descripter, pbounds=pbounds, verbose=2, random_state=1, bounds_transformer=bounds_transformer, allow_duplicate_points=True)
  optimizer = BayesianOptimization(f=descripter, pbounds=pbounds, verbose=2, random_state=1, bounds_transformer=bounds_transformer)
  logger = JSONLogger(path="./logs") # Results will be saved in ./logs.json
  optimizer.subscribe(Events.OPTIMIZATION_STEP, logger)
  optimizer.maximize(init_points=(n_gene*50), n_iter=(300*1)) # 600 cycles / 12 h (Note: It depends on the number of parameters and search range, but usually around 150 times is a good value (in n_gene*5 case). I set it to 600 just in case (from after I got home until the next morning).)
  optimizer.set_gp_params(alpha=1e-3) # The greater the whitenoise, the greater alpha value.
  # Note: Since "bounds_transformer" is used to narrow the search area, 
  #  in order to initially search as wide a range as possible, 
  #  the initial random number search (init_points) is set to the number of parameters * 5 (= n_gene * 5). 
  #  It will take more time, but if you want to be more elaborate, increase the value from 5 to a higher value such as 7 or 9.
  #  Of course, it is also a good idea to expand the initial search range.
#--------------------------------------------------------
#------------------ for ucb -----------------------------
#utility = UtilityFunction(kind="ucb", kappa=2.5, xi=0.0)
#next_point = optimizer.suggest(utility)
#print("Next point to probe is:", next_point)
#target = descripter(**next_point)
#print("Found the target value to be:", target)
#optimizer.register(params=next_point, target=target)
#--------------------------------------------------------
# old version 1.1.0
#optimizer.maximize(init_points=3, n_iter=2000, acq="ucb")
#acq = ucb, ei, poi, (default: ubc)
#----------------------------------------------------------------------
subprocess.run("sort -k 2 Evalute.txt > Evalute_sort.txt", shell=True)
#subprocess.run("mv Evalute_sort.txt ./"+element+"/Evalute_sort.txt", shell=True)
