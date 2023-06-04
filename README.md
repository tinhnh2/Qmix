**1.**	**QMix program to estimate 4-matrix mixture models**

Modeling amino acid substitutions during the evolution process is a complex and time-consuming task. The amino acid substitutions at sites are heterogeneous and affected by different factors such as solvent accessibility, protein structures and functions. Several studies have proposed methods to estimate multi-matrix mixture models and showed their advantages over the single-matrix models. However, no program is available to automatically estimate mixture models.  Here, we present a maximum likelihood estimation program, called QMix, to efficiently estimate mixture models with four replacement matrices from large datasets. The four replacement matrices either follow the discrete gamma distribution (4M) or a distribution-free scheme (4X) for site rates. 

We applied the QMix program to estimate two mixture models from 1471 HSSP alignments: HSSP4M consisting of 4 replacement matrices corresponding to 4 categories of the discrete gamma distribution and HSSP4X model with 4 replacement matrices following a distribution-free scheme for site rates. Experiments showed the advantages of HSSP4M and HSSP4X over the single-matrix and multi-matrix mixture models. QMix required about 144 (160) hours on a CPU of 36 2.3GHz-cores to estimate the HSSP4X (HSSP4M) model from 1471 HSSP alignments

**2.**	**Program installation**

In followings we will instruct you how to estimate 4-matrix mixture models from a set of alignments.

-	Download Qmix.sh script; and the scripts folder that includes scripts for all steps of the Qmix algorithm. The scripts are written in Python so please install Python. 
-	The Qmix scripts are built from the IQ-TREE software (iqtree.org), therefore, you need the iqtree version 2.2.0 or later and set PATH to the iqtree program (i.e. export PATH=path_to_iqtree:$PATH)
-	Create a folder containing all alignments. For testing purpose, download “hssp200.zip” file from folder data; extract the file to get the folder hssp200 containing 200 HSSP alignments. 
-	Execute the Qmix program as followings:

  sh Qmix.sh type corr cores start_matrix alignments

options:

•	type: Type of the mixture model, i.e., 4m (the gamma distribution) or 4x (distribution-free scheme).

•	corr: The Pearson correlation threshold used to stop the model estimation process. The default value is 0.99

•	cores: The number of CPU cores for parallel running.

•	start_matrix: The starting matrix for the estimation process (LG/Q.pfam/JTT/WAG). If you want to start from other matrix, please save matrix into a file and put it into the scripts folder.

•	alignments: the full path to folder of alignments.

  For example: sh Qmix.sh 4x 0.95 18 LG /home/user/Qmix/hssp200

The Qmix program will use 18 CPU cores to estimate a 4-matrix mixture model from alignments in the /home/user/Qmix/hssp200 folder following the free-distribution scheme for site rates. The Qmix program will output four matrices Q.1, Q.2, Q.3, and Q.4 (corresponding to the ‘very slow’, ‘slow’, ‘medium’, and ‘fast’ rate category, respectively) to the same running folder. 

**3.**	**Using mixture models**

You can use the mixture models with IQTREE to reconstruct phylogenetic trees from an input alignment. For example:

  iqtree2 -s input_aln -m "MIX{Q.1,Q.2,Q.3,Q.4}*R4"

