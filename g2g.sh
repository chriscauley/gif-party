# this is useful for tweaking image
# convert logo_rotate_500.gif -coalesce -repage 0x0 -shave 80 -thumbnail 100 +repage logo_rotate_100.gif

SOURCE="logo_rotate_100"
DIR=".cache"
NROT=6
SLICE=8

rm -rf $DIR
mkdir $DIR
mkdir $DIR/$SOURCE

convert $SOURCE.gif $DIR/$SOURCE.png
NUM=`ls $DIR/$SOURCE*.png|wc -l`

for i in `seq 1 $SLICE $NUM`
do
    SFILE=$DIR/$SOURCE-$((i-1)).png
    HUE=$((100*i*NROT/NUM))
    N=`printf %03d $i`
    #echo $DIR/__spin-pw_$N.png
    #convert $SFILE -shave 80 $SFILE
    convert $SFILE -modulate 100,100,$HUE $DIR/$SOURCE/__frame_$N.png
done

convert -delay 8 -loop 0 $DIR/$SOURCE/*.png party-$SOURCE.gif
