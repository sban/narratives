# The Digital Story Grammar package (DSG)

A simple wrapper program to perform digital story grammar (DSG) analyses on textual data in Python using the AllenNLP framework. 

For empirical examples that also present the theory behind DSG, please see:

Andrade SB & Andersen D (2020). Digital story grammar: a quantitative methodology for narrative analysis. International Journal of Social Research Methodology. Volume 23, Issue 4. https://doi.org/10.1080/13645579.2020.1723205

Andrade SB, Sools A & Saghai Y (2022). Writing styles and modes of engagement with the future. Futures
Volume 141. https://doi.org/10.1016/j.futures.2022.102986.


## Install
Install the program by downloading the DSG-program file from this site (DSG.py), save the file to your working directory for your analysis, and run the following commands in python: <br/>

```python

from allennlp.predictors.predictor import Predictor
import pandas as pd
import re
import DSG as dsg

```

##  Usage
The module also requires a SRL model. For example, this excellent public model by AllenNLP:

https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz

The program takes two options: the model (model) and where to place the output file (out_file) saved in CSV-format.

```python
>>>text = ["Yesterday, the red fox jumped the old fence.",
         "The red fox hits the dog with her paw.",
         "In the UK, the red foxes hate brown dogs."]

>>>model_SRl = 'https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz'
>>>result = dsg.DSG(text, model = model_SRL, out_file = 'test.csv')
```

The result is stored as a DataFrame and includes variabel information about the subject (S), the verb (V), the object (O), the means for the action (M), the place (P), time (T) and the tagged sentence (txt):

```python
>>>result
               S         V               O                M             P               T               txt
0     the red fox   jumped   the old fence                -             -        Yesterday         [ARG0: The red fox] [V: jumped] [ARG1: the old...  
1     The red fox     hits         the dog     with her paw             -               -          The red fox jumped the old fence . [ARG0: the
2   the red foxes    hates   the brown cat                -      In the UK              -          The red fox jumped the old fence . the brown c...  

[3 rows x 7 columns]
>>> 
```



