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
#skprogs_adress = "/home/ubuntu/skprogs-v.0.2.1/sktools/src/sktools/scripts/skgen.py" # Linux
skprogs_adress = "/mnt/d/skprogs-v.0.2.1/sktools/src/sktools/scripts/skgen.py" # WSL2
#pwscf_adress = "mpirun -np "+str(num_core)+" pw.x"

#----------------------------------------------------------------------
# set initial parameters and boundaries
#----------------------------------------------------------------------
element = "element_Xx"
atomic_number = atomic_number_Yy # In this code, this value is used as a parameter of the radial wave function.
#---------------------------
# The parameters of the radial wave function.
#y0s = 0.5 # S orbitals
#y0p = 0.5 # P orbitals
#y0d = 1.5 # D orbitals
#----------
#y0s = 1.0 # S orbitals
#y0p = 1.0 # P orbitals
#y0d = 1.5 # D orbitals
#----------
#y0s = 1.5 # S orbitals
#y0p = 1.5 # P orbitals
#y0d = 2.0 # D orbitals
#----------
#y0s = 2.0 # S orbitals, TM: 2.0
#y0p = 2.0 # P orbitals, TM: 2.0
#y0d = 2.5 # D orbitals, TM: 2.5
#----------
y0s = y0s_Nn # S orbitals
y0p = y0p_Nn # P orbitals
y0d = y0d_Nn # D orbitals
#--------
# The parameters of the radial wave function.
#ylasts = atomic_number      # S orbitals
#ylastp = atomic_number      # P orbitals
#ylastd = atomic_number*2.0  # D orbitals
#----------
#ylasts = atomic_number*1.5   # S orbitals
#ylastp = atomic_number*1.5   # P orbitals
#ylastd = atomic_number*2.0   # D orbitals
#----------
#ylasts = atomic_number*2.0  # S orbitals, TM: x2.0
#ylastp = atomic_number*2.0  # P orbitals, TM: x2.0
#ylastd = atomic_number*3.0  # D orbitals, TM: x2.0
#----------
ylasts = ylasts_Nn   # S orbitals
ylastp = ylastp_Nn   # P orbitals
ylastd = ylastd_Nn   # D orbitals
#---------------------------

#------------------------------------------------
# Note: Empirically, setting a value around 0.3 will significantly reduce the number of failures.
#---------------------------
hwb_den = 0.15 # search range [-x*hwb:+x*hwt]
hwt_den = 0.15 # search range [-x*hwb:+x*hwt]
#---------------------------
hwb_wav = 0.37 # search range [-x*hwb:+x*hwt]
hwt_wav = 0.37 # search range [-x*hwb:+x*hwt]
#---------------------------
hwb_sto = 0.27 # search range [-x*hwb:+x*hwt]
hwt_sto = 0.27 # search range [-x*hwb:+x*hwt]
#---------------------------
# Note
# 1. A value around sigma = 7.0 is often good. (r0 >= 12.0 in this case)
# 2. It is often good for r0 for the S orbit to be slightly (about 1.0 ?) smaller than for the P or D orbits.
# 3. In the radial wave function, calculations can be converged over a fairly wide range for the S orbit, 
#   but of course the P orbit is more limited than the S orbit. When increasing the value, 
#   start from the value at which the P orbit begins to converge. Conversely, when decreasing the value, 
#   start from the value at which the P orbit begins to converge.
# 4. In transition metals, it is often sufficient to adjust the P orbital last.
# 5. The radial wave function only slightly moves the position of each orbit. 
#---------------------------
x0  = x0_Zz # sigma of density
x1  = x1_Zz # r0 of density
#---------------------------
x2  = x2_Zz # simga of S
x3  = x3_Zz # r0 of S
#---------------------------
x4  = x4_Zz # simga of P
x5  = x5_Zz # r0 of P
#---------------------------
x6  = x6_Zz # simga of D
x7  = x7_Zz # r0 of D
#---------------------------
sto_auto_preset = "yes"
if sto_auto_preset == "no":
  #---------------------------
  x8  =  x8_Nn # y1 of S
  x9  =  x9_Nn # y2 of Ss
  x10 = x10_Nn # y3 of S
  #---------------------------
  x11 = x11_Nn # y1 of P
  x12 = x12_Nn # y2 of P
  x13 = x13_Nn # y3 of P
  #---------------------------
  x14 = x14_Nn # y1 of D or D
  x15 = x15_Nn # y2 of D or D
  x16 = x16_Nn # y3 of D or D
  #---------------------------
else:
  print("Auto set coefficients of Slater-type orbitals.")
  # In the results for boron, it was better to equalize the log (coefficient), 
  #   so we made it possible to select it as the initial value.
  #---------------------------
  #x8  = np.exp( (np.log(ylasts)-np.log(y0s))*1/4 + np.log(y0s) )
  #x9  = np.exp( (np.log(ylasts)-np.log(y0s))*2/4 + np.log(y0s) )
  #x10 = np.exp( (np.log(ylasts)-np.log(y0s))*3/4 + np.log(y0s) )
  x8  = 10.0**( (np.log10(ylasts)-np.log10(y0s))*1/4 + np.log10(y0s) )
  x9  = 10.0**( (np.log10(ylasts)-np.log10(y0s))*2/4 + np.log10(y0s) )
  x10 = 10.0**( (np.log10(ylasts)-np.log10(y0s))*3/4 + np.log10(y0s) )
  #---------------------------
  #x11 = np.exp( (np.log(ylastp)-np.log(y0p))*1/4 + np.log(y0p) )
  #x12 = np.exp( (np.log(ylastp)-np.log(y0p))*2/4 + np.log(y0p) )
  #x13 = np.exp( (np.log(ylastp)-np.log(y0p))*3/4 + np.log(y0p) )
  x11 = 10.0**( (np.log10(ylastp)-np.log10(y0p))*1/4 + np.log10(y0p) )
  x12 = 10.0**( (np.log10(ylastp)-np.log10(y0p))*2/4 + np.log10(y0p) )
  x13 = 10.0**( (np.log10(ylastp)-np.log10(y0p))*3/4 + np.log10(y0p) )
  #---------------------------
  #x14 = np.exp( (np.log(ylastd)-np.log(y0d))*1/4 + np.log(y0d) )
  #x15 = np.exp( (np.log(ylastd)-np.log(y0d))*2/4 + np.log(y0d) )
  #x16 = np.exp( (np.log(ylastd)-np.log(y0d))*3/4 + np.log(y0d) )
  x14 = 10.0**( (np.log10(ylastd)-np.log10(y0d))*1/4 + np.log10(y0d) )
  x15 = 10.0**( (np.log10(ylastd)-np.log10(y0d))*2/4 + np.log10(y0d) )
  x16 = 10.0**( (np.log10(ylastd)-np.log10(y0d))*3/4 + np.log10(y0d) )
  #---------------------------
#---------------------------
print("------------------------")
print("initial parameters:   x0  x1  x2  x3  x4  x5  x6  x7   x8   x9"
  +"  x10  x11  x12  x13  x14  x15  x16")
print("initial parameters: ",x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16)
x = [x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16]
#------------------------------------------------

#------------------------------------------------
n_gene = 17 # number of parameters, number of individual +1
min_ind = np.ones(n_gene) * -1.0
max_ind = np.ones(n_gene) *  1.0
#---------------------------
# sigma of density
min_ind[0] = float(x0) - float(x0)*hwb_den
max_ind[0] = float(x0) + float(x0)*hwt_den
#min_ind[0] =  2.0; max_ind[0] = 17.0
#---------------------------
# r0 of density
min_ind[1] = float(x1) - float(x1)*hwb_den
max_ind[1] = float(x1) + float(x1)*hwt_den
#min_ind[1] =  2.4; max_ind[1] = 29.0
#---------------------------
# sigma of S orbitals
min_ind[2] = float(x2) - float(x2)*hwb_wav
max_ind[2] = float(x2) + float(x2)*hwt_wav
#min_ind[2] =  2.0; max_ind[2] = 17.0
#---------------------------
# r0 of S orbitals
min_ind[3] = float(x3) - float(x3)*hwb_wav
max_ind[3] = float(x3) + float(x3)*hwt_wav
#min_ind[3] =  2.4; max_ind[3] = 29.0
#---------------------------
# sigma of P orbitals
min_ind[4] = float(x4) - float(x4)*hwb_wav
max_ind[4] = float(x4) + float(x4)*hwt_wav
#min_ind[4] =  2.0; max_ind[4] = 17.0
#---------------------------
# r0 of P orbitals
min_ind[5] = float(x5) - float(x5)*hwb_wav
max_ind[5] = float(x5) + float(x5)*hwt_wav
#min_ind[5] =  2.4; max_ind[5] = 29.0
#---------------------------
# sigma of D orbitals
min_ind[6] = float(x6) - float(x6)*hwb_wav
max_ind[6] = float(x6) + float(x6)*hwt_wav
#min_ind[6] =  2.0; max_ind[6] = 17.0
#---------------------------
# r0 of D orbitals
min_ind[7] = float(x7) - float(x7)*hwb_wav
max_ind[7] = float(x7) + float(x7)*hwt_wav
#min_ind[7] =  2.4; max_ind[7] = 29.0
#---------------------------
# Slater-Type Orbitals of S: y1
min_ind[8] = float(x8) - float(x8)*hwb_sto
max_ind[8] = float(x8) + float(x8)*hwt_sto
#---------------------------
# Slater-Type Orbitals of S: y2
min_ind[9] = float(x9) - float(x9)*hwb_sto
max_ind[9] = float(x9) + float(x9)*hwt_sto
#---------------------------
# Slater-Type Orbitals of S: y3
min_ind[10] = float(x10) - float(x10)*hwb_sto
max_ind[10] = float(x10) + float(x10)*hwt_sto
#---------------------------
# Slater-Type Orbitals of P: y1
min_ind[11] = float(x11) - float(x11)*hwb_sto
max_ind[11] = float(x11) + float(x11)*hwt_sto
#---------------------------
# Slater-Type Orbitals of P: y2
min_ind[12] = float(x12) - float(x12)*hwb_sto
max_ind[12] = float(x12) + float(x12)*hwt_sto
#---------------------------
# Slater-Type Orbitals of P: y3
min_ind[13] = float(x13) - float(x13)*hwb_sto
max_ind[13] = float(x13) + float(x13)*hwt_sto
#---------------------------
# Slater-Type Orbitals of D: y1
min_ind[14] = float(x14) - float(x14)*hwb_sto
max_ind[14] = float(x14) + float(x14)*hwt_sto
#---------------------------
# Slater-Type Orbitals of D: y2
min_ind[15] = float(x15) - float(x15)*hwb_sto
max_ind[15] = float(x15) + float(x15)*hwt_sto
#---------------------------
# Slater-Type Orbitals of D: y3
min_ind[16] = float(x16) - float(x16)*hwb_sto
max_ind[16] = float(x16) + float(x16)*hwt_sto
#---------------------------
if min_ind[0] < 2.0:
  min_ind[0] = 2.0
if min_ind[2] < 2.0:
  min_ind[2] = 2.0
if min_ind[4] < 2.0:
  min_ind[4] = 2.0
if min_ind[6] < 2.0:
  min_ind[6] = 2.0
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
subprocess.run("echo \"#No.: ETA [eV], sigma_den, r0_den, simga_s, r0_s, sigma_p, r0_p, sigma_d, r0_d,"
  +" stos(y1s), stos(y2s), stos(y3s), stop(y1p), stop(y2p), stop(y3p), stod(y1d), stod(y2d), stod(y3d), sdt, sdt3kbt"
  +" \" > Evalute.txt", shell=True)
subprocess.run("echo \"#| iter | 1/target | x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 |"
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
  if fine_step == "no": # 0.2 and 0.02 step for sigma and sto, respectively.
    print("0.2 and 0.02 step for sigma and sto, respectively.")
    #-------------------------------
    # Density
    #--------- 0.2 step
    if int(x0*10+0.5) % 2 == 0:
      sx0 = "{:.1f}".format(x0)
    else:
      sx0 = "{:.1f}".format(x0+0.1)
    #--------- 0.1 step
    sx1  = "{:.1f}".format(x1+R1)
    #-------------------------------
    #-------------------------------
    # S orbital
    #--------- 0.2 step
    if int(x2*10+0.5) % 2 == 0:
      sx2 = "{:.1f}".format(x2)
    else:
      sx2 = "{:.1f}".format(x2+0.1)
    #--------- 0.1 step
    sx3  = "{:.1f}".format(x3+R1)
    #-------------------------------
    #-------------------------------
    # P orbital
    #--------- 0.2 step
    if int(x4*10+0.5) % 2 == 0:
      sx4 = "{:.1f}".format(x4)
    else:
      sx4 = "{:.1f}".format(x4+0.1)
    #--------- 0.1 step
    sx5  = "{:.1f}".format(x5+R1)
    #-------------------------------
    #-------------------------------
    # D orbital
    #--------- 0.2 step
    if int(x6*10+0.5) % 2 == 0:
      sx6 = "{:.1f}".format(x6)
    else:
      sx6 = "{:.1f}".format(x6+0.1)
    #--------- 0.1 step
    sx7  = "{:.1f}".format(x7+R1)
    #-------------------------------
    #-------------------------------
    # Slater-Type Orbitals of S
    #--------- 0.02 step
    if int(x8*100+0.5) % 2 == 0:
      sx8 = "{:.2f}".format(x8)
    else:
      sx8 = "{:.2f}".format(x8+0.01)
    #--------- 0.02 step
    if int(x9*100+0.5) % 2 == 0:
      sx9 = "{:.2f}".format(x9)
    else:
      sx9 = "{:.2f}".format(x9+0.01)
    #--------- 0.02 step
    if int(x10*100+0.5) % 2 == 0:
      sx10 = "{:.2f}".format(x10)
    else:
      sx10 = "{:.2f}".format(x10+0.01)
    #-------------------------------
    #-------------------------------
    # Slater-Type Orbitals of P
    #--------- 0.02 step
    if int(x11*100+0.5) % 2 == 0:
      sx11 = "{:.2f}".format(x11)
    else:
      sx11 = "{:.2f}".format(x11+0.01)
    #--------- 0.02 step
    if int(x12*100+0.5) % 2 == 0:
      sx12 = "{:.2f}".format(x12)
    else:
      sx12 = "{:.2f}".format(x12+0.01)
    #--------- 0.02 step
    if int(x13*100+0.5) % 2 == 0:
      sx13 = "{:.2f}".format(x13)
    else:
      sx13 = "{:.2f}".format(x13+0.01)
    #-------------------------------
    #-------------------------------
    # Slater-Type Orbitals of D
    #--------- 0.02 step
    if int(x14*100+0.5) % 2 == 0:
      sx14 = "{:.2f}".format(x14)
    else:
      sx14 = "{:.2f}".format(x14+0.01)
    #--------- 0.02 step
    if int(x15*100+0.5) % 2 == 0:
      sx15 = "{:.2f}".format(x15)
    else:
      sx15 = "{:.2f}".format(x15+0.01)
    #--------- 0.02 step
    if int(x16*100+0.5) % 2 == 0:
      sx16 = "{:.2f}".format(x16)
    else:
      sx16 = "{:.2f}".format(x16+0.01)
    #-------------------------------
  else:
    print("sigma and r0: 0.1 step, sto: 0.01 step")
    #-------------------------------
    # Density
    sx0  = "{:.1f}".format(x0+R1)
    sx1  = "{:.1f}".format(x1+R1)
    #-------------------------------
    # S orbital
    sx2  = "{:.1f}".format(x2+R1)
    sx3  = "{:.1f}".format(x3+R1)
    #-------------------------------
    # P orbital
    sx4  = "{:.1f}".format(x4+R1)
    sx5  = "{:.1f}".format(x5+R1)
    #-------------------------------
    # D orbital
    sx6  = "{:.1f}".format(x6+R1)
    sx7  = "{:.1f}".format(x7+R1)
    #-------------------------------
    # Slater-Type Orbitals of S
    sx8  = "{:.2f}".format(x8+R2)
    sx9  = "{:.2f}".format(x9+R2)
    sx10 = "{:.2f}".format(x10+R2)
    #-------------------------------
    # Slater-Type Orbitals of P
    sx11 = "{:.2f}".format(x11+R2)
    sx12 = "{:.2f}".format(x12+R2)
    sx13 = "{:.2f}".format(x13+R2)
    #-------------------------------
    # Slater-Type Orbitals of D
    sx14 = "{:.2f}".format(x14+R2)
    sx15 = "{:.2f}".format(x15+R2)
    sx16 = "{:.2f}".format(x16+R2)
    #-------------------------------
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
    subprocess.run("mv ./"+element+"-"+element+".skf ./"+element+"/"+element+"-"+element+".skf", shell=True)
    subprocess.run("cd ./"+element+" ; ./run.sh ; cd ../", shell=True)
    evaluate = subprocess.run("awk '{if(NR==10){printf \"%s\",$3}}' ./"+element+"/"+file_msd, shell=True, stdout=subprocess.PIPE)
    evaluate_sdt = subprocess.run("awk '{if(NR==4){printf \"%s\",$3}}' ./"+element+"/"+file_msd, shell=True, stdout=subprocess.PIPE)
    evaluate_sdt3kbt = subprocess.run("awk '{if(NR==8){printf \"%s\",$3}}' ./"+element+"/"+file_msd, shell=True, stdout=subprocess.PIPE)
    if evaluate.returncode == 0:
      try:
        etav = float(str(evaluate.stdout).lstrip("b'").rstrip("\\n'"))
        sdtv = float(str(evaluate_sdt.stdout).lstrip("b'").rstrip("\\n'"))
        sdtv3kbt = float(str(evaluate_sdt3kbt.stdout).lstrip("b'").rstrip("\\n'"))
        y = 1.0/etav
        subprocess.run("mv "+file_inp+" ./"+element+"/results/"+file_inp+"_No"+str(count), shell=True)
        subprocess.run("cp ./"+element+"/comp_band.png ./"+element+"/results/comp_band_No"+str(count)+".png", shell=True)
      except ValueError as error:
        y = 0.0
        etav = 9.999
        sdtv = 9.999
        sdtv3kbt = 9.999
    else:
      y = 0.0
      etav = 9.999
      sdtv = 9.999
      sdtv3kbt = 9.999
  else:
    y = 0.0
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
  print("Next values")
  print("| iter | target | x0 | x1 | x10 | x11 | ... ")
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
  new_optimizer.maximize(init_points=11, n_iter=(600*2)) # 300 cycle / 6 h
  new_optimizer.set_gp_params(alpha=1e-3) # The greater the whitenoise, the greater alpha value.
else:
  optimizer = BayesianOptimization(f=descripter, pbounds=pbounds, verbose=2, random_state=1, bounds_transformer=bounds_transformer, allow_duplicate_points=True)
  logger = JSONLogger(path="./logs") # Results will be saved in ./logs.json
  optimizer.subscribe(Events.OPTIMIZATION_STEP, logger)
  optimizer.maximize(init_points=(n_gene*11), n_iter=(600*1)) # 600 cycles / 12 h (Note: It depends on the number of parameters and search range, but usually around 150 times is a good value (in n_gene*5 case). I set it to 600 just in case (from after I got home until the next morning).)
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
