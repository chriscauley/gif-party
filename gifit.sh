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

STEP_COUNT=0
function _new_dir () {
    _SC=`printf %02d $STEP_COUNT`
    DIR="$DEST/${_SC}_$1"
    mkdir -p $DIR
    export SOURCE_2="$DIR/$FILENAME.$EXT"
    let "STEP_COUNT=STEP_COUNT+1"
}

rm -rf $DEST
mkdir -p $DEST

_new_dir source
cp $OG_SOURCE $DIR
SOURCE="$DIR/$FILENAME.$EXT"


# if it's a multi frame gif, force it to break up
GIF_N_FRAMES=`identify $SOURCE|wc -l`
if [ -z "$GIF_SPLIT" ] && [ "$GIF_N_FRAMES" -gt "1" ]
then
    echo Forcing gif split
    GIF_SPLIT=1
fi

if [ ! -z "$RESIZE" ]
then
    _new_dir resize
    convert $SOURCE -resize $RESIZE $SOURCE_2
    SOURCE=$SOURCE_2
    echo resized $RESIZE
fi

if [ ! -z "$NEGATE" ]
   then
       _new_dir negate
       convert $SOURCE -channel $NEGATE -negate $SOURCE_2
       SOURCE=$SOURCE_2
       echo negated $NEGATE
fi

if [ ! -z "$BRIGHTEN" ]
   then
       _new_dir brighten
       convert $SOURCE -modulate $BRIGHTEN% $SOURCE_2
       SOURCE=$SOURCE_2
       echo brigtened $BRIGHTEN
fi

if [ ! -z "$GIF_SPLIT" ]
then
    _new_dir gif_split
    convert $SOURCE $DIR/$FILENAME-%02d.png
    GIF_DIR=$DIR
    SOURCE=`ls $GIF_DIR`
    set -- `ls $GIF_DIR`
    N_FRAMES=$GIF_N_FRAMES

    # ifno delay, use original
    DELAY=${DELAY:=`identify -format "%T\n" $OG_SOURCE|head -n 1`}
fi

if [ ! -z "$HUE_RATE" ]
then
    _new_dir hue_rotate
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

DELAY=${DELAY:=4}

# create final gif
echo delaying gif - $DELAY
convert -delay $DELAY -dispose previous -loop 0 $DIR/*.png $DEST/party.gif

# reset log files which are used in the app to generate file tree
cd $ROOT
echo */ > gifs.log
find . -type f -print |grep -v /files.log > files.log
echo */ > directories.log

