set -e
if [[ $# -eq 0 ]] ; then
    echo "first argument should be a file"
    exit 0
fi

OG_SOURCE=`realpath $1`
FULLNAME=$(basename -- "$1")
EXT="${FULLNAME##*.}"
FILENAME="${FULLNAME%.*}"
mkdir -p .media/.party/
ROOT=`realpath $(pwd)`
DEST=`realpath .media/.party/$2`
mkdir -p $DEST
cd $DEST
shift
shift

N_FRAMES=7
N_COLORS=7
COLORS=("#e81d1d" "#e8b71d" "#e3e81d" "#1de840" "#1ddde8" "#2b1de8" "#dd00f3")

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
        -f | --fuzz )
            shift
            FUZZ=$1
            ;;
        -d | --delay )
            shift
            DELAY=$1
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
            shift
            ;;
        -R | --replace )
            shift
            REPLACE=$1
            ;;
        # -h | --help )
        #     usage
        #     exit
        #     ;;
        # * )                     usage
        #                         exit 1
    esac
    shift
done

function noop() {
    echo noop $@
}

# STEP_COUNT=0
function _new_dir () {
    DIR="$1"
    shift

    # let "STEP_COUNT=STEP_COUNT+1"
    if [[ ! -d "$DIR" ]];
    then
        mkdir -p $DIR
        pwd
        $@ "$DIR/$FULLNAME"
    else
        : # echo skipping because exists: $@ "$DIR/$FULLNAME"
    fi
    SOURCE=$(basename -- "$SOURCE")
    cd $DIR
}

SOURCE=$OG_SOURCE

# if it's a multi frame gif, force it to break up
GIF_N_FRAMES=`identify $SOURCE|wc -l`
if [ -z "$GIF_SPLIT" ] && [ "$GIF_N_FRAMES" -gt "1" ]
then
    _new_dir coalesce convert $SOURCE -coalesce -repage 0x0 +repage
    GIF_SPLIT=1
    echo coalesced
fi

if [ ! -z "$RESIZE" ]
then
    _new_dir resize=$RESIZE convert $SOURCE -resize $RESIZE
    echo resized $RESIZE
fi

if [ ! -z "$NEGATE" ]
then
    _new_dir negate=$NEGATE convert $SOURCE -channel $NEGATE -negate
    echo negated $NEGATE
fi

if [ ! -z "$BRIGHTEN" ]
then
    _new_dir brighten=$BRIGHTEN convert $SOURCE -modulate $BRIGHTEN%
    echo brigtened $BRIGHTEN
fi

if [ ! -z "$GIF_SPLIT" ]
then
    echo splitting gif
    _new_dir gif_split noop
    convert ../$SOURCE $FILENAME-%04d.png
    SOURCE=`ls`
    set -- `ls`
    N_FRAMES=$GIF_N_FRAMES

    # if no delay, use original
    _DELAYS=`identify -format "%T\n" $OG_SOURCE`
    DELAY=${DELAY:=`bash $ROOT/ave.sh $_DELAYS`}
fi

if [ ! -z "$REPLACE" ]
then
    _new_dir replace=$FUZZ noop
else
    _new_dir hue_rotate=$N_FRAMES noop
fi

for i in `seq $N_FRAMES`
do
    HUE=$((200*i/$N_FRAMES))
    N=`printf %04d $i`
    S=$SOURCE
    if [ ! -z "$GIF_SPLIT" ]
    then
        S=$1
        shift
    fi
    if [ ! -z "$REPLACE" ]
    then
        FUZZ=${FUZZ:=6}
        echo fuzzing $FUZZ%
        _IC=`expr $N % $N_COLORS`
        _COLOR=${COLORS[_IC]}
        convert ../$S -fuzz $FUZZ% -fill $_COLOR -opaque "$REPLACE" "$FILENAME__$N.png"
    else
        # "hue_rotate"
        convert ../$S -modulate 100,100,$HUE "$FILENAME__$N-$HUE.png"
    fi
done

DELAY=${DELAY:=4}

# create final gif
echo delay $DELAY
_new_dir gifit noop
convert -delay $DELAY -dispose previous -loop 0 ../*.png "$FILENAME.gif"
echo `pwd`/$FULLNAME