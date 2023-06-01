for entry in `ls data`; do
	iqtree2 -seed 1 -T $1 -s data/$entry --prefix $entry -m "MIX{Q.step3.4x.1,Q.step3.4x.2,Q.step3.4x.3,Q.step3.4x.4}*R4" --no-seq-comp -wslmr
done
for entry in `ls data`; do
        iqtree2 -seed 1 -T $1 -s data/$entry --prefix $entry -m "MIX{Q.step3.4x.1,Q.step3.4x.2,Q.step3.4x.3,Q.step3.4x.4}*R4" --no-seq-comp -wslmr
done
touch step3.iqtree
