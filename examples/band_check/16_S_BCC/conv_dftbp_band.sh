#!/bin/bash

EF=`awk '{if($1=="Fermi"){printf "%f",$5}}' info.dat`
echo "Fermi energy = ${EF} [eV] from info.dat"

nband=`awk -v max=0 '{if($1>max){max=$1}}END{print max} ' band.dat`
echo "Number of band = ${nband}"

echo -n > dftbp_band.dat 

for i in `seq ${nband}`
do
  awk -v nband=${i} -v EF=${EF} '
  BEGIN {nL=0}
  {
    if($1==nband){
      nL=nL+1;
      printf "%d %f \n",nL,(EF-$2);}
  }
  END {printf "\n"}' band.dat >> dftbp_band.dat
done

#cat dftbp_bands.dat

