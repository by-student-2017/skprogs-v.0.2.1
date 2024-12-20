import numpy as np
from scipy.optimize import minimize
import subprocess
import sys
#----------------------------------------------------------------------
# command: python3 nm_r0_v1.py
#----------------------------------------------------------------------
file_tmp = 'skdef.hsd.tmp_sto'
file_inp = 'skdef.hsd'
file_msd = 'msd.dat'

#cif2cell_adress = "cif2cell"

subprocess.run("export OMP_NUM_THREADS=1", shell=True)
num_core = subprocess.run("grep 'core id' /proc/cpuinfo | sort -u | wc -l", shell=True, stdout=subprocess.PIPE)
print("CPU: ",str(num_core.stdout).lstrip("b'").rstrip("\\n'"))
dftbp_adress = "mpirun -np "+str(num_core)+" dftb+"
pwscf_adress = "mpirun -np "+str(num_core)+" pw.x"

subprocess.run("echo \"No.: ETA value [eV]\" > Evalute.txt", shell=True)

#natom = 1
#r0 = numpy.ones(int(natom)+1)

#----------------------------------------------------------------------
# fitting parameters
element = "B"
#------------------------
spt = 1.0
dt  = 1.0
stosp = [0.5,0.95,2.62,6.0]
stod  = [0.5,0.95,2.62,6.0]
#------------------------
area=[
  (0.8,1.5),
  (0.8,1.5)
]
#------------------------
print("initial parameters, SP: "+str(stosp))
print("initial parameters, D : "+str(stod))
x0 = np.array([spt,dt])

subprocess.run("cd ./"+str(element)+" ; rm -f -r results ; cd ../", shell=True)
subprocess.run("cd ./"+str(element)+" ; mkdir results ; cd ../", shell=True)

count = 0
#----------------------------------------------------------------------
def f(x):
  
  print("------------------------")
  global count
  count += 1
  print(count)
  
  subprocess.run("cp "+" "+str(file_tmp)+" "+str(file_inp), shell=True)
  
  stos_all = str(stosp[0]*spt)+" "+str(stosp[1]*spt)+" "+str(stosp[2]*spt)+" "+str(stosp[3]*spt)
  stop_all = str(stod[0]*dt)+" "+str(stod[1]*dt)+" "+str(stod[2]*dt)+" "+str(stod[3]*dt)
  subprocess.call("sed -i s/stosp/\""+str(stos_all)+"\"/g "+str(file_inp), shell=True)
  subprocess.call("sed -i s/stod/\""+str(stop_all)+"\"/g "+str(file_inp), shell=True)
  
  sub = subprocess.run("/mnt/d/skprogs/sktools/src/sktools/scripts/skgen.py -o slateratom -t sktwocnt sktable -d "+str(element)+" "+str(element), shell=True)
  
  subprocess.run("cd ./"+str(element)+" ; ./run.sh ; cd ../", shell=True)
  
  evaluate = subprocess.run("awk '{if(NR==10){printf \"%s\",$3}}' ./"+str(element)+"/"+str(file_msd), shell=True, stdout=subprocess.PIPE)
  if evaluate.returncode == 0:
    y = float(str(evaluate.stdout).lstrip("b'").rstrip("\\n'"))
  else:
    y = 99999.999
  
  print("Evaluate: ",str(y))
  print("Parameters: x0 = "+"[ "+str(x[0])+","+str(x[1])+" ]")
  print("------------------------")
  subprocess.run("mv "+str(file_inp)+" ./"+str(element)+"/results/"+str(file_inp)+"_No"+str(count), shell=True)
  subprocess.run("cp ./"+str(element)+"/comp_band.png ./"+str(element)+"/results/comp_band_No"+str(count)+".png", shell=True)
  subprocess.run("echo No."+str(count)+": "+str(y)+" >> Evalute.txt", shell=True)

  return y
#----------------------------------------------------------------------
res = minimize(f,x0,bounds=area,method='Nelder-Mead',options={'adaptive':True})
#res = minimize(f,x0,method='Nelder-Mead')
#res = minimize(f,x0,method='TNC')
#res = minimize(f,x0,method='Powell')
#res = minimize(f,x0,method='BFGS')
