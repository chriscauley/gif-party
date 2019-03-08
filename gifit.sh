echo $1
rm -f __spin-*.png
rm -f __no_spin-*.png

DIR=".cache"

echo $DIR
for i in `seq 12`
do
    HUE=$((100*i/6))
    ROT=$((720*i/16))
    N=`printf %02d $i`
    echo $HUE $ROT $N
    echo $DIR/__spin-pw_$N.png
    convert favicon.png -rotate $ROT -modulate 100,100,$HUE $DIR/__spin-pw_$N.png
    convert favicon.png -rotate $ROT -modulate 100,100,$HUE $DIR/__no_spin-pw_$N.png
done
exit
convert -delay 10 -loop 0 $DIR__spin-*.png pw-spin.gif
convert -delay 10 -loop 0 $DIR__no_spin-*.png pw.gif