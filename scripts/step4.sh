CURR_DIR=`pwd`
cp step4.py ${CURR_DIR}/loop$1/step4/
cd ${CURR_DIR}/loop$1/step4
mkdir step3_out1
mkdir step3_out2
mkdir step3_out3
mkdir step3_out4
mkdir -p trees/out1
mkdir -p trees/out2
mkdir -p trees/out3
mkdir -p trees/out4
#cp -rf ../step3/group$2/out$2 .
cp -rf ../step3/* .
python step4.py data
