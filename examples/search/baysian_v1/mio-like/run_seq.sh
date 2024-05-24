#!/bin/bash

filename="skdef.hsd"
if [ -f ${filename}_backup_run_seq ]; then
  cp ${filename}_backup_run_seq ${filename}
else
  cp ${filename} ${filename}_backup_run_seq
fi

#-------------------------------------------------------------------------
elements=(Xx
  H                                                                   He
  Li  Be                                           B   C   N   O   F  Ne
  Na  Mg                                          Al  Si   P   S  Cl  Ar
  K   Ca  Sc  Ti   V  Cr  Mn  Fe  Co  Ni  Cu  Zn  Ga  Ge  As  Se  Br  Kr
  Rb  Sr   Y  Zr  Nb  Mo  Tc  Ru  Rh  Pd  Ag  Cd  In  Sn  Sb  Te   I  Xe
  Cs  Ba
          La  Ce  Pr  Nd  Pm  Sm  Eu  Gd  Tb  Dy  Ho  Er  Tm  Yb  Lu  
              Hf  Ta   W  Re  Os  Ir  Pt  Au  Hg  Tl  Pb  Bi  Po  At  Rn
  Fr  Ra
          Ac  Th  Pa   U  Np  Pu  XX)
#-------------------------------------------------------------------------
lattices=(Yy
  SC                                                                  SC
  BCC HCP                                         SC  HCP SC  SC  SC  FCC
  BCC HCP                                         FCC FCC SC  SC  SC  FCC
  BCC FCC HCP HCP BCC BCC BCC BCC HCP FCC FCC HCP BCC FCC SC  SC  SC  FCC
  BCC FCC HCP HCP BCC BCC HCP HCP FCC FCC FCC HCP BCC FCC SC  SC  SC  FCC
  BCC BCC 
          HCP FCC HCP FCC FCC FCC FCC HCP HCP HCP HCP HCP HCP FCC HCP 
              HCP BCC BCC FCC HCP FCC FCC FCC SC  HCP FCC BCC SC  FCC FCC
  BCC BCC
          FCC FCC FCC FCC FCC FCC YY)
#-------------------------------------------------------------------------
nelement=(0
  1                                                                    2
  3   4                                            5   6   7   8   9  10
  11  12                                          13  14  15  16  17  18
  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35  36
  37  38  39  40  41  42  43  44  45  46  47  48  49  50  51  52  53  54
  55  56  
          57  58  59  60  61  62  63  64  65  66  67  68  69  70  71  
              72  73  74  75  76  77  78  79  80  81  82  83  84  85  86
  87  88
          89  90  91  92  93  94  95)
#------------------------------------------------------------------------------------------
# Angstrom, single bond
rcov1=(1.00
  0.32                                                                                 0.46
  1.33 1.02                                                   0.85 0.75 0.71 0.63 0.64 0.67
  1.55 1.39                                                   1.26 1.16 1.11 1.03 0.99 0.96
  1.96 1.71 1.48 1.36 1.34 1.22 1.19 1.16 1.11 1.10 1.12 1.18 1.24 1.24 1.21 1.16 1.14 1.17
  2.10 1.85 1.63 1.54 1.47 1.38 1.28 1.25 1.25 1.20 1.28 1.36 1.42 1.40 1.40 1.36 1.33 1.31
  2.32 1.96
            1.80 1.63 1.76 1.74 1.73 1.72 1.68 1.69 1.68 1.67 1.66 1.65 1.64 1.70 1.62
                 1.52 1.46 1.37 1.31 1.29 1.22 1.23 1.24 1.33 1.44 1.44 1.51 1.45 1.47 1.42
  2.23 2.01
            1.86 1.75 1.69 1.70 1.71 1.72 1.00)
# Ref: https://ja.wikipedia.org/wiki/%E5%85%B1%E6%9C%89%E7%B5%90%E5%90%88%E5%8D%8A%E5%BE%84
#------------------------------------------------------------------------------------------
# Angstrom, double bond
rcov2=(2.00
  0.00                                                                                 0.00
  1.24 0.90                                                   0.78 0.67 0.60 0.57 0.59 0.96
  1.60 1.36                                                   1.13 1.07 1.02 0.94 0.95 1.07
  1.93 1.44 1.16 1.17 1.12 1.11 1.05 1.09 1.03 1.01 1.15 1.20 1.17 1.17 1.14 1.07 1.09 1.21
  2.02 1.57 1.30 1.27 1.25 1.21 1.20 1.14 1.10 1.17 1.39 1.44 1.36 1.30 1.33 1.28 1.29 1.35
  2.09 1.61
            1.39 1.37 1.38 1.37 1.35 1.34 1.34 1.35 1.35 1.33 1.33 1.33 1.31 1.29 1.31
                 1.28 1.26 1.20 1.19 1.16 1.15 1.12 1.21 1.42 1.42 1.35 1.41 1.35 1.38 1.45
  2.18 1.73
            1.53 1.43 1.38 1.34 1.36 1.35 2.00)
# Ref: https://ja.wikipedia.org/wiki/%E5%85%B1%E6%9C%89%E7%B5%90%E5%90%88%E5%8D%8A%E5%BE%84
#------------------------------------------------------------------------------------------
# Angstrom, triple bond
rcov3=(3.00
  0.00                                                                                 0.00
  0.00 0.85                                                   0.73 0.60 0.54 0.53 0.53 0.00
  0.00 1.27                                                   1.11 1.02 0.94 0.95 0.93 0.96
  0.00 1.33 1.14 1.08 1.06 1.03 1.03 1.02 0.96 1.01 1.20 0.00 1.21 1.21 1.06 1.07 1.10 1.08
  0.00 1.39 1.24 1.21 1.16 1.13 1.10 1.03 1.06 1.12 1.37 0.00 1.46 1.32 1.27 1.21 1.25 1.22
  0.00 1.49
            1.39 1.31 1.28 0.00 0.00 0.00 0.00 1.32 0.00 0.00 0.00 0.00 0.00 0.00 1.31
                 1.21 1.19 1.15 1.10 1.09 1.07 1.10 1.23 0.00 1.50 1.37 1.35 1.29 1.38 1.33
  0.00 1.59
            1.40 1.36 1.29 1.18 1.16 0.00 3.00)
# Ref: https://ja.wikipedia.org/wiki/%E5%85%B1%E6%9C%89%E7%B5%90%E5%90%88%E5%8D%8A%E5%BE%84
#------------------------------------------------------------------------------------------------------------
# Bohr
rcov_be=(1.000
  0.586                                                                                                 0.529
  2.419 1.814                                                             1.587 1.436 1.342 1.247 1.077 1.096
  3.137 2.664                                                             2.287 2.097 2.022 1.984 1.928 2.003
  3.836 3.326 3.213 3.024 2.891 2.627 3.042 2.872 2.381 2.343 2.494 2.305 2.305 2.267 2.249 2.267 2.267 2.192
  4.157 3.685 3.590 3.307 3.099 2.910 2.778 2.759 2.683 2.627 2.740 2.721 2.683 2.627 2.627 2.608 2.627 2.646
  4.611 4.063
              3.912 3.855 3.836 3.798 3.760 3.742 3.742 3.704 3.667 3.628 3.628 3.572 3.590 3.533 3.307
                    3.307 3.213 3.061 2.853 2.721 2.664 2.570 2.570 2.494 2.740 2.759 2.797 2.646
  4.913 4.176
              4.062 3.893 3.779 3.704 3.590 3.534 3.401)
# Ref: https://en.wikipedia.org/wiki/Covalent_radius
#-------------------------------------------------------------------------------------------------------------
ndata=${#elements[@]}
#echo ${ndata}
#-------------------------------------------------------------------------
for((i=22;i<56;i++)); do # Ti-Ba
#for i in 24 28 30 31  32  33  34  35; do
  #--------------------------------------------------------------
  echo $i", "${nelement[$i]}", "${elements[$i]}", "${lattices[$i]}
  #echo $(($i+1))", "${nelement[$(($i+1))]}", "${elements[$(($i+1))]}", "${lattices[$(($i+1))]}
  #---------------------------------------------------------------
  # minimal input file
  #----- -----
  if [ -f ${filename}_backup_mkinp ]; then
    rm -f ${filename}_backup_mkinp
  fi
  #----- -----
  nOCC_Rn=`grep "OCCUPATIONS_Rn {" -n ${filename}_backup_run_seq | sed "s/:.*//g"`
  #----- -----
  n1st_start=`grep " ${elements[$i]} {" -n ${filename}_backup_run_seq | sed "s/:.*//g" | sed -n "1p"`
  n1st_end=`grep " ${elements[$(($i+1))]} {" -n ${filename}_backup_run_seq | sed "s/:.*//g" | sed -n "1p"`
  #----- -----
  nOne=`grep OnecenterParameters -n ${filename}_backup_run_seq | sed "s/:.*//g"`
  #----- -----
  n2nd_start=`grep " ${elements[$i]} {" -n ${filename}_backup_run_seq | sed "s/:.*//g" | sed -n "2p"`
  n2nd_end=`grep " ${elements[$(($i+1))]} {" -n ${filename}_backup_run_seq | sed "s/:.*//g" | sed -n "2p"`
  #----- -----
  nTwo_start=`grep TwoCenterParameters -n ${filename}_backup_run_seq | sed "s/:.*//g"`
  nTwo_end=`grep SkTwocnt_400_200 -n ${filename}_backup_run_seq | sed "s/:.*//g" | sed -n "1p"`
  #----- -----
  npair=`grep ${elements[$i]}-${elements[$i]} -n ${filename}_backup_run_seq  | sed "s/:.*//g"`
  #----- -----
  echo "nOCC_Rn   : "${nOCC_Rn}
  echo "n1st_start: "${n1st_start}
  echo "n1st_end  : "${n1st_end}
  echo "nOne      : "${nOne}
  echo "n2nd_start: "${n2nd_start}
  echo "n2nd_end  : "${n2nd_end}
  echo "nTwo_start: "${nTwo_start}
  echo "nTwo_end  : "${nTwo_end}
  echo "npair     : "${npair}
  #----- -----
  awk -v nOCC_Rn=${nOCC_Rn} '{if(NR<=(nOCC_Rn+4)){print $0}}' ${filename}_backup_run_seq > ${filename}
  awk -v n1st_start=${n1st_start} -v n1st_end=${n1st_end} '{if(n1st_start<=NR && NR<=(n1st_end-1)){print $0}}' ${filename}_backup_run_seq >> ${filename}
  echo } >> ${filename}
  echo "" >> ${filename}
  awk -v nOne=${nOne} '{if(nOne<=NR && NR<=(nOne+5)){print $0}}' ${filename}_backup_run_seq >> ${filename}
  awk -v n2nd_start=${n2nd_start} -v n2nd_end=${n2nd_end} '{if(n2nd_start<=NR && NR<=(n2nd_end-1)){print $0}}' ${filename}_backup_run_seq >> ${filename}
  echo } >> ${filename}
  echo "" >> ${filename}
  awk -v nTwo_start=${nTwo_start} -v nTwo_end=${nTwo_end} '{if(nTwo_start<=NR && NR<=(nTwo_end+3)){print $0}}' ${filename}_backup_run_seq >> ${filename}
  awk -v npair=${npair} '{if(NR==npair){print $0}}' ${filename}_backup_run_seq >> ${filename}
  echo } >> ${filename}
  #----- -----
  #---------------------------------------------------------------
  ./mkinp_baysian.sh ${elements[$i]} ${lattices[$i]} ${rcov1[$i]}
  #---------------------------------------------------------------
  cp plot_map.gpl ./${elements[$i]}/plot_map.gpl
  sort -k 2 Evalute.txt > Evalute_sort.txt
  mv Evalute_sort.txt ./${elements[$i]}/Evalute_sort.txt
  mv Evalute.txt ./${elements[$i]}/Evalute.txt
    #------------------------
    cd ./${elements[$i]}
      gnuplot < plot_map.gpl
    cd ..
    #------------------------
  mv logs.json   ./${elements[$i]}/logs.json
  mv skdef.hsd.tmp_baysian_${elements[$i]} ./${elements[$i]}/skdef.hsd.tmp_baysian_${elements[$i]}
  mv baysian_v1_${elements[$i]}.py ./${elements[$i]}/baysian_v1_${elements[$i]}.py
  #---------------------------------------------------------------
done
#-------------------------------------------------------------------------