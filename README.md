**1.**	**QMix program to estimate 4-matrix mixture models**

The single-matrix amino acid substitution models are widely used in phylogenetic analyses; however, they are uncapable to properly model the heterogeneity of amino acid substitution rates among sites. The multi-matrix mixture models LG4X and LG4M can handle the site rate heterogeneity, and outperform the single-matrix models. Estimating multi-matrix mixture models is a complex process, and no computer program is available for this task. In this study, we implemented a computer program of the so-called QMix based on the algorithm of LG4X and LG4M to automatically estimate multi-matrix mixture models from large datasets. QMix employs QMaker algorithm instead of XRATE algorithm to accurately and rapidly estimate parameters of models. It also supports multi-threading computing to efficiently estimate models from thousands of genes. We re-estimate 4-matrix mixture models LG4X and LG4M from 1471 HSSP alignments. The re-estimated models (HP4X and HP4M) are slightly better than LG4X and LG4M in building maximum likelihood trees from HSSP and TreeBASE datasets. The QMix program required about 10 hours on a computer with 18 cores to estimate a 4-matrix mixture model from 200 HSSP alignments. It is easy to use and freely available for researchers.

**2.**	**Installation and Execution**

Installation:

-	Download the Python Qmix.py program and the folder 'initial_models' containing some initial models for the QMix estimation process.
-	The QMix uses the IQ-TREE software (iqtree.org). Download the IQ-TREE version 2.2.0 or later and set PATH to the iqtree program (i.e. export PATH=path_to_iqtree:$PATH)
-	Create a folder containing all alignments. The "hssp200.zip" with 200 HSSP alignments and “hssp1471.zip” with 1471 HSSP alignments are available in the folder data.

Execution:  Estimating a 4-matrix mixture model from a set of alignments can be accomplished by QMix with one command:

 python Qmix.py -model rate_model -cor correlation_threshold -threads number_threads -initial start_model -data training_alignment_set

Options:

•	model: Type of the mixture site rate model, i.e., 4M (the gamma distribution) or 4X (the distribution-free scheme).

•	cor: The Pearson correlation threshold used to stop the model estimation process. The default value is 0.99

•	threads: The number of threads for parallel running.

•	initial: The starting model for the estimation process (LG/Q.pfam/JTT/WAG). If you want to start from another model, copy the file containing the model to the initial models folder.

•	data: the full path to the folder of alignments.

  For example: 
  
  python Qmix.py -model 4X -cor 0.99 -threads 18 -initial LG -data /home/user/hssp200

The Qmix program will output four matrices Q.1, Q.2, Q.3, and Q.4 (corresponding to the ‘very slow’, ‘slow’, ‘medium’, and ‘fast’ rate category, respectively) to the same running folder.

**3.**	**Using mixture models**

You can use the mixture models with IQ-TREE to reconstruct phylogenetic trees.

  iqtree2 -s alignment -m "MIX{Q.1,Q.2,Q.3,Q.4}"
