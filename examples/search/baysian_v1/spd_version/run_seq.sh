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
          HCP FCC HCP FCC HCP HCP FCC HCP HCP HCP HCP HCP HCP FCC HCP 
              HCP BCC BCC FCC HCP FCC FCC FCC SC  HCP FCC BCC SC  FCC FCC
  BCC BCC
          FCC FCC FCC FCC FCC FCC  YY)
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
#-------------------------------------------------------------------------
ndata=${#elements[@]}
#echo ${ndata}
#-------------------------------------------------------------------------
#for((i=1;i<${ndata};i++)); do
#for((i=19;i<${ndata};i++)); do
#for((i=37;i<39;i++)); do
#for i in 38 47; do # Sr, Ag
for i in 19 38 40 42 44 46 48 50 52 33 31 21 23; do # K, Sr, Zr, Mo, Ru, Pd, Cd, Sn, Te, As, Ga, Sc, V
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
  n1st_start=`grep " ${elements[$i]} " -n ${filename}_backup_run_seq | sed "s/:.*//g" | sed -n "1p"`
  n1st_end=`grep " ${elements[$(($i+1))]} " -n ${filename}_backup_run_seq | sed "s/:.*//g" | sed -n "1p"`
  #----- -----
  nOne=`grep OnecenterParameters -n ${filename}_backup_run_seq | sed "s/:.*//g"`
  #----- -----
  n2nd_start=`grep " ${elements[$i]} " -n ${filename}_backup_run_seq | sed "s/:.*//g" | sed -n "2p"`
  n2nd_end=`grep " ${elements[$(($i+1))]} " -n ${filename}_backup_run_seq | sed "s/:.*//g" | sed -n "2p"`
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
  ./mkinp_baysian.sh ${elements[$i]} ${lattices[$i]}
  #---------------------------------------------------------------
  mv Evalute.txt ./${elements[$i]}/Evalute.txt
  mv Evalute_sort.txt ./${elements[$i]}/Evalute_sort.txt
  mv logs.json   ./${elements[$i]}/logs.json
  mv skdef.hsd.tmp_baysian_${elements[$i]} ./${elements[$i]}/skdef.hsd.tmp_baysian_${elements[$i]}
  mv baysian_v1_${elements[$i]}.py ./${elements[$i]}/baysian_v1_${elements[$i]}.py
  #---------------------------------------------------------------
done
#-------------------------------------------------------------------------