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
set trange [25:-5]

# plot
set terminal png
set output "band.png"
set title "SC: M-R-G-X-M-G-R"
set grid y
set ytics 2.5
unset xtics
unset yrange
set ylabel "Binding Energy / eV"
set yrange [25:-5] reverse
set xzeroaxis
plot "band.plot" u 1:(ef-$2) w p pt 7 ps 0.6 t "DFTB" , \
  11,t with lines title "" lw 1 lc rgb "gray", \
  31,t with lines title "" lw 1 lc rgb "gray", \
  41,t with lines title "" lw 1 lc rgb "gray", \
  51,t with lines title "" lw 1 lc rgb "gray", \
  71,t with lines title "" lw 1 lc rgb "gray", \
  91,t with lines title "" lw 1 lc rgb "gray"