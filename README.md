**1.**	**QMix program to estimate 4-matrix mixture models**

The single-matrix amino acid substitution models are widely used in phylogenetic analyses; however, they are uncapable to properly model the heterogeneity of amino acid substitution rates among sites. The multi-matrix mixture models LG4X and LG4M can handle the site rate heterogeneity, and outperform the single-matrix models. Estimating multi-matrix mixture models is a complex process, and no computer program is available for this task. In this study, we implemented a computer program of the so-called QMix based on the algorithm of LG4X and LG4M to automatically estimate multi-matrix mixture models from large datasets. QMix employs QMaker algorithm instead of XRATE algorithm to accurately and rapidly estimate parameters of models. It also supports multi-threading computing to efficiently estimate models from thousands of genes. We re-estimate 4-matrix mixture models LG4X and LG4M from 1471 HSSP alignments. The re-estimated models (HP4X and HP4M) are slightly better than LG4X and LG4M in building maximum likelihood trees from HSSP and TreeBASE datasets. The QMix program required about 10 hours on a computer with 18 cores to estimate a 4-matrix mixture model from 200 HSSP alignments. It is easy to use and freely available for researchers. 

**2.**	**Program installation**

In followings we will instruct you how to estimate 4-matrix mixture models from a set of alignments.

-	Download Qmix.py script; and the workflow folder that includes scripts for all steps of the Qmix algorithm. The scripts are written in Python so please install Python. 
-	The Qmix scripts are built from the IQ-TREE software (iqtree.org), therefore, you need the iqtree version 2.2.0 or later and set PATH to the iqtree program (i.e. export PATH=path_to_iqtree:$PATH)
-	Create a folder containing all alignments. For testing purpose, download “hssp200.zip” file from folder data; extract the file to get the folder hssp200 containing 200 HSSP alignments. 
-	Execute the Qmix program as followings:
cd 
 
 python Qmix.py -model rate_model -cor correlation_threshold -threads number_threads -initial start_matrix -data training_alignment_set

options:


•	model: Type of the mixture site rate model, i.e., 4M (the gamma distribution) or 4X (distribution-free scheme).

•	cor: The Pearson correlation threshold used to stop the model estimation process. The default value is 0.99

•	threads: The number of CPU cores for parallel running.

•	initial matrix: The starting matrix for the estimation process (LG/Q.pfam/JTT/WAG). If you want to start from other matrix, please save matrix into a file and put it into the scripts folder.

•	data: the full path to folder of alignments.

  For example: python Qmix.py -model 4M -cor 0.99 -threads 18 -initial LG -data /home/user/hssp200

The Qmix program will use 18 CPU cores to estimate a 4-matrix mixture time reversible model from alignments in the /home/user/Qmix/hssp200 folder following the free-distribution scheme for site rates. The Qmix program will output four matrices Q.1, Q.2, Q.3, and Q.4 (corresponding to the ‘very slow’, ‘slow’, ‘medium’, and ‘fast’ rate category, respectively) to the same running folder. 

**3.**	**Using mixture models**

You can use the mixture models with IQTREE to reconstruct phylogenetic trees from an input alignment. For example:

  iqtree2 -s input_aln -m "MIX{Q.1,Q.2,Q.3,Q.4}"

