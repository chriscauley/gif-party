if [[ $# -eq 0 ]] ; then
    echo "first argument should be a file"
    exit 0
fi

OG_SOURCE=$1
FILENAME=$(basename -- "$1")
EXT="${FILENAME##*.}"
FILENAME="${FILENAME%.*}"
mkdir -p .media/.party/
ROOT=`realpath .media/.party/`
mkdir -p $ROOT/$FILENAME.$EXT/$2
DEST=`realpath $ROOT/$FILENAME.$EXT/$2`
shift
shift

N_FRAMES=24
DELAY=2

while [ "$1" != "" ]; do
    case $1 in
        -r | --resize )
            shift
            RESIZE=$1
            ;;
        -n | --number )
            shift
            N_FRAMES=$1
            ;;
        -h | --hue-rate )
            HUE_RATE=$N_FRAMES
            ;;
        -d | --delay )
            shift
            DELAY=$1
            ;;
        -i | --interactive )
            interactive=1
            ;;
        -b | --brighten )
            shift
            BRIGHTEN=$1
            ;;
        -N | --negate )
            shift
            NEGATE=$1
            ;;
        -g | --gif)
            GIF_SPLIT=1
        # -h | --help )
        #     usage
        #     exit
        #     ;;
        # * )                     usage
        #                         exit 1
    esac
    shift
done

function _new_dir () {
    DIR="$DEST/$1"
    mkdir -p $DIR
    export SOURCE_2="$DIR/$FILENAME.$EXT"
}

rm -rf $DEST
mkdir -p $DEST

_new_dir 00-source
cp $OG_SOURCE $DIR
SOURCE="$DIR/$FILENAME.$EXT"
if [ ! -z "$GIF_SPLIT" ]
then
    _new_dir 10-gif_split
    convert $SOURCE $DIR/$FILENAME-%02d.png
    GIF_DIR=$DIR
fi

if [ ! -z "$RESIZE" ]
then
    _new_dir 20-resize
    convert $SOURCE -resize $RESIZE $SOURCE_2
    SOURCE=$SOURCE_2
    echo resized $RESIZE
fi

if [ ! -z "$NEGATE" ]
   then
       _new_dir 30-negate
       convert $SOURCE -channel $NEGATE -negate $SOURCE_2
       SOURCE=$SOURCE_2
       echo negated $NEGATE
fi

if [ ! -z "$BRIGHTEN" ]
   then
       _new_dir 40-brighten
       convert $SOURCE -modulate $BRIGHTEN% $SOURCE_2
       SOURCE=$SOURCE_2
       echo brigtened $BRIGHTEN
fi

if [ ! -z "$GIF_SPLIT" ]
then
    set -- `ls $GIF_DIR`
fi
if [ ! -z "$HUE_RATE" ]
then
    _new_dir 50-hue_rotate
    for i in `seq $N_FRAMES`
    do
        HUE=$((200*i/$HUE_RATE))
        N=`printf %03d $i`
        S=$SOURCE
        if [ ! -z "$GIF_SPLIT" ]
        then
            S=$GIF_DIR/$1
            shift
        fi
        convert $S -modulate 100,100,$HUE $DIR/$N-$HUE.png
    done
fi

echo delaying gif - $DELAY
convert -delay $DELAY -dispose previous -loop 0 $DIR/*.png $DEST/party.gif
echo $DIR
cd $ROOT
echo */ > gifs.log
find . -type f -print |grep -v /files.log > files.log
echo */ > directories.log

