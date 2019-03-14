if [[ $# -eq 0 ]] ; then
    echo "first argument should be a file"
    exit 0
fi

ROOT="dist"

FILENAME=$(basename -- "$1")
EXT="${FILENAME##*.}"
FILENAME="${FILENAME%.*}"
shift

N_FRAMES=12
HUE_RATE=6
DELAY=10

while [ "$1" != "" ]; do
    case $1 in
        -n | --number )
            shift
            N_FRAMES=$1
            ;;
        -h | --hue-rate )
            shift
            HUE_RATE=$1
            ;;
        -d | --delay )
            shift
            DELAY=$1
            ;;
        -i | --interactive )
            interactive=1
            ;;
        -c | --clear )
            clear=1
            ;;
        -b | --brighten )
            shift
            BRIGHTEN=$1
            ;;
        --negate )
            shift
            NEGATE=$1
            ;;
        -g | --gif)
            SOURCE_IS_GIF=1
        # -h | --help )
        #     usage
        #     exit
        #     ;;
        # * )                     usage
        #                         exit 1
    esac
    shift
done

if [ "$clear" = "1" ]
   then
       echo "cleared cache directory"
       rm -rf $ROOT
       mkdir $ROOT
fi

function _new_dir () {
    DIR="$ROOT/$FILENAME/$1"
    mkdir -p $DIR
    export SOURCE_2="$DIR/$FILENAME.$EXT"
}

rm -rf $ROOT/$FILENAME
mkdir -p $ROOT/$FILENAME

_new_dir 00-source
cp $FILENAME.$EXT $DIR
SOURCE="$DIR/$FILENAME.$EXT"

if [ ! -z "$BRIGHTEN" ]
   then
       _new_dir 02-brighten
       convert $SOURCE -modulate $BRIGHTEN% $SOURCE_2
       SOURCE=$SOURCE_2
       echo "brightened image"
fi

if [ ! -z "$NEGATE" ]
   then
       _new_dir 02-negate
       convert $SOURCE -channel $NEGATE -negate $SOURCE_2
       SOURCE=$SOURCE_2
       echo "negated image"
fi

_new_dir 03-hue_rotate
for i in `seq $N_FRAMES`
do
    HUE=$((200*i/$HUE_RATE))
    N=`printf %03d $i`
    convert $SOURCE -modulate 100,100,$HUE $DIR/$N.png
done

convert -delay $DELAY -loop 0 $DIR/*.png $ROOT/$FILENAME/party.gif

cd $ROOT
echo */ > gifs.log
cd $FILENAME
find . -type f -print |grep -v /files.log > files.log
echo */ > directories.log

