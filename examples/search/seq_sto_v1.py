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
base = 0.5          # = y0
#------------------------
dt = 0.1            # t=[-(4/dt):(2/dt)]
t = -(4.0/dt)
y0 = base
y1 = (atomic_number - base)*(1/4)**((1.0/(1.0-dt))**t) + base # x=1/4, t=-40
y2 = (atomic_number - base)*(2/4)**((1.0/(1.0-dt))**t) + base # x=2/4, t=-40
y3 = (atomic_number - base)*(3/4)**((1.0/(1.0-dt))**t) + base # x=3/4, t=-40
y4 = atomic_number
stosp  = np.array([y0,y1,y2,y3,y4])
stod   = np.array([y0,y1,y2,y3,y4])
#------------------------
new_stosp = stosp
new_stod = stod
#------------------------
print("initial parameters, SP: "+str(new_stosp))
print("initial parameters, D : "+str(new_stod))
#------------------------

subprocess.run("cd ./"+str(element)+" ; rm -f -r results ; cd ../", shell=True)
subprocess.run("cd ./"+str(element)+" ; mkdir results ; cd ../", shell=True)
subprocess.run("cd ./"+str(element)+" ; chmod +x *.sh ; cd ../", shell=True)

count = 0
#----------------------------------------------------------------------
def f(stosp,stod,spt,dot):
  
  print("------------------------")
  global count
  count += 1
  print(count)
  
  subprocess.run("cp "+" "+str(file_tmp)+" "+str(file_inp), shell=True)

  stos_all = str(stosp[0])+" "+str(stosp[1])+" "+str(stosp[2])+" "+str(stosp[3])
  stop_all = str(stod[0])+" "+str(stod[1])+" "+str(stod[2])+" "+str(stod[3])  
  subprocess.call("sed -i s/stosp/\""+str(stos_all)+"\"/g "+str(file_inp), shell=True)
  subprocess.call("sed -i s/stod/\""+str(stop_all)+"\"/g "+str(file_inp), shell=True)
  
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
for dot in np.arange(-(4.0/dt),(2.0/dt),dt): # d orbital
  y1 = (atomic_number - base)*(1/4)**((1.0/(1.0-dt))**dot) + base # x=1/4
  y2 = (atomic_number - base)*(2/4)**((1.0/(1.0-dt))**dot) + base # x=2/4
  y2 = (atomic_number - base)*(3/4)**((1.0/(1.0-dt))**dot) + base # x=3/4
  new_stod[1]  = y1
  new_stod[2]  = y2
  new_stod[3]  = y3
  for spt in np.arange(-(4.0/dt),(2.0/dt),dt): # sp orbitals
    y1 = (atomic_number - base)*(1/4)**((1.0/(1.0-dt))**spt) + base # x=1/4
    y2 = (atomic_number - base)*(2/4)**((1.0/(1.0-dt))**spt) + base # x=2/4
    y2 = (atomic_number - base)*(3/4)**((1.0/(1.0-dt))**spt) + base # x=3/4
    new_stosp[1] = y1
    new_stosp[2] = y2
    new_stosp[3] = y3
    res = f(new_stosp,new_stod,spt,dot)
  subprocess.run("echo \"\" >> Evalute.txt", shell=True)
#----------------------------------------------------------------------
