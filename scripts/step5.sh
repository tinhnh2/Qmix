export CURR_DIR=`pwd`
cd ${CURR_DIR}/loop$1/step5/
rm step5*
cat ../step4/trees/out1/* > tree1.treefile
cat ../step4/trees/out2/* > tree2.treefile
cat ../step4/trees/out3/* > tree3.treefile
cat ../step4/trees/out4/* > tree4.treefile
mkdir out1
mkdir out2
mkdir out3
mkdir out4
cp ../step4/step3_out1/* out1/
cp ../step4/step3_out2/* out2/
cp ../step4/step3_out3/* out3/
cp ../step4/step3_out4/* out4/
cp ../step3/Q.step3.4x* .
cd ${CURR_DIR}
cp step5.1.* loop$1/step5/
cp step5.2.* loop$1/step5/
cp step5.3.* loop$1/step5/
cp step5.4.* loop$1/step5/
cp normalized.sh loop$1/step5/
cp NormalizeMatrix.pl loop$1/step5/
cd ${CURR_DIR}/loop$1/step5
sh step5.1.sh $2
sh step5.2.sh $2
sh step5.3.sh $2
sh step5.4.sh $2
