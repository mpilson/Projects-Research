**Projects & Research Portfolio**
Hi, I’m Michael (Phin) Pilson, and welcome to my Projects & Research Portfolio! This repository reflects my passion for data science, math, and computer science.
Through these projects, I’ve explored everything from coding machine learning algorithms from scratch to graduate-level graph theory research.
Below, you'll find descriptions of each folder and its contents. Enjoy! (I will try to keep this up to date as best I can, Last Updated: 9/10/2024) 

[**112**](https://github.com/mpilson/Projects-Research/tree/main/112)
This folder captures the work I did in my intro cs class (15-112)

Mini Metro Simulation
This project simulates a transportation network, inspired by the game Mini Metro
- OOP: Object-Oriented Programming for managing vehicles, passengers, and routes.
- Data Structures: Efficient data structures to handle dynamic edge lists for real-time route planning.
- Pathfinding: Focus on pathfinding and network optimization algorithms.

Tetris Clone
A custom implementation of the classic Tetris game
- OOP: Object-Oriented Programming for managing game elements like pieces and the grid.
- 2d grid data structure: Use of 2D grid-based algorithms for piece movement, collision detection, and line clearing.
- Graphics: A simple graphical interface for rendering the game board and interactions.

[**202**](https://github.com/mpilson/Projects-Research/tree/main/202)
These two end-to-end data analysis projects use real-world datasets (Titanic and bike-sharing data), (From stats class 36-202)

Titanic EDA
- Dataset: Titanic survival data
- Techniques: Data wrangling (dplyr, readr), univariate and bivariate analysis and visualization (ggplot2, bar charts, scatter/box plots),
classification models (LDA, QDA, logistic regression, decision trees, …), performance analysis (error metrics, misclassification)
- Insights: Passenger class and gender strongly influenced survival rates.
  
Bike Sharing EDA
- Dataset: Washington D.C. bike-sharing data
- Techniques: Linear regression, data transformations (log, power), univariate and bivariate analysis and visualization (ggplot2, histograms, bar plots),
- performance analysis (multicollinearity with VIF, residual using QQ plots)
- Insights: Temperature positively correlated with bike usage, while weather played a significant role in user behavior.

[**ML**](https://github.com/mpilson/Projects-Research/tree/main/ML)
This folder contains what I am currently working on and current skills I am trying to develop.
Across all models, I used pandas for data processing/importing and sklearn train_test_split for data split

GLM
Implemented regression model from scratch that is easily adapted to GLM models (linear, logistic, poisson, …)
- Libraries: Numpy for efficiency and linear algebra, sklearn for testing and comparison, matplotlib for visualization
- OOP: to provide seamless storage and access to model attributes and specific methods
- Optimization: implemented gradient descent from scratch for parameter optimization, adaptable to batch size (stochastic, batch, mini-batch)
- visualizations: scatter plot of total cost as a function of epochs, shows convergence and optimization of loss function
- performance analysis: used error metrics (r squared, MSE, MAE)
- sklearn comparison: used sklearn to construct rival model to evaluate performance and build familiarity

DT
Implemented numerical based decision tree
- Libraries: Numpy for efficiency and linear algebra, sklearn for testing and comparison, matplotlib for visualization
- OOP: Used oop extensively for tree and node structure, functionality, and data storage
- Growing: evaluated gini-loss for potentially threshold splits, using midpoints of input data
- Pruning: Used misclassification error to evaluate fully grown tree and prune back inefficient sub-branches
- testing and visualizations: used matplotlib and sklearn build in DT, to evaluate my own and compare methodology

GDA/GNB 
Implemented numerical based gaussian discriminant analysis and naive bayes
- pandas: used pandas to partition data for class priors, means, variance/covariance
- Numpy:  used Numpy for efficiency, seamless linear algebra and vectorization, and broadcasting for dimensional flexibility
- Sklearn:  for metrics and performance analysis

CV
Used cross validation and error analysis to compare performance
- Sklearn: used pipeline, gridsearch, cross validation, and built in performance metrics to streamline training, testing, and model evaluation
- Sklearn pipeline: scale data, streamline training
- Sklearn gridsearch: iterate through possible hyperparameter values, find best combination

[**SUAMI**](https://github.com/mpilson/Projects-Research/tree/main/SUAMI)
This folder encapsulates some of the work I did over the summer through CMU's math research program Summer Undergraduate Applied Mathematics Institute (SUAMI)
My group was mainly from Clark Atlanta University (CAU) and we were mentored by Professor Shanise Walker [LinkedIn](https://www.linkedin.com/in/shanise-walker-600036b1/)
We studied induced saturation on Boolean Lattices, attempting to find tighter bounds for specific sub-posets and lattices
Included are the papers we built off of/studied, latex files of our results, and a photo of the team!

[**SURA**](https://github.com/mpilson/Projects-Research/tree/main/SURA)
This folder encapsulates some of the work I did over the summer through CMU's Summer Undergraduate Research Apprenticeship (SURA) program
I worked under Professor Juergen Kritschgau [Website](https://www.jkritschgau.com/home) studying Zero-Forcing on k-ary trees
Included are the papers I built off of/studied and latex files of our preliminary results

[**SW**](https://github.com/mpilson/Projects-Research/tree/main/SW)
More of a side project, but implementing based algorithms and data structures
Plan to adopt into Java/C, to build language fluency and practice pointers/memory allocation

[**Test**](https://github.com/mpilson/Projects-Research/tree/main/Test)
These are just files for me to mess with syntax, explore software interactions, and debug
