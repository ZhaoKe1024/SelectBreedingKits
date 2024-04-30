A library of simulation calculation tools for quantitative genetics developed for poultry breeding.

### Key Issue
The core of the entire algorithm consists of two parts, how to calculate the kinship correlation coefficient, and how to assign female individuals to male poultry. 
In fact, our algorithm should be expressed in another way, how to select male individuals for female poultry. 
Because there is a one-to-many relationship between males and females, it is actually critical which one is dominant in the algorithm.


### File Structure
```text
root(Sound-Representation-KZ)
└─Breeding_Main.py  // Main Program, Genetic Algorithm
└─entities.py  // Poultry object and functions
└─breedingkits.py  // functions for breeding
└─xlsxreader.py  // used to read data from xlsx(Excel) files
└─func.py  // generate common value
└─kinship_calc.py  // test the calculation of kinship and inbreed
```


