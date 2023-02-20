# NetworkScience

Instruction for executing code -

1. Deploying clustering algorithms via SSH


2. Analysis

After executing the algorithms on the server, save all output files in one output folder according to the following naming convensions:
- Wikipedia files begin with "wiki-Vote"
- P2P Filesharing files begin with "p2p-Gnutella08"
- Facebook files begin with "facebook_combined"
- Collaboration files begin with "ca-GrQc"
- Youtube files begin with "com-youtube.ungraph_communities.txt"

Additionally, output files should end with the following suffix:
- ".metis.part.100" if from the METIS algorithm
- ".metis.c1000.i2.0.b0.5" if from the MCL algorithm
- "_community.txt" if from the Clauset-Newman-Moore algorithm

After setting up these dependencies, the file titled "networkScienceLab2.ipynb" should be executable given the additional helper.py file is in the same director. An exported jupyter notebook will contain all of these results.