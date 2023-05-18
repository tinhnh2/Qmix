Author: Tinh H. Nguyen
Email: nguyenhuytinh@gmail.com
# mixture_model
Steps to estimate mixture models:
step 1: unzip training data file in folder data into the estimate_scripts folder
cp data/hssp200 estimate_scripts
cd estimate_scripts
unzip hssp200.zip
step2: run command to start estimate process:
# Set PATH to iqtree2 execute file.
export PATH=`pwd`:$PATH
# Run script to estimate free-schema (4x) or gamma distribution (4m), start from step 1 and stop with correlation threshold is 0.999, '&' for underground running.
python mix_process.py 4x 1 0.999 &

After this command, the process will run and finish after some loops. With hssp200, it took about 8 loops to obtain new model.

# Test
We also provide some script for RELL test, AU test in test_scripts
