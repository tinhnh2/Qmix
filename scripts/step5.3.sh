iqtree2 -seed 1 -st AA -T $1 -S out3  -te tree3.treefile --model-joint $2+FO --init-model Q.step3.4x.3  --prefix step5.3
grep -A 22 "can be used as input for IQ-TREE" step5.3.iqtree | tail -n21 > Q.step5.4x.3
