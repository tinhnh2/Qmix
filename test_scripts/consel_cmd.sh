export PATH_TO_BIN=~/bin
cd $1
for f in *.sitelh 
do
	echo "Process file $f"
	mv $f ${f%%.*}.sitelh
	${PATH_TO_BIN}/seqmt --puzzle ${f%%.*}.sitelh
	${PATH_TO_BIN}/makermt ${f%%.*}
	${PATH_TO_BIN}/consel ${f%%.*}.rmt
	${PATH_TO_BIN}/catpv ${f%%.*}.pv > ${f%%.*}_250.pv
done
