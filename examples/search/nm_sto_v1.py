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
st = 1.0
pt = 1.0
stos = [0.5,0.95,2.62,6.0]
stop = stos
#------------------------
area=[
  (0.8,1.5),
  (0.8,1.5)
]
#------------------------
print("initial parameters, S: "+str(stos))
print("initial parameters, P: "+str(stop))
x0 = np.array([st,pt])

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
  
  stos_all = str(stos[0]*st)+" "+str(stos[1]*st)+" "+str(stos[2]*st)+" "+str(stos[3]*st)
  stop_all = str(stos[0]*pt)+" "+str(stos[1]*st)+" "+str(stos[2]*st)+" "+str(stos[3]*st)
  subprocess.call("sed -i s/stos/\""+str(stos_all)+"\"/g "+str(file_inp), shell=True)
  subprocess.call("sed -i s/stop/\""+str(stop_all)+"\"/g "+str(file_inp), shell=True)
  
  sub = subprocess.run("/mnt/d/skprogs/sktools/src/sktools/scripts/skgen.py -o slateratom -t sktwocnt sktable -d "+str(element)+" "+str(element), shell=True)
  
  subprocess.run("cd ./"+str(element)+" ; ./run.sh ; cd ../", shell=True)
  
  evaluate = subprocess.run("awk '{if(NR==10){printf \"%s\",$3}}' ./"+str(element)+"/"+str(file_msd), shell=True, stdout=subprocess.PIPE)
  if cp.returncode == 0:
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
