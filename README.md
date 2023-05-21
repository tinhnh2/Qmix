Author: Tinh H. Nguyen\
Email: nguyenhuytinh@gmail.com
# Unzip training data
cp data/hssp200 estimate_scripts\
cd estimate_scripts\
unzip hssp200.zip

# Set PATH to iqtree2 execute file.
export PATH=PATH_TO_IQTREE2:$PATH

We uploaded iqtree-2.2.2.1 in estimate_scripts folder. So, you can set PATH with command:

export PATH=\`pwd\`:$PATH

# Run script to estimate 

Run with command: 

python mix_process.py model_type loop_id stop_threshold

Options:

model_type: 4m for gamma rate distribution, 4x for free-schema distribution

loop_id: default is 1

stop_threshold: condition for stopping estimation process, here we choose correlation score is the criteria with 0.999

Example command: 

python mix_process.py 4x 1 0.999

After this command, the process will run and finish after some loops. With hssp200, it took about 8 loops to obtain new model.

# Run from certain loop. For example, we continue from loop 3

touch un.do

python mix_process.py 4x 3 0.999
# Test
For test script, please see in test_scripts folder.
