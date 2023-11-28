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
#skprogs_adress = "/home/ubuntu/skprogs-v.0.2.1/sktools/src/sktools/scripts/skgen.py" # Linux
skprogs_adress = "/mnt/d/skprogs-v.0.2.1/sktools/src/sktools/scripts/skgen.py" # WSL2
#pwscf_adress = "mpirun -np "+str(num_core)+" pw.x"

subprocess.run("echo \"#No.: ETA value [eV], spt, dt\" > Evalute.txt", shell=True)

#----------------------------------------------------------------------
# fitting parameters
element = "Mg"
atomic_number = 12.0 # = y4
base = 0.5           # = y0
#------------------------
dt = 0.1             # t=[-(4/dt):(2/dt)]
#------------------------
hwb_sp =  0.8
hwt_sp =  3.0
#------------------------
hwb_do =  0.8
hwt_do =  3.0
#------------------------
y0 = base
y1 = y2 = y3 = y0
ylast = atomic_number
#------------------------
stosp  = np.array([y0,y1,y2,y3,ylast])
stod   = np.array([y0,y1,y2,y3,ylast])
#------------------------

subprocess.run("cd ./"+str(element)+" ; rm -f -r results ; cd ../", shell=True)
subprocess.run("cd ./"+str(element)+" ; mkdir results ; cd ../", shell=True)
subprocess.run("cd ./"+str(element)+" ; chmod +x *.sh ; cd ../", shell=True)

if os.path.exists(str(element)+"-"+str(element)+".skf"):
  print("------------------------")
  print("Delete old "+str(element)+"-"+str(element)+".skf file")
  subprocess.run("rm -f "+str(element)+"-"+str(element)+".skf", shell=True)

count = 0
#----------------------------------------------------------------------
def f(stosp,stod,spt,dot):
  
  print("------------------------")
  global count
  count += 1
  print(count)
  print("set parameters, SP: "+str(stosp))
  print("set parameters, D : "+str(stod))
  
  subprocess.run("cp "+" "+str(file_tmp)+" "+str(file_inp), shell=True)

  stos_all = str(stosp[0])+" "+str(stosp[1])+" "+str(stosp[2])+" "+str(stosp[3])+" "+str(stosp[4])
  stod_all = str(stod[0])+" "+str(stod[1])+" "+str(stod[2])+" "+str(stod[3])+" "+str(stod[4])
  subprocess.call("sed -i s/stosp/\""+str(stos_all)+"\"/g "+str(file_inp), shell=True)
  subprocess.call("sed -i s/stod/\""+str(stod_all)+"\"/g "+str(file_inp), shell=True)
  
  subprocess.run("export OMP_NUM_THREADS="+str(num_core), shell=True)
  skgen = subprocess.run("python3 "+str(skprogs_adress)+" -o slateratom -t sktwocnt sktable -d "+str(element)+" "+str(element), shell=True, stdout=subprocess.PIPE)
  subprocess.run("export OMP_NUM_THREADS=1", shell=True)
  
  if os.path.exists(str(element)+"-"+str(element)+".skf"):
    subprocess.run("cd ./"+str(element)+" ; ./run.sh ; cd ../", shell=True)
    evaluate = subprocess.run("awk '{if(NR==10){printf \"%s\",$3}}' ./"+str(element)+"/"+str(file_msd), shell=True, stdout=subprocess.PIPE)
    if evaluate.returncode == 0:
      try:
        y = float(str(evaluate.stdout).lstrip("b'").rstrip("\\n'"))
        subprocess.run("mv "+str(file_inp)+" ./"+str(element)+"/results/"+str(file_inp)+"_No"+str(count), shell=True)
        subprocess.run("cp ./"+str(element)+"/comp_band.png ./"+str(element)+"/results/comp_band_No"+str(count)+".png", shell=True)
      except ValueError as error:
        y = 99999.999
    else:
      y = 99999.999
  else:
    y = 99999.999
  
  print("Evaluate: ",str(y))
  print("------------------------")
  subprocess.run("echo No."+str(count)+": "+str(y)+", "+str(spt)+", "+str(dot)+" >> Evalute.txt", shell=True)

  return y
#----------------------------------------------------------------------
# fitting parameters
for dot in np.arange((hwb_do/dt),(hwt_do/dt),dt): # d orbital
  y1 = (atomic_number - base)*(3/8)**((1.0/(1.0-dt))**dot) + base # x=3/8
  y2 = (atomic_number - base)*(4/8)**((1.0/(1.0-dt))**dot) + base # x=4/8
  y3 = (atomic_number - base)*(6/8)**((1.0/(1.0-dt))**dot) + base # x=6/8
  stod[1]  = y1
  stod[2]  = y2
  stod[3]  = y3
  for spt in np.arange((hwb_sp/dt),(hwt_sp/dt),dt): # sp orbitals
    y1 = (atomic_number - base)*(3/8)**((1.0/(1.0-dt))**spt) + base # x=3/8
    y2 = (atomic_number - base)*(4/8)**((1.0/(1.0-dt))**spt) + base # x=4/8
    y3 = (atomic_number - base)*(6/8)**((1.0/(1.0-dt))**spt) + base # x=6/8
    stosp[1] = y1
    stosp[2] = y2
    stosp[3] = y3
    res = f(stosp,stod,spt,dot)
  subprocess.run("echo \"\" >> Evalute.txt", shell=True)
#----------------------------------------------------------------------
