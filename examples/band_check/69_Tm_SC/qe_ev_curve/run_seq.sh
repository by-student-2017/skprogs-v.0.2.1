#!/bin/bash

#-------------------------------------------------------------------------
sym=SC # e.g., FCC, BCC, HCP, SC

export OMP_NUM_THREADS=1
NCPU=`grep 'core id' /proc/cpuinfo | sort -u | wc -l`
echo "Number of CPUs: "${NCPU}
MPI_PREFIX="mpirun -np ${NCPU}"
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
cp -r ./../qe ./qe_vS

if [ ! -d qe_bands_series ]; then
  mkdir qe_bands_series
fi

if [ ! -e ve.data ]; then
  echo "# V(Angstrom^3), Etot(Ry), La(Angstrom), dV(%)" > ve.data
fi
#-------------------------------------------------------------------------
for dv in -20 -14 -10 -8 -6 -4 -2 -1 0 1 2 4 6 8 10 14 20 26; do
#for dv in -6 -4 -2  0  2  4  6 ; do
  #---------------------------------------------------------------
  if [ ! -e qe_v${dv} ]; then
    #---------------------------------------------------------------
    cp -r qe_vS qe_v${dv}
    cd qe_v${dv}
    #---------------------------------------------------------------
    cif2cell -p pwscf --pwscf-nbnd=26 --pwscf-pseudo-PSLibrary-libdr='./../../../../pseudo/psl100_PBE' --setup-all --k-resolution=0.20 --pwscf-spin=no --pwscf-run-type=scf -f POSCAR.cif
    mv POSCAR.cif POSCAR_vS.cif
    #---------------------------------------------------------------
    awk -v dv=${dv} '{
             if($1=="_cell_length_a"){printf "%s                     %12.6f \n",$1,$2*(1+dv/100)^(1/3)}
        else if($1=="_cell_length_b"){printf "%s                     %12.6f \n",$1,$2*(1+dv/100)^(1/3)}
        else if($1=="_cell_length_c"){printf "%s                     %12.6f \n",$1,$2*(1+dv/100)^(1/3)}
        else if($1=="_cell_volume")  {printf "%s                     %15.6f \n",$1,$2*(1+dv/100)}
        else {print $0}
    }' POSCAR_vS.cif > POSCAR_v${dv}.cif
    cp POSCAR_v${dv}.cif POSCAR.cif
    #---------------------------------------------------------------
    awk -v dv=${dv} '{
        if($1=="A" && $2=="="){printf "  A = %10.5f",$3*(1+dv/100)^(1/3)}
        else {print $0}
    }' POSCAR.scf.in > POSCAR_v${dv}.scf.in
    cp POSCAR_v${dv}.scf.in POSCAR.scf.in
    #---------------------------------------------------------------
    awk -v dv=${dv} '{
        if($1=="A" && $2=="="){printf "  A = %10.5f",$3*(1+dv/100)^(1/3)}
        else {print $0}
    }' POSCAR.bands.in > POSCAR_v${dv}.bands.in
    cp POSCAR_v${dv}.bands.in POSCAR.bands.in
    #---------------------------------------------------------------
    #cif2cell -p pwscf --pwscf-nbnd=26 --pwscf-pseudo-PSLibrary-libdr='./../../../../pseudo/psl100_PBE' --setup-all --k-resolution=0.20 --pwscf-spin=no --pwscf-run-type=scf -f POSCAR.cif
    ${MPI_PREFIX} pw.x < POSCAR.scf.in | tee POSCAR.scf.out
    
    grep "Fermi" POSCAR.scf.out > info.dat
    
    ML=`grep -n K_POINTS POSCAR.scf.in | sed -e 's/:.*//g'`
    awk -v ML=${ML} '{if(NR<ML){print $0}}' POSCAR.scf.in > POSCAR.bands.in
    sed -i "s/scf/bands/" POSCAR.bands.in
    cat kpath_${sym}.txt >> POSCAR.bands.in
    
    ${MPI_PREFIX} pw.x < POSCAR.bands.in | tee POSCAR.bands.out
    
    ${MPI_PREFIX} bands.x < bands.in
    
    ./conv_qe_bands.sh
    #---------------------------------------------------------------
  else
    #---------------------------------------------------------------
    cd qe_v${dv}
    #---------------------------------------------------------------
  fi
    cp qe_bands.dat qe_bands_v${dv}.dat
    cp qe_bands.dat ./../qe_bands_series/qe_bands_v${dv}.dat
    grep "!    total energy" POSCAR.scf.out > total_energy.dat
    vol=`awk -v dv=${dv} '{if($1=="_cell_volume"){printf "%-15.6f",$2*(1+dv/100)}}' POSCAR_vS.cif`
    awk -v vol=${vol} -v dv=${dv} '{if(NR==1){printf "%15.6f %15.6f %15.6f %d \n",vol,$5,vol^(1/3),dv}}' total_energy.dat > v${dv}e.dat
    cat v${dv}e.dat >> ./../ve.data
    #---------------------------------------------------------------
    cd ./../
    #---------------------------------------------------------------
done
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
sort -k 1 -g -u -f ve.data > ve_sort.data # -n option for int case
mv ve_sort.data ve.data
gnuplot < veplot.gpl
cp ve.data ./qe_bands_series/ve.data
cp fit.log ./qe_bands_series/fit.log
#-------------------------------------------------------------------------
