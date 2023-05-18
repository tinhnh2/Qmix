iqtree-2.2.2.1 -seed 1 -st AA -T 36 -S out2  -te tree2.treefile --model-joint GTR20+FO --init-model Q.step3.4x.2  --prefix step5.2 --redo
grep -A 22 "can be used as input for IQ-TREE" step5.2.iqtree | tail -n21 > Q.step5.4x.2
