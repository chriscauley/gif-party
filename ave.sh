# Total numbers 
n=${#}

# copying the value of n 
m=$n 

# initialized sum by 0 
sum=0 

# array initialized with 
# some numbers 

# loop until n is greater 
# than 0 
while [ $n -gt 0 ] 
do
    # copy element in a 
    # temp variable 
    num=$1
    shift

    # add them to sum 
    sum=`expr $sum + $num` 

    # decrement count of n 
    n=`expr $n - 1` 
done 

avg=`expr $sum / $m`
printf '%0.0f' "$avg"
