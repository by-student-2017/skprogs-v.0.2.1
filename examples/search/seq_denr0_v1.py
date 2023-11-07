import numpy as np
from scipy.optimize import minimize
import subprocess
import sys
import os
#----------------------------------------------------------------------
# command: python3 seq_denr0_v1.py
#----------------------------------------------------------------------
file_tmp = 'skdef.hsd.tmp_denr0'
file_inp = 'skdef.hsd'
file_msd = 'msd.dat'

#cif2cell_adress = "cif2cell"

subprocess.run("export OMP_NUM_THREADS=1", shell=True)
num_core = subprocess.run("grep 'core id' /proc/cpuinfo | sort -u | wc -l", shell=True, stdout=subprocess.PIPE)
print("CPU: ",str(num_core.stdout).lstrip("b'").rstrip("\\n'"))
dftbp_adress = "mpirun -np "+str(num_core)+" dftb+"
#pwscf_adress = "mpirun -np "+str(num_core)+" pw.x"

subprocess.run("echo \"#No.: ETA value [eV], r0, sigma\" > Evalute.txt", shell=True)

#----------------------------------------------------------------------
element = "B"

subprocess.run("cd ./"+str(element)+" ; rm -f -r results ; cd ../", shell=True)
subprocess.run("cd ./"+str(element)+" ; mkdir results ; cd ../", shell=True)

count = 0
#----------------------------------------------------------------------
def f(r0,sigma):
  
  print("------------------------")
  global count
  count += 1
  print(count)
  
  subprocess.run("rm *-*.skf", shell=True)
  
  subprocess.run("cp "+" "+str(file_tmp)+" "+str(file_inp), shell=True)
  
  subprocess.call("sed -i s/r0/"+str(r0)+"/g "+str(file_inp), shell=True)
  subprocess.call("sed -i s/sigma/"+str(sigma)+"/g "+str(file_inp), shell=True)
  
  subprocess.run("export OMP_NUM_THREADS="+str(num_core), shell=True)
  skgen = subprocess.run("/mnt/d/skprogs/sktools/src/sktools/scripts/skgen.py -o slateratom -t sktwocnt sktable -d "+str(element)+" "+str(element), shell=True, stdout=subprocess.PIPE)
  subprocess.run("export OMP_NUM_THREADS=1", shell=True)
  
  if os.path.exists(str(element)+"-"+str(element)+".skf"):
    subprocess.run("cd ./"+str(element)+" ; ./run.sh ; cd ../", shell=True)
    evaluate = subprocess.run("awk '{if(NR==10){printf \"%s\",$3}}' ./"+str(element)+"/"+str(file_msd), shell=True, stdout=subprocess.PIPE)
    if evaluate.returncode == 0:
      y = float(str(evaluate.stdout).lstrip("b'").rstrip("\\n'"))
      subprocess.run("mv "+str(file_inp)+" ./"+str(element)+"/results/"+str(file_inp)+"_No"+str(count), shell=True)
      subprocess.run("cp ./"+str(element)+"/comp_band.png ./"+str(element)+"/results/comp_band_No"+str(count)+".png", shell=True)
    else:
      y = 99999.999
  else:
    y = 99999.999
  
  print("Evaluate: ",str(y))
  print("Parameters: "+"[ "+str(r0)+","+str(sigma)+" ]")
  print("------------------------")
  subprocess.run("echo No."+str(count)+": "+str(y)+", "+str(r0)+", "+str(sigma)+" >> Evalute.txt", shell=True)

  return y
#----------------------------------------------------------------------
# fitting parameters
for sigma in np.arange(2.0,20.0,1.0):
  for r0 in np.arange(6.0,40.0,1.0): # [bohr] unit
    print("initial parameters, r0: "+str(r0))
    print("initial parameters, sigma: "+str(sigma))
    res = f(r0,sigma)
  subprocess.run("echo \"\" >> Evalute.txt", shell=True)
#----------------------------------------------------------------------
