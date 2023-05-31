iqtree2 -seed 1 -st AA -T 36 -S out4  -te tree4.treefile --model-joint GTR20+FO --init-model Q.step3.4x.4  --prefix step5.4 --redo
grep -A 22 "can be used as input for IQ-TREE" step5.4.iqtree | tail -n21 > Q.step5.4x.4
