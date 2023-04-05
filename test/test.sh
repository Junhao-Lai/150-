
#echo "Enter your name: "
#read name

#echo "Hello, $name!"
for file in *
do
	lineNumber=1
	while read line
	do
		if [ $((lineNumber%2)) == 0 ]
		then 
			echo "$file: $line"
		fi
		((lineNumber++))
	done < "$file"
done
