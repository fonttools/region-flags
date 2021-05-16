#!/usr/bin/env sh

echo "Options: w, width, h, height, n, normal, default"
echo -n "Enter your option: "
read OPTION

echo ""

echo "Options: yes, true, 1"
echo -n "Do you want to optimize the converted file? "
read OPTIPNGOP

updatealiases(){
    echo "Updating aliases!"
    IFS='	'
    while read dst src; do
        for dir in png; do
            s="$dir/$src.$dir"
            d="$dir/$dst.$dir"
            cp -f "$s" "$d"
        done
    done < data/ALIASES
}

rsvgconvert() {
    case $OPTIPNGOP in
        "yes" | "true" | "1")
            echo "Converting svg/$region.svg to png/$region.png.tmp"
            if ! rsvg-convert $1 -f png -o "png/$region.png.tmp" "svg/$region.svg"; then
                echo "ERROR rsvg-convert failed."
                rm -f "png/$region.png.tmp"
            else
                echo "Optimizing png/$region.png!"
                if !  optipng -quiet "png/$region.png.tmp"; then
                    echo "ERROR: optipng failed."
                    rm -f "png/$region.png.tmp"
                    continue
                else
                    mv "png/$region.png.tmp" "png/$region.png"
                fi
            fi
            echo ""
        ;;
        
        *)
            echo "Converting svg/$region.svg to png/$region.png" && rsvg-convert $1 -f png -o "png/$region.png" "svg/$region.svg"
        ;;
    esac
}

usersvgconvert() {
    
    WIDTH=$1;
    HEIGHT=$2;
    
    if [ $WIDTH -ne 0 ]; then
        IFS='    '
        cat SOURCES |
        while read region htmlurl ; do
            if [ -f "svg/$region.svg" ]; then
                rsvgconvert "-a -w ${WIDTH}"
            else
                echo "File svg/$region.svg doesn't exist!"
            fi
        done
    fi
    
    if [ $HEIGHT -ne 0 ]; then
        IFS='    '
        cat SOURCES |
        while read region htmlurl ; do
            if [ -f "svg/$region.svg" ]; then
                rsvgconvert "-a -h ${HEIGHT}"
            else
                echo "File svg/$region.svg doesn't exist!"
            fi
        done
    fi
    
    if  [ $WIDTH -eq 0 ] && [ $HEIGHT -eq 0 ]; then
        
        IFS='    '
        cat SOURCES |
        while read region htmlurl ; do
            if [ -f "svg/$region.svg" ]; then
                rsvgconvert "-a"
            else
                echo "File svg/$region.svg doesn't exist!"
            fi
        done
    fi
    
    updatealiases
}


case $OPTION in
    w | width)
        echo -n "Enter the prefered width: "
        read WIDTH
        usersvgconvert ${WIDTH} 0
    ;;
    
    h | height)
        echo -n "Enter the prefered height: "
        read HEIGHT
        usersvgconvert 0 ${HEIGHT}
    ;;
    
    n | normal | default)
        usersvgconvert 0 0
    ;;
    
    *)
        echo "Unknown option!"
    ;;
esac