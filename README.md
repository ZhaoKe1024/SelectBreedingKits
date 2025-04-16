A library of simulation calculation tools for quantitative genetics developed for poultry breeding.

# 家禽配种优化程序

给定多代家禽的信息，例如2017、2018、...、2020年的家禽配种和出雏方案，构建出一个族谱图，创建对应的图数据结构。然后采用遗传算法，给出2021年的家禽配种方案，目标为配种平均亲缘相关系数最小化。

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


