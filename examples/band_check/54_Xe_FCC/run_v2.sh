#!/bin/bash

#sym=FCC # e.g., FCC, BCC, HCP, SC

export OMP_NUM_THREADS=1
#NCPU=`grep 'core id' /proc/cpuinfo | sort -u | wc -l`
#echo "Number of CPU: "${NCPU}
MPI_PREFIX="mpirun -np 1"

echo "---------- SCF calculation ----------"
cp dftb_in_scf.hsd dftb_in.hsd
${MPI_PREFIX} dftb+ < dftb_in.hsd > dftb_out_scf.hsd

echo "---------- Get Fermi level ----------"
grep "Fermi level:"  < detailed.out >  info.dat
grep "Total energy:" < detailed.out >> info.dat

echo "---------- Band calculation ----------"
cp dftb_in_band.hsd dftb_in.hsd
${MPI_PREFIX} dftb+ < dftb_in.hsd > dftb_out_band.hsd

echo "---------- Get Fermi level ----------"
EF1=`awk '{if($1=="Fermi"){printf "%f",$5}}' info.dat`
EF2=`awk 'BEGIN{EF=-30}{if($1!="KPT" && $2>EF && $3>0.0){EF=$2}}END{printf "%f",EF}' band.out`
echo ${EF1} ${EF2} | awk '{if( (($1-$2)^2)^0.5 >= 0.003 ){printf "Fermi level: %f H %f eV from band.out file \n",$2/(13.602*2),$2}}' > info.dat

echo "---------- plot (gnuplot) ----------"
grep -v "KPT" band.out > band.dat
#gnuplot band_${sym}.gp
./conv_dftbp_band.sh
#gnuplot < comp_band_${sym}.gpl
gnuplot < comp_band_*.gpl

echo "---------- Evaluate DS ----------"
./msd.sh

echo "---------- Delete files ----------"
rm -f dftb_in.hsd
rm -f dftb_out_scf.hsd
rm -f dftb_out_band.hsd
rm -f dftb_pin.hsd
rm -f charges.bin
rm -f detailed.out
#-----------------
rm -f info.dat
rm -f band.out
rm -f band.dat
rm -f info_gnu.dat
rm -f band.plot
rm -f msd_band.dat


echo "---------- Ende ----------"
