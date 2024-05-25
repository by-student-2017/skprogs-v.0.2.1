#!/bin/bash

#-----------------------------------------------------------------------------------
# Usage
# 1. chmod +x mkinp.sh
# 2. ./mkinp.sh Sr FCC 1.00
#-----------------------------------------------------------------------------------

if [ ! -e $1 ]; then
  cp -f -r ./../../band_check/*_$1_$2 ./$1
  #cp baysian_v1_msd.sh ./$1/msd.sh
fi

filename="skdef.hsd"
if [ -f ${filename}_backup_run_seq ]; then
  echo "run_seq.sh program"
elif [ -f ${filename}_backup ]; then
  cp ${filename}_backup ${filename}
else
  cp ${filename} ${filename}_backup
fi

python_filename="baysian_v1_tmp.py"
grep -v '^\s*#' ${filename} > new_${filename}
filename=new_${filename}

#-----------------------------------------------------------------------------------
n1st=`grep " $1 {" -n ${filename} | sed "s/:.*//g" | sed -n "1p"`
#echo ${n1st}

sed   "s/element_Xx/$1/g" ${python_filename} > baysian_v1_$1.py
atomic_number=`awk -v n1st=${n1st} '{if(NR==n1st+2){printf "%4.1f",$3}}' ${filename}`
sed -i "s/atomic_number_Yy/${atomic_number}/g" baysian_v1_$1.py

n1st_dftbatom=`awk -v n1st=${n1st} 'BEGIN{n=0}
{if(n1st<=NR && n==0 && $1=="DftbAtom"){n=NR}}
END{printf "%d",n}' ${filename}`

#echo ${n1st_dftbatom}

awk -v n1st_dftbatom=${n1st_dftbatom} '{
  if(NR==n1st_dftbatom+2){printf "      DensityCompression = PowerCompression{ Power = sigma; Radius = r0_den }\n"}
  #--------------
  else if(NR==n1st_dftbatom+4 && $1=="F"){printf "        F = PowerCompression { Power = sigma; Radius = r0_wav }\n"}
  else if(NR==n1st_dftbatom+5 && $1=="D"){printf "        D = PowerCompression { Power = sigma; Radius = r0_wav }\n"}
  else if(NR==n1st_dftbatom+6 && $1=="P"){printf "        P = PowerCompression { Power = sigma; Radius = r0_wav }\n"}
  else if(NR==n1st_dftbatom+7 && $1=="S"){printf "        S = PowerCompression { Power = sigma; Radius = r0_wav }\n"}
  #--------------
  else if(NR==n1st_dftbatom+4 && $1=="D"){printf "        D = PowerCompression { Power = sigma; Radius = r0_wav }\n"}
  else if(NR==n1st_dftbatom+5 && $1=="P"){printf "        P = PowerCompression { Power = sigma; Radius = r0_wav }\n"}
  else if(NR==n1st_dftbatom+6 && $1=="S"){printf "        S = PowerCompression { Power = sigma; Radius = r0_wav }\n"}
  #--------------
  else if(NR==n1st_dftbatom+4 && $1=="P"){printf "        P = PowerCompression { Power = sigma; Radius = r0_wav }\n"}
  else if(NR==n1st_dftbatom+5 && $1=="S"){printf "        S = PowerCompression { Power = sigma; Radius = r0_wav }\n"}
  #--------------
  else if(NR==n1st_dftbatom+4 && $1=="S"){printf "        S = PowerCompression { Power = sigma; Radius = r0_wav }\n"}
  #--------------
  else if(NR==n1st_dftbatom+5 && $1=="P"){printf "        P = PowerCompression { Power = sigma; Radius = r0_wav }\n"}
  else if(NR==n1st_dftbatom+6 && $1=="D"){printf "        D = PowerCompression { Power = sigma; Radius = r0_wav }\n"}
  else if(NR==n1st_dftbatom+7 && $1=="F"){printf "        F = PowerCompression { Power = sigma; Radius = r0_wav }\n"}
  #--------------
  else {print $0}
}' ${filename} > skdef.hsd.tmp_baysian_1st

mv skdef.hsd.tmp_baysian_1st skdef.hsd.tmp_baysian_$1
sed -i "s/skdef.hsd.tmp_baysian/skdef.hsd.tmp_baysian_$1/g" baysian_v1_$1.py

#----------
x0=`awk -v n1st_dftbatom=${n1st_dftbatom} '{
  if(NR==n1st_dftbatom+2 && $8=="="){printf "%4.1f",$9}
  else if(NR==n1st_dftbatom+2 && $9=="="){printf "%4.1f",$10}
  else if(NR==n1st_dftbatom+2 && $10=="="){printf "%4.1f",$11}
}' ${filename}`
#----------
x1=`awk -v n1st_dftbatom=${n1st_dftbatom} '{
  #--------------
       if(NR==n1st_dftbatom+4 && $1=="S" &&  $9=="="){printf "%4.1f",$10}
  else if(NR==n1st_dftbatom+4 && $1=="S" && $10=="="){printf "%4.1f",$11}
  #--------------
  else if(NR==n1st_dftbatom+5 && $1=="S" &&  $9=="="){printf "%4.1f",$10}
  else if(NR==n1st_dftbatom+5 && $1=="S" && $10=="="){printf "%4.1f",$11}
  #--------------
  else if(NR==n1st_dftbatom+6 && $1=="S" &&  $9=="="){printf "%4.1f",$10}
  else if(NR==n1st_dftbatom+6 && $1=="S" && $10=="="){printf "%4.1f",$11}
  #--------------
  else if(NR==n1st_dftbatom+7 && $1=="S" &&  $9=="="){printf "%4.1f",$10}
  else if(NR==n1st_dftbatom+7 && $1=="S" && $10=="="){printf "%4.1f",$11}
  #--------------
}' ${filename}`
#-----------------------------------------------------------------------------------
#New predict version
echo "Rcov "$3" [Angstrom]"
x0=`echo $3 | awk '{printf "%4.1f",16.0*($1/0.529)^(0.5)}'` # Al:36, K<19, V:23, Cr:14, Mn:20, Fe:17, Co:16, Ni:16, Cu:<10, Zn:<10, Ga:36
x1=`echo $3 | awk '{printf "%4.1f",(2.0*$1/0.529)}'`
#New predict version
#-----------------------------------------------------------------------------------
sed -i "s/x0_Zz/${x0}/g" baysian_v1_$1.py
sed -i "s/x1_Zz/${x1}/g" baysian_v1_$1.py
#----------
#-----------------------------------------------------------------------------------
rm -f skdef.hsd.tmp_baysian_1st
rm -f ${filename}
#-----------------------------------------------------------------------------------
python3 baysian_v1_$1.py
#-----------------------------------------------------------------------------------
