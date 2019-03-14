if [[ $# -eq 0 ]] ; then
    echo "first argument should be a file"
    exit 0
fi

ROOT=".cache"

filename=$(basename -- "$1")
extension="${filename##*.}"
filename="${filename%.*}"
shift

nframes=12
hue_rate=6
delay=10

while [ "$1" != "" ]; do
    case $1 in
        -n | --number )
            shift
            nframes=$1
            ;;
        -h | --hue-rate )
            shift
            hue_rate=$1
            ;;
        -d | --delay )
            shift
            delay=$1
            ;;
        -i | --interactive )
            interactive=1
            ;;
        -c | --clear )
            clear=1
            ;;
        -b | --brighten )
            shift
            brighten=$1
            ;;
        --negate )
            shift
            negate=$1
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

if [ "$clear" = "1" ]
   then
       echo "cleared cache directory"
       rm -rf $ROOT
       mkdir $ROOT
fi

function _done () {
    cat $html_file
    python -m SimpleHTTPServer 8756
    exit
}

function _new_dir () {
    _h4 $1
    $DIR=$ROOT/$filename$/$1
    export SOURCE=$DIR/$filename.$extension
}

function _h4 () {
    echo "</div><div><h4>$1</h4>" >> "$html_file"
}

function _img () {
    echo "<img title='$1' src='../$1'/>" >> "$html_file"
}

mkdir -p $ROOT/$filename
rm -f $ROOT/$filename/*

html_file="$ROOT/$filename.html"
echo "<div style='display:flex;justify-content: space-between'><div>" >  $html_file

SOURCE="$ROOT/$filename.$extension"
cp $filename.$extension $SOURCE
_h4 $SOURCE
_img $SOURCE

if [ ! -z "$brighten" ]
   then
       SOURCE_2=`_new_dir brighten`
       convert $SOURCE -modulate $brighten% $SOURCE_2
       SOURCE=$SOURCE_2
       echo "brightened image"
       _img $SOURCE
fi

if [ ! -z "$negate" ]
   then
       convert $SOURCE -channel $negate -negate $SOURCE
       echo "negated image"
fi

for i in `seq $nframes`
do
    HUE=$((200*i/$hue_rate))
    N=`printf %03d $i`
    convert $SOURCE -modulate 100,100,$HUE $ROOT/$filename/$N.png
done

convert -delay $delay -loop 0 $ROOT/$filename/*.png party-$filename.gif
_done

