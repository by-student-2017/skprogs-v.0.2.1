# get data size
stats "band.dat" using 1 nooutput
TN = STATS_records   # total number of lines
BN = STATS_blank 
PN = TN/BN

# declare Array
array data[TN]

# save
stats "band.dat" using (data[$0+1] = $2, 0) nooutput

# arrange data
set print "band.plot"
do for [i=1:BN]{
  do for [j=PN*(i-1)+1:PN*i]{
    print i,data[j]
  }
}

# get fermi energy data
set table "info_gnu.dat"
plot "info.dat" u 3:5 w p
stats "info_gnu.dat"
NI = STATS_records
array EF[NI]
stats "info_gnu.dat" using (EF[$0+1] = $2, 0) nooutput
ef = EF[1]
unset table

set parametric
set trange [8:-12]

# plot
set terminal png
set output "band.png"
set title "BCC: P-N-G-H-P-G-N"
set grid y
set ytics 2
unset xtics
unset yrange
set ylabel "Binding Energy / eV"
set yrange [8:-12] reverse
set xzeroaxis
plot "band.plot" u 1:(ef-$2) w p pt 7 ps 0.6 t "DFTB" , \
  11,t with lines title "" lw 1 lc rgb "gray", \
  21,t with lines title "" lw 1 lc rgb "gray", \
  41,t with lines title "" lw 1 lc rgb "gray", \
  61,t with lines title "" lw 1 lc rgb "gray", \
  71,t with lines title "" lw 1 lc rgb "gray", \
  81,t with lines title "" lw 1 lc rgb "gray"