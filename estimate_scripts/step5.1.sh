iqtree-2.2.2.5 -seed 1 -st AA -T 36 -S out1  -te tree1.treefile --model-joint GTR20+FO --init-model Q.step3.4x.1  --prefix step5.1 --redo
grep -A 22 "can be used as input for IQ-TREE" step5.1.iqtree | tail -n21 > Q.step5.4x.1
