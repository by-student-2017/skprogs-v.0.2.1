#!/bin/bash

export OMP_NUM_THREADS=1

echo "---------- SCF calculation ----------"
cp dftb_in_scf.hsd dftb_in.hsd
mpirun -np 1 dftb+ < dftb_in.hsd > dftb_out_scf.hsd

echo "---------- Get Fermi level ----------"
grep "Fermi level:"  < detailed.out >  info.dat
grep "Total energy:" < detailed.out >> info.dat

echo "---------- Band calculation ----------"
cp dftb_in_band.hsd dftb_in.hsd
mpirun -np 1 dftb+ < dftb_in.hsd > dftb_out_band.hsd

echo "---------- plot (gnuplot) ----------"
grep -v "KPT" band.out > band.dat
gnuplot band_BCC.gp
./conv_dftbp_band.sh
gnuplot comp_band_BCC.gpl

echo "---------- Delete files ----------"
rm -f dftb_in.hsd
rm -f dftb_out_scf.hsd
rm -f dftb_out_band.hsd
rm -f dftb_pin.hsd
rm -f charges.bin
rm -f detailed.out
rm -f band.out
rm -f info_gnu.dat
rm -f band.plot

echo "---------- Evaluate DS ----------"
./msd.sh

echo "---------- Ende ----------"
