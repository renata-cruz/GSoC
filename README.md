# Google Summer of Code 2022 - Final Report
## INCF GSoC 2022 1.1. Implementation of White Matter Substrates in Disimpy

## Summary 

During the GSoC 2022 program, I implemented an algorithm to simulate white matter substrates in Disimpy, an open-source Python package for generating diffusion MRI data. Due to time restrictions, I could not achive all the goals described in my initial [project proposal](https://github.com/renata-cruz/GSoC/blob/d8b7bb829b809203a9f2ca79f44553e454592ec9/GSoC_ProjectProposal.pdf) yet I will continue to work on this project even as GSoC comes to an end. In addition to the documented code found in this [Pull Request](https://github.com/kerkelae/disimpy/pull/16#issue-1321589071), the following [Jupyter Notebook](https://github.com/renata-cruz/GSoC/blob/d7aee6517fa2d73611bd3be5bef52a87ddba187b/GSoC2022_Disimpy_WM_Substrates.ipynb) contains the script and further results on which I worked during the coding period. Finally, altough the project will continue to be developed, the code written specifially for this program will be archived [here](https://github.com/renata-cruz/disimpy.git) and will not suffer any further modifications.


## What Was Done

1. Implementation of an algorithm to create packed cylindrical substrates;


## To Be Continued...

1. Review my pull request and do the required changes to make sure the code gets merged;
2. Write a tutorial for the algorithm;
3. Implement additional features.


## Important Links

- [Project Proposal](https://github.com/renata-cruz/GSoC/blob/d8b7bb829b809203a9f2ca79f44553e454592ec9/GSoC_ProjectProposal.pdf)
- [Jupyter Notebook](https://github.com/renata-cruz/GSoC/blob/d8b7bb829b809203a9f2ca79f44553e454592ec9/GSoC2022_Disimpy_WM_Substrates.ipynb)
- [Pull Request](https://github.com/kerkelae/disimpy/pull/16#issue-1321589071)


## In Detail

The opportunity to participate in GSoC came to be as a former contributer and now my current mentor, presented an idea for a project and introduced the program as a great way to learn more about open source coding. Since the beginning, we maintained an open line of communication and had weekly meetings to always be up to date on the progress of the project. 

During the period prior to the coding phase, I started with learning more about Disimpy by studying the source code and completing the tutorial. Disimpy is an open-source Python package for generating dMRI data through Monte Carlo random walk simulations. I contributed to the package by opening a [pull request](https://github.com/kerkelae/disimpy/pull/13#issue-1166368430) and wrote a function to generate a gradient array for the Pulsed Gradient Spin Echo (PGSE) sequence. I also wrote the appropriate documentation and unit tests and the code was merged after review.

As for the project, I began with a 2D implementation of the algorithm in which I sampled circles with gamma distributed radii and packed them in a square with periodic boundaries. In the following steps, I designed a triangular mesh with cylindric shape and packed the meshes in a cube to simulate white matter in a voxel. I also generalised the sampling step to generate radii from other distributions. Due to time restrictions, I was not able to add other features to the substrates as initially intended. Also, in the current state, there are still some issues with the code that need to be fixed before merging is possible. 

The main challenge I faced during the development of this project was the implementation of periodic boundaries in the cylindrical meshes, which remains to be resolved. We will continue to work on this algorithm so it can be merged and hopefully useful to other users.

Overall, being part of this program has allowed me to learn a lot about open source coding and was a starting point for me to develop a new set of skills which I will continue to expand in the future.

























