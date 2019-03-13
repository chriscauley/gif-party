if [[ $# -eq 0 ]] ; then
    echo "first argument should be a file"
    exit 0
fi

DIR=".cache"

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
       rm -rf $DIR
       mkdir $DIR
fi

function _html () {
    echo "<$1>$2</$1>" >> "$html_file"
}

function _img () {
    echo "<img title='$1' src='../$1'/>" >> "$html_file"
}

mkdir -p $DIR/$filename
rm -f $DIR/$filename/*

html_file="$DIR/$filename.html"
rm -f $html_file
touch $html_file

SOURCE="$DIR/$filename.$extension"
cp $filename.$extension $SOURCE
_html h4 $SOURCE
_img $SOURCE
open $html_file
exit
if [ ! -z "$brighten" ]
   then
       convert $SOURCE -modulate $brighten% $SOURCE
       echo "brightened image"
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
    convert $SOURCE -modulate 100,100,$HUE $DIR/$filename/$N.png
done

convert -delay $delay -loop 0 $DIR/$filename/*.png party-$filename.gif