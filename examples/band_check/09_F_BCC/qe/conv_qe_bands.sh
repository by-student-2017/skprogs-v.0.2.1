#!/bin/bash

EF=`awk '{printf "%f",$5}' info.dat`
echo "Fermi energy = ${EF} [eV] from info.dat"

ytop=-25
ybottom=25

awk -v EF=${EF} -v ytop=${ytop} -v ybottom=${ybottom} '
  BEGIN {nL=0; flag=0}
  {
    if( $2=="" ){ nL=NR }
    if( $2=="" && flag==1 ){ print $0 }
    if( (EF-$2)<ybottom && (EF-$2)>ytop && (NR-nL)>=1){
      printf "%d %f \n",(NR-nL),(EF-$2)
      flag=1
    }
  }
  END {}' POSCAR.bands.gnu > qe_bands.dat

#cat qe_bands.dat

