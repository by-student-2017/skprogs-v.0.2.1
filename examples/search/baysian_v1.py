from bayes_opt import BayesianOptimization
import numpy as np
import subprocess
import sys
import os
#----------------------------------------------------------------------
# command:
# 1. pip3 install bayesian-optimization==1.4.3
# 2. python3 baysian_v1.py
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
#skprogs_adress = "/home/ubuntu/skprogs-v.0.2.1/sktools/src/sktools/scripts/skgen.py" # Linux
skprogs_adress = "/mnt/d/skprogs-v.0.2.1/sktools/src/sktools/scripts/skgen.py" # WSL2
#pwscf_adress = "mpirun -np "+str(num_core)+" pw.x"

subprocess.run("echo \"#No.: ETA value [eV], r0, sigma\" > Evalute.txt", shell=True)

#----------------------------------------------------------------------
element = "Mg"
atomic_number = 12.0
#---------------------------
y0s = 0.5
y0p = 0.5
y0d = 1.5
#--------
ylasts = atomic_number
ylastp = atomic_number
ylastd = atomic_number
#---------------------------

#------------------------------------------------
hw  =  0.3 # search range [-x*hw:+x*hw]
#---------------------------
x0  =  2.0 # sigma of density
x1  = 17.0 # r0 of density
#---------------------------
x2  =  6.2 # simga of S
x3  =  5.0 # r0 of S
#---------------------------
x4  =  6.2 # simga of P
x5  =  5.0 # r0 of P
#---------------------------
x6  =  6.2 # simga of D
x7  =  5.0 # r0 of D
#---------------------------
x8  =  0.93 # y1 of S
x9  =  2.18 # y2 of S
x10 =  5.12 # y3 of S
#---------------------------
x11 =  0.93 # y1 of P
x12 =  2.18 # y2 of P
x13 =  5.12 # y3 of P
#---------------------------
x14 =  2.75 # y1 of D or D
x15 =  5.81 # y2 of D or D
x16 = 12.30 # y3 of D or D
#---------------------------
print("------------------------")
print("initial parameters: ",x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16)
x = [x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16]
#------------------------------------------------

#------------------------------------------------
n_gene = 17 # number of parameters, number of individual +1
min_ind = np.ones(n_gene) * -1.0
max_ind = np.ones(n_gene) *  1.0
#---------------------------
min_ind[0] = float(x0) - float(x0)*hw
max_ind[0] = float(x0) + float(x0)*hw
min_ind[1] = float(x1) - float(x1)*hw
max_ind[1] = float(x1) + float(x1)*hw
min_ind[2] = float(x2) - float(x2)*hw
max_ind[2] = float(x2) + float(x2)*hw
min_ind[3] = float(x3) - float(x3)*hw
max_ind[3] = float(x3) + float(x3)*hw
min_ind[4] = float(x4) - float(x4)*hw
max_ind[4] = float(x4) + float(x4)*hw
min_ind[5] = float(x5) - float(x5)*hw
max_ind[5] = float(x5) + float(x5)*hw
min_ind[6] = float(x6) - float(x6)*hw
max_ind[6] = float(x6) + float(x6)*hw
min_ind[7] = float(x7) - float(x7)*hw
max_ind[7] = float(x7) + float(x7)*hw
min_ind[8] = float(x8) - float(x8)*hw
max_ind[8] = float(x8) + float(x8)*hw
min_ind[9] = float(x9) - float(x9)*hw
max_ind[9] = float(x9) + float(x9)*hw
min_ind[10] = float(x10) - float(x10)*hw
max_ind[10] = float(x10) + float(x10)*hw
min_ind[11] = float(x11) - float(x11)*hw
max_ind[11] = float(x11) + float(x11)*hw
min_ind[12] = float(x12) - float(x12)*hw
max_ind[12] = float(x12) + float(x12)*hw
min_ind[13] = float(x13) - float(x13)*hw
max_ind[13] = float(x13) + float(x13)*hw
min_ind[14] = float(x14) - float(x14)*hw
max_ind[14] = float(x14) + float(x14)*hw
min_ind[15] = float(x15) - float(x15)*hw
max_ind[15] = float(x15) + float(x15)*hw
min_ind[16] = float(x16) - float(x16)*hw
max_ind[16] = float(x16) + float(x16)*hw
#---------------------------
pbounds = {
   'x0': (float(min_ind[0]),float(max_ind[0])),
   'x1': (float(min_ind[1]),float(max_ind[1])),
   'x2': (float(min_ind[2]),float(max_ind[2])),
   'x3': (float(min_ind[3]),float(max_ind[3])),
   'x4': (float(min_ind[4]),float(max_ind[4])),
   'x5': (float(min_ind[5]),float(max_ind[5])),
   'x6': (float(min_ind[6]),float(max_ind[6])),
   'x7': (float(min_ind[7]),float(max_ind[7])),
   'x8': (float(min_ind[8]),float(max_ind[8])),
   'x9': (float(min_ind[9]),float(max_ind[9])),
  'x10': (float(min_ind[10]),float(max_ind[10])),
  'x11': (float(min_ind[11]),float(max_ind[11])),
  'x12': (float(min_ind[12]),float(max_ind[12])),
  'x13': (float(min_ind[13]),float(max_ind[13])),
  'x14': (float(min_ind[14]),float(max_ind[14])),
  'x15': (float(min_ind[15]),float(max_ind[15])),
  'x16': (float(min_ind[16]),float(max_ind[16]))}# boundary
print("------------------------")
print("boundary of parameters: ",pbounds)
print("------------------------")
#------------------------------------------------

subprocess.run("cd ./"+str(element)+" ; rm -f -r results ; cd ../", shell=True)
subprocess.run("cd ./"+str(element)+" ; mkdir results ; cd ../", shell=True)
subprocess.run("cd ./"+str(element)+" ; chmod +x *.sh ; cd ../", shell=True)

if os.path.exists(str(element)+"-"+str(element)+".skf"):
  rint("------------------------")
  print("Delete old "+str(element)+"-"+str(element)+".skf file")
  subprocess.run("rm -f "+str(element)+"-"+str(element)+".skf", shell=True)

count = 0
#----------------------------------------------------------------------
def descripter(x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16):
  
  print("------------------------")
  global count
  count += 1
  print(count)
  
  subprocess.run("cp "+" "+str(file_tmp)+" "+str(file_inp), shell=True)
  
  #-------------------------------
  # Density
  subprocess.call("sed -i s/sigma_den/"+str(x0)+"/g "+str(file_inp), shell=True)
  subprocess.call("sed -i s/r0_den/"+str(x1)+"/g "+str(file_inp), shell=True)
  #-------------------------------
  # S orbital
  subprocess.call("sed -i s/sigma_s/"+str(x2)+"/g "+str(file_inp), shell=True)
  subprocess.call("sed -i s/r0_s/"+str(x3)+"/g "+str(file_inp), shell=True)
  #-------------------------------
  # P orbital
  subprocess.call("sed -i s/sigma_p/"+str(x4)+"/g "+str(file_inp), shell=True)
  subprocess.call("sed -i s/r0_p/"+str(x5)+"/g "+str(file_inp), shell=True)
  #-------------------------------
  # D orbital
  subprocess.call("sed -i s/sigma_d/"+str(x6)+"/g "+str(file_inp), shell=True)
  subprocess.call("sed -i s/r0_d/"+str(x7)+"/g "+str(file_inp), shell=True)
  #-------------------------------
  # Slater-Type Orbitals of S
  stos_all = str(y0s)+" "+str(x8)+" "+str(x9)+" "+str(x10)+" "+str(ylasts)
  subprocess.call("sed -i s/stos/\""+str(stos_all)+"\"/g "+str(file_inp), shell=True)
  #-------------------------------
  # Slater-Type Orbitals of P
  stop_all = str(y0p)+" "+str(x11)+" "+str(x12)+" "+str(x13)+" "+str(ylastp)
  subprocess.call("sed -i s/stop/\""+str(stop_all)+"\"/g "+str(file_inp), shell=True)
  #-------------------------------
  # Slater-Type Orbitals of D
  stod_all = str(y0d)+" "+str(x14)+" "+str(x15)+" "+str(x16)+" "+str(ylastd)
  subprocess.call("sed -i s/stod/\""+str(stod_all)+"\"/g "+str(file_inp), shell=True)
  #-------------------------------
  
  subprocess.run("export OMP_NUM_THREADS="+str(num_core), shell=True)
  skgen = subprocess.run("python3 "+str(skprogs_adress)+" -o slateratom -t sktwocnt sktable -d "+str(element)+" "+str(element), shell=True, stdout=subprocess.PIPE)
  subprocess.run("export OMP_NUM_THREADS=1", shell=True)
  
  if os.path.exists(str(element)+"-"+str(element)+".skf"):
    subprocess.run("cd ./"+str(element)+" ; ./run.sh ; cd ../", shell=True)
    evaluate = subprocess.run("awk '{if(NR==10){printf \"%s\",$3}}' ./"+str(element)+"/"+str(file_msd), shell=True, stdout=subprocess.PIPE)
    if evaluate.returncode == 0:
      try:
        eta = float(str(evaluate.stdout).lstrip("b'").rstrip("\\n'"))
        y = 1.0/eta
        subprocess.run("mv "+str(file_inp)+" ./"+str(element)+"/results/"+str(file_inp)+"_No"+str(count), shell=True)
        subprocess.run("cp ./"+str(element)+"/comp_band.png ./"+str(element)+"/results/comp_band_No"+str(count)+".png", shell=True)
      except ValueError as error:
        y = 0.0
        eta = 99999.999
    else:
      y = 0.0
      eta = 99999.999
  else:
    y = 0.0
    eta = 99999.999

  print("------------------------")
  print("iter:",count)
  print("------------------------")
  print("target:",str(y))
  print("------------------------")
  print("Density")
  print("set parameters, sigma_den = x0: "+str(x0))
  print("set parameters, r0_den = x1: "+str(x1))
  print("------------------------")
  print("S orbital")
  print("set parameters, sigma_s = x2: "+str(x2))
  print("set parameters, r0_s = x3: "+str(x3))
  print("------------------------")
  print("P orbital")
  print("set parameters, sigma_p = x4: "+str(x4))
  print("set parameters, r0_p = x5: "+str(x5))
  print("------------------------")
  print("D orbital")
  print("set parameters, sigma_d = x6: "+str(x6))
  print("set parameters, r0_d = x7: "+str(x7))
  print("------------------------")
  print("Slater-Type Orbitals of S")
  print("set parameters, y1s = x8: "+str(x8))
  print("set parameters, y2s = x9: "+str(x9))
  print("set parameters, y3s = x10: "+str(x10))
  print("------------------------")
  print("Slater-Type Orbitals of P")
  print("set parameters, y1p = x11: "+str(x11))
  print("set parameters, y2p = x12: "+str(x12))
  print("set parameters, y3p = x13: "+str(x13))
  print("------------------------")
  print("Slater-Type Orbitals of D")
  print("set parameters, y1d = x14: "+str(x14))
  print("set parameters, y2d = x15: "+str(x15))
  print("set parameters, y3d = x16: "+str(x16))
  print("------------------------")
  print("Next values")
  print("| iter | target | x0 | x1 | ... ")
  subprocess.run("echo No."+str(count)+": "+str(eta)+", "+str(x0)+", "+str(x1)+" >> Evalute.txt", shell=True)

  return y
#----------------------------------------------------------------------
# fitting parameters
optimizer = BayesianOptimization(f=descripter, pbounds=pbounds)
optimizer.set_gp_params(alpha=1e-3)
optimizer.maximize()
#optimizer.maximize(init_points=3, n_iter=2000, acq="ucb")
#acq = ucb, ei, poi, (default: ubc)
#----------------------------------------------------------------------
