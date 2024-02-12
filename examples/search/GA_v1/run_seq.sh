#!/bin/bash

#-------------------------------------------------------------------------
elements=(Xx
  H                                                                   He
  Li  Be                                           B   C   N   O   F  Ne
  Na  Mg                                          Al  Si   P   S  Cl  Ar
  K   Ca  Sc  Ti   V  Cr  Mn  Fe  Co  Ni  Cu  Zn  Ga  Ge  As  Se  Br  Kr
  Rb  Sr   Y  Zr  Nb  Mo  Tc  Ru  Rh  Pd  Ag  Cd  In  Sn  Sb  Te   I  Xe
  Cs  Ba  La  Hf  Ta   W  Re  Os  Ir  Pt  Au  Hg  Tl  Pb  Bi)
#-------------------------------------------------------------------------
lattices=(YY
  SC                                                                  SC
  BCC HCP                                         SC  HCP SC  SC  SC  FCC
  BCC HCP                                         FCC FCC SC  SC  SC  FCC
  BCC FCC HCP HCP BCC BCC BCC BCC HCP FCC FCC HCP BCC FCC SC  SC  SC  FCC
  BCC FCC HCP HCP BCC BCC HCP HCP FCC FCC FCC HCP BCC FCC SC  SC  SC  FCC
  BCC BCC FCC HCP BCC BCC FCC HCP FCC FCC FCC SCC HCP FCC BCC)
#-------------------------------------------------------------------------
nelement=(0
  1                                                                    2
  3   4                                            5   6   7   8   9  10
  11  12                                          13  14  15  16  17  18
  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35  36
  37  38  39  40  41  42  43  44  45  46  47  48  49  50  51  52  53  54
  55  56  57  72  73  74  75  76  77  78  79  80  81  82  83)
#-------------------------------------------------------------------------
ndata=${#elements[@]}
#echo ${ndata}
#-------------------------------------------------------------------------
#for((i=1;i<${ndata};i++)); do
#for((i=19;i<${ndata};i++)); do
#for((i=37;i<39;i++)); do
for i in 38 47; do # Sr, Ag
  echo $i", "${nelement[$i]}", "${elements[$i]}", "${lattices[$i]}
  ./mkinp_ga.sh ${elements[$i]} ${lattices[$i]}
  #---------------------------------------------------------------
  mv Evalute.txt ./${elements[$i]}/Evalute.txt
  mv logs.json   ./${elements[$i]}/logs.json
  mv skdef.hsd.tmp_ga_${elements[$i]} ./${elements[$i]}/skdef.hsd.tmp_ga_${elements[$i]}
  mv ga_v1_${elements[$i]}.py ./${elements[$i]}/ga_v1_${elements[$i]}.py
  #---------------------------------------------------------------
done
#-------------------------------------------------------------------------