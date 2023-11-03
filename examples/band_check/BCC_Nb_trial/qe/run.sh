#!/bin/bash

export OMP_NUM_THREADS=1
MPI_PREFIX="mpirun -np 1"

#cif2cell -p pwscf --pwscf-pseudo-PSLibrary-libdr='./../../../pseudo/psl100_PBE' --setup-all --k-resolution=0.20 --pwscf-spin=no --pwscf-run-type=scf -f *.cif
${MPI_PREFIX} pw.x < POSCAR.scf.in | tee POSCAR.scf.out

grep "Fermi" POSCAR.scf.out > info.dat

${MPI_PREFIX} pw.x < POSCAR.bands.in | tee POSCAR.bands.out

${MPI_PREFIX} bands.x < bands.in

