Author: Tinh H. Nguyen

Email: nguyenhuytinh@gmail.com

Modeling amino acid substitution process is a complex and time-consuming task in phylogenetic analysis. Up to date, single-matrix models (i.e., models with single amino acid replacement matrices) are widely used to analyze protein sequences. A number of programs have been developed to estimate single replacement matrices from large datasets. The evolution at sites is heterogeneous and many factors such as solvent accessibility, protein structures and functions, affect amino acid substitution processes. Several studies have proposed methods to estimate multi-matrix mixture models (i.e., models with multiple replacement matrices) and showed their advantages over the single-matrix models. However, programs to automatically estimate mixture models from large dataset are unavailable.  In this paper, we present an efficient program, called QMix, to estimate mixture models with multi-matrix from large datasets. We applied the QMix program to estimate HSSP4M model using the discrete gamma rate distribution and HSSP4X model using the free schema distribution from the HSSP database. Experiments showed the advantages of HSSP4M and HSSP4X over current single-matrix and multi-matrix mixture models. QMix required about 80 (144) hours on a CPU of 36 2.3GHz-cores to estimate the HSSP4X (HSSP4M) model from 1471 HSSP alignments.

We first demonstrate the estimation of a mixture model for a dataset of 200 HSSP alignments. This sample data was extracted from full 1471 training alignments. Please download and extract the “hssp200.zip” file from folder “sample_data”, and put the extracted folder “data” into “sub_script” folder. 

To use Qmix please make sure that you download the IQ-TREE version 2.2.0 or later and set PATH to the execute downloaded file. For example:
**export PATH=path_to_IQTREE:$PATH**

The estimation (training) then can be accomplished with just one command. The command is:

**sh Qmix.sh 4x 0.95 18 /home/test/hssp200**

Options:
-	**4x**: specifies for free-schema distribution, the resulted matrix will be HSSP4X which is similar to LG4X. We can change to 4m for HSSP4M.
-	**0.95**: the correlation threshold condition for stopping estimation process (the training process consists of many loops, ~8 loops for HSSP4X to optimize upto 0.999), here we choose 0.95 for fast training in one loop.
-	**18**: the number of CPU cores will be assigned for parallel running process.
-	**/home/test/hssp200**: the path of input alignment data set folder for training process

The 4 resulting matrices **(Q.1, Q.2, Q.3, Q.4)** are placed in the same running folder.

We can use these matrices with IQTREE to reconstruct phylogenetic tree from an input alignment. For example:

**iqtree2 -s input_aln -m "MIX{Q.1,Q.2,Q.3,Q.4}\*R4"**

