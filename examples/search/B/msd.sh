#!/bin/bash

join dftbp_band.dat qe_bands.dat > msd_band.dat

ytop=-2
ybottom=16

echo "---------------------------------"
if [ ! "$1" == "" ]; then
  Temp=$1
else
  echo "---------------------------------"
  echo "Auto set 10000 K"
  Temp=10000.0 # [K]
fi
kbT=`echo ${Temp} | awk '{printf "%f",(8.6173e-5*$1)}'`
echo "kbT = "${kbT}" [eV] at ${Temp} [K]"
kbT3=`echo ${kbT} | awk '{printf "%f",(3.0*$1)}'`
echo "3*kbT = "${kbT3}" [eV] at ${Temp} [K]"

awk -v ybottom=${ybottom} -v ytop=${ytop} -v kbT=${kbT} '
BEGIN{n=0;VD=0.0;VDT=0.0;eta=0.0}
{
  if(ybottom>$3 && $3>ytop){
    VD=VD+($3-$2)^2
    n=n+1
    VDT=VDT+($3-$2)^2*exp(-((($2)^2)^0.5)/(3.0*kbT))
    ETA=ETA+(($3-$2)^2)^0.5
  }
}END{
  printf "---------------------------------\n"
  SD=(VD/n)^0.5
  printf "Standard diviation (SD) = %f [eV]\n",SD
  printf "---------------------------------\n"
  SDT=(VDT/n)^0.5
  printf "SDT = %f [eV] \n",SDT
  printf "---------------------------------\n"
  printf "SDT = sqrt(sum(VDT)/n) \n"
  printf "VDT = (E(DFT)-E(DFTB))^2*exp(-|E(DFTB)-EF|/(3.0*kbT)) \n"
  printf "3*kbT = %f [eV] \n",(3.0*kbT)
  printf "---------------------------------\n"
  printf "ETA = %f [eV]\n",(ETA/n)
  printf "ETA = sum(|E(DFT)-E(DFTB)|)/n \n"
  printf "---------------------------------\n"
}' msd_band.dat | tee msd.dat

echo "gnuplot"
echo "set yrange[${ybottom}:${ytop}]"
echo "set xzeroaxis"
echo "set arrow 1 nohead from 1,${kbT3} to 81,${kbT3} lt 2 lc \"red\""
echo "set arrow 2 nohead from 1,-${kbT3} to 81,-${kbT3} lt 2 lc \"blue\""
echo "plot \"msd_band.dat\" u 1:2 w l t \"DFTB\", \"msd_band.dat\" u 1:3 w l t \"QE(DFT)\""
echo "quit"
echo "---------------------------------"

