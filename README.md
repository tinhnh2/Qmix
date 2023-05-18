Author: Tinh H. Nguyen\
Email: nguyenhuytinh@gmail.com
# Unzip training data
cp data/hssp200 estimate_scripts\
cd estimate_scripts\
unzip hssp200.zip

# Set PATH to iqtree2 execute file.
export PATH=PATH_TO_IQTREE2:$PATH
# Run script to estimate 
Option: free-schema (4x) or gamma distribution (4m), start from step 1 and stop with correlation threshold is 0.999.\
Run with command: 

python mix_process.py 4x 1 0.999

After this command, the process will run and finish after some loops. With hssp200, it took about 8 loops to obtain new model.

# Run from certain loop. For example, we continue from loop 3

touch un.do

python mix_process.py 4x 3 0.999
# Test
We also provide some script for RELL test, AU test in test_scripts
