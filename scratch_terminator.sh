while :
do
    read key
    if [[ $key = q]]
    then
        break
    fi
done

pkill -fe scratch
