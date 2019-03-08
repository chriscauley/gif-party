SOURCE="logo_rotate_500"
DIR=".cache"
NROT=6

rm -rf $DIR
mkdir $DIR
mkdir $DIR/$SOURCE

convert $SOURCE.gif $DIR/$SOURCE.png
NUM=`ls $DIR/$SOURCE*.png|wc -l`

for i in `seq $NUM`
do
    HUE=$((100*i*NROT/NUM))
    N=`printf %03d $i`
    echo $HUE $N
    #echo $DIR/__spin-pw_$N.png
    convert $DIR/$SOURCE-$((i-1)).png -shave 90 $DIR/$SOURCE-$((i-1)).png
    convert $DIR/$SOURCE-$((i-1)).png -modulate 100,100,$HUE $DIR/$SOURCE/__frame_$N.png
done

convert -delay 2 -loop 0 $DIR/$SOURCE/*.png party-$SOURCE.gif
