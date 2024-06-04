# StageM2


## Descriptions 
This package is used to detect and quantify spots in live cells. 
It use BigFish and BigFish live to quantify single molecules and clusters in live movies. 


## Table of Contents 
1. [Installation](#installation)
2. [Usage](#usage)
3. [Contributing](#contributing)
4. [License](#license)

## Installation 

To download this package use the following command : 
git clone https://github.com/raphaeluniversitebdx/StageM2.git

You need to create 2 distincts Anaconda environments : 
- segmentation
- detection 

each environment has it own yml file. 

## Usage

### Description of the pipeline 
The pipeline consist of the following steps :
- segmentation of cells
- tracking of the cells
- cropping and centering

- get threshold
- Build Reference spot
- Quantification of the clusters 

