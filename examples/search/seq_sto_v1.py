import numpy as np
import subprocess
import sys
import os
#----------------------------------------------------------------------
# command: python3 seq_sto_v1.py
#----------------------------------------------------------------------
file_tmp = 'skdef.hsd.tmp_sto'
file_inp = 'skdef.hsd'
file_msd = 'msd.dat'

#cif2cell_adress = "cif2cell"

subprocess.run("export OMP_NUM_THREADS=1", shell=True)
sub_num_core = subprocess.run("grep 'core id' /proc/cpuinfo | sort -u | wc -l", shell=True, stdout=subprocess.PIPE)
print("CPU: ",str(sub_num_core.stdout).lstrip("b'").rstrip("\\n'"))
num_core = int(str(sub_num_core.stdout).lstrip("b'").rstrip("\\n'"))
dftbp_adress = "mpirun -np "+str(num_core)+" dftb+"
#pwscf_adress = "mpirun -np "+str(num_core)+" pw.x"

subprocess.run("echo \"#No.: ETA value [eV], spt, dt\" > Evalute.txt", shell=True)

#----------------------------------------------------------------------
# fitting parameters
element = "B"
#------------------------
stospt = np.array([1.0,1.10,1.20,1.3])
stodt  = np.array([1.0,1.10,1.20,1.3])
#------------------------
stosp  = np.array([0.5,0.75,1.92,4.3])
stod   = np.array([0.5,0.75,1.92,4.3])
#------------------------
print("initial parameters, SP: "+str(stosp))
print("initial parameters, D : "+str(stod))

subprocess.run("cd ./"+str(element)+" ; rm -f -r results ; cd ../", shell=True)
subprocess.run("cd ./"+str(element)+" ; mkdir results ; cd ../", shell=True)

count = 0
#----------------------------------------------------------------------
def f(stosp,stod):
  
  print("------------------------")
  global count
  count += 1
  print(count)
  
  subprocess.run("cp "+" "+str(file_tmp)+" "+str(file_inp), shell=True)

  stos_all = str(stosp[0])+" "+str(stosp[1])+" "+str(stosp[2])+" "+str(stosp[3])
  stop_all = str(stod[0])+" "+str(stod[1])+" "+str(stod[2])+" "+str(stod[3])  
  subprocess.call("sed -i s/stosp/\""+str(stos_all)+"\"/g "+str(file_inp), shell=True)
  subprocess.call("sed -i s/stod/\""+str(stop_all)+"\"/g "+str(file_inp), shell=True)
  
  skgen = subprocess.run("/mnt/d/skprogs/sktools/src/sktools/scripts/skgen.py -o slateratom -t sktwocnt sktable -d "+str(element)+" "+str(element), shell=True, stdout=subprocess.PIPE)
  
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
  print("------------------------")
  subprocess.run("echo No."+str(count)+": "+str(y)+", "+str(spt)+", "+str(dt)+" >> Evalute.txt", shell=True)

  return y
#----------------------------------------------------------------------
# fitting parameters
for dt in np.arange(0.7,1.5,0.1):
  for spt in np.arange(0.7,1.5,0.05):
    new_stosp = stosp * stospt ** spt
    new_stod  = stod * stodt ** dt
    res = f(new_stosp,new_stod)
  subprocess.run("echo \"\" >> Evalute.txt", shell=True)
#----------------------------------------------------------------------
