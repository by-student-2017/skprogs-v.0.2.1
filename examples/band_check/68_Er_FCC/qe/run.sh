#!/bin/bash

sym=FCC # e.g., FCC, BCC, HCP, SC

export OMP_NUM_THREADS=1
NCPU=`grep 'core id' /proc/cpuinfo | sort -u | wc -l`
echo "Number of CPUs: "${NCPU}
MPI_PREFIX="mpirun -np ${NCPU}"

cif2cell -p pwscf --pwscf-nbnd=24 --pwscf-pseudo-PSLibrary-libdr='./../../../pseudo/psl100_PBE' --setup-all --k-resolution=0.20 --pwscf-spin=no --pwscf-run-type=scf -f POSCAR.cif
${MPI_PREFIX} pw.x < POSCAR.scf.in | tee POSCAR.scf.out

grep "Fermi" POSCAR.scf.out > info.dat

ML=`grep -n K_POINTS POSCAR.scf.in | sed -e 's/:.*//g'`
awk -v ML=${ML} '{if(NR<ML){print $0}}' POSCAR.scf.in > POSCAR.bands.in
sed -i "s/scf/bands/" POSCAR.bands.in
cat kpath_${sym}.txt >> POSCAR.bands.in

${MPI_PREFIX} pw.x < POSCAR.bands.in | tee POSCAR.bands.out

${MPI_PREFIX} bands.x < bands.in

./conv_qe_bands.sh
