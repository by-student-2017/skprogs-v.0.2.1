#!/bin/bash

# Usage
# 1. chmod +x mkinp.sh
# 2. ./mkinp.sh Sr FCC

if [ ! -e $1 ]; then
  cp -f -r ./../../band_check/*_$1_$2 ./$1
  cp baysian_v1_msd.sh ./$1/msd.sh
fi

filename="skdef.hsd"
if [ -f ${filename}_backup ]; then
  cp ${filename}_backup ${filename}
else
  cp ${filename} ${filename}_backup
fi

python_filename="baysian_v1_tmp.py"
grep -v '^\s*#' ${filename} > new_${filename}
filename=new_${filename}

#-----------------------------------------------------------
n1st=`grep $1 -n ${filename} | sed "s/:.*//g" | sed -n "1p"`
#echo ${n1st}

sed   "s/element_Xx/$1/g" ${python_filename} > baysian_v1_$1.py
atomic_number=`awk -v n1st=${n1st} '{if(NR==n1st+2){printf "%4.1f",$3}}' ${filename}`
sed -i "s/atomic_number_Yy/${atomic_number}/g" baysian_v1_$1.py

n1st_dftbatom=`awk -v n1st=${n1st} 'BEGIN{n=0}
{if(n1st<=NR && n==0 && $1=="DftbAtom"){n=NR}}
END{printf "%d",n}' ${filename}`

#echo ${n1st_dftbatom}

awk -v n1st_dftbatom=${n1st_dftbatom} '{
  if(NR==n1st_dftbatom+2){printf "      DensityCompression = PowerCompression{ Power = sigma_den; Radius = r0_den }\n"}
  else if(NR==n1st_dftbatom+4){printf "        D = PowerCompression { Power = sigma_d; Radius = r0_d }\n"}
  else if(NR==n1st_dftbatom+5){printf "        P = PowerCompression { Power = sigma_p; Radius = r0_p }\n"}
  else if(NR==n1st_dftbatom+6){printf "        S = PowerCompression { Power = sigma_s; Radius = r0_s }\n"}
  else {print $0}
}' ${filename} > skdef.hsd.tmp_baysian_1st

#----------
x0=`awk -v n1st_dftbatom=${n1st_dftbatom} '{
  if(NR==n1st_dftbatom+2 && $5=="="){printf "%4.1f",$6}
  else if(NR==n1st_dftbatom+2 && $6=="="){printf "%4.1f",$7}
}' ${filename}`
x1=`awk -v n1st_dftbatom=${n1st_dftbatom} '{
  if(NR==n1st_dftbatom+2 && $8=="="){printf "%4.1f",$9}
  else if(NR==n1st_dftbatom+2 && $9=="="){printf "%4.1f",$10}
}' ${filename}`
#----------
x2=`awk -v n1st_dftbatom=${n1st_dftbatom} '{
       if(NR==n1st_dftbatom+4 && $1=="S" && $5=="="){printf "%4.1f",$6}
  else if(NR==n1st_dftbatom+4 && $1=="S" && $6=="="){printf "%4.1f",$7}
  else if(NR==n1st_dftbatom+5 && $1=="S" && $5=="="){printf "%4.1f",$6}
  else if(NR==n1st_dftbatom+5 && $1=="S" && $6=="="){printf "%4.1f",$7}
  else if(NR==n1st_dftbatom+6 && $1=="S" && $5=="="){printf "%4.1f",$6}
  else if(NR==n1st_dftbatom+6 && $1=="S" && $6=="="){printf "%4.1f",$7}
}' ${filename}`
x3=`awk -v n1st_dftbatom=${n1st_dftbatom} '{
       if(NR==n1st_dftbatom+4 && $1=="S" &&  $9=="="){printf "%4.1f",$10}
  else if(NR==n1st_dftbatom+4 && $1=="S" && $10=="="){printf "%4.1f",$11}
  else if(NR==n1st_dftbatom+5 && $1=="S" &&  $9=="="){printf "%4.1f",$10}
  else if(NR==n1st_dftbatom+5 && $1=="S" && $10=="="){printf "%4.1f",$11}
  else if(NR==n1st_dftbatom+6 && $1=="S" &&  $9=="="){printf "%4.1f",$10}
  else if(NR==n1st_dftbatom+6 && $1=="S" && $10=="="){printf "%4.1f",$11}
}' ${filename}`
#----------
x4=`awk -v n1st_dftbatom=${n1st_dftbatom} '{
       if(NR==n1st_dftbatom+4 && $1=="P" && $5=="="){printf "%4.1f",$6}
  else if(NR==n1st_dftbatom+4 && $1=="P" && $6=="="){printf "%4.1f",$7}
  else if(NR==n1st_dftbatom+5 && $1=="P" && $5=="="){printf "%4.1f",$6}
  else if(NR==n1st_dftbatom+5 && $1=="P" && $6=="="){printf "%4.1f",$7}
  else if(NR==n1st_dftbatom+6 && $1=="P" && $5=="="){printf "%4.1f",$6}
  else if(NR==n1st_dftbatom+6 && $1=="P" && $6=="="){printf "%4.1f",$7}
}' ${filename}`
x5=`awk -v n1st_dftbatom=${n1st_dftbatom} '{
       if(NR==n1st_dftbatom+4 && $1=="P" &&  $9=="="){printf "%4.1f",$10}
  else if(NR==n1st_dftbatom+4 && $1=="P" && $10=="="){printf "%4.1f",$11}
  else if(NR==n1st_dftbatom+5 && $1=="P" &&  $9=="="){printf "%4.1f",$10}
  else if(NR==n1st_dftbatom+5 && $1=="P" && $10=="="){printf "%4.1f",$11}
  else if(NR==n1st_dftbatom+6 && $1=="P" &&  $9=="="){printf "%4.1f",$10}
  else if(NR==n1st_dftbatom+6 && $1=="P" && $10=="="){printf "%4.1f",$11}
}' ${filename}`
#----------
x6=`awk -v n1st_dftbatom=${n1st_dftbatom} '{
       if(NR==n1st_dftbatom+4 && $1=="D" && $5=="="){printf "%4.1f",$6}
  else if(NR==n1st_dftbatom+4 && $1=="D" && $6=="="){printf "%4.1f",$7}
  else if(NR==n1st_dftbatom+5 && $1=="D" && $5=="="){printf "%4.1f",$6}
  else if(NR==n1st_dftbatom+5 && $1=="D" && $6=="="){printf "%4.1f",$7}
  else if(NR==n1st_dftbatom+6 && $1=="D" && $5=="="){printf "%4.1f",$6}
  else if(NR==n1st_dftbatom+6 && $1=="D" && $6=="="){printf "%4.1f",$7}
}' ${filename}`
x7=`awk -v n1st_dftbatom=${n1st_dftbatom} '{
       if(NR==n1st_dftbatom+4 && $1=="D" &&  $9=="="){printf "%4.1f",$10}
  else if(NR==n1st_dftbatom+4 && $1=="D" && $10=="="){printf "%4.1f",$11}
  else if(NR==n1st_dftbatom+5 && $1=="D" &&  $9=="="){printf "%4.1f",$10}
  else if(NR==n1st_dftbatom+5 && $1=="D" && $10=="="){printf "%4.1f",$11}
  else if(NR==n1st_dftbatom+6 && $1=="D" &&  $9=="="){printf "%4.1f",$10}
  else if(NR==n1st_dftbatom+6 && $1=="D" && $10=="="){printf "%4.1f",$11}
}' ${filename}`
#----------
sed -i "s/x0_Zz/${x0}/g" baysian_v1_$1.py
sed -i "s/x1_Zz/${x1}/g" baysian_v1_$1.py
sed -i "s/x2_Zz/${x2}/g" baysian_v1_$1.py
sed -i "s/x3_Zz/${x3}/g" baysian_v1_$1.py
sed -i "s/x4_Zz/${x4}/g" baysian_v1_$1.py
sed -i "s/x5_Zz/${x5}/g" baysian_v1_$1.py
sed -i "s/x6_Zz/${x6}/g" baysian_v1_$1.py
sed -i "s/x7_Zz/${x7}/g" baysian_v1_$1.py
#----------
#-----------------------------------------------------------
n2nd=`grep $1 -n skdef.hsd.tmp_baysian_1st | sed "s/:.*//g" | sed -n "2p"`
#echo ${n2nd}

awk -v n2nd=${n2nd} '{
       if(NR==n2nd+4){printf "    S = stos \n"}
  else if(NR==n2nd+5){printf "    P = stop \n"}
  else if(NR==n2nd+6){printf "    D = stod \n"}
  else {print $0}
}' skdef.hsd.tmp_baysian_1st > skdef.hsd.tmp_baysian_$1
sed -i "s/skdef.hsd.tmp_baysian/skdef.hsd.tmp_baysian_$1/g" baysian_v1_$1.py
#----------------------------------------------------------
rm -f skdef.hsd.tmp_baysian_1st
rm -f ${filename}
#----------------------------------------------------------
python3 baysian_v1_$1.py
#----------------------------------------------------------
