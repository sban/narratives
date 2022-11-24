# The Digital Story Grammar package (DSG)

A simple program wrapper with a few modifications to perform digital story grammar (DSG) analyses on textual data in Python using AllenNLP. 

For empirical examples of DSG see 

Andrade SB & Andersen D (2020). Digital story grammar: a quantitative methodology for narrative analysis. International Journal of Social Research Methodology. Volume 23, Issue 4. https://doi.org/10.1080/13645579.2020.1723205

Andrade SB, Sools A & Saghai Y (2022). Writing styles and modes of engagement with the future. Futures
Volume 141. https://doi.org/10.1016/j.futures.2022.102986.


## Install
Install the program by downloading the DSG-program file from this site and run the following commands in python: <br/>

``` r

from allennlp.predictors.predictor import Predictor
import pandas as pd
import re
import DSG as dsg

```

##  Usage
The module also requires a SRL model. For example, this excellent public model by AllenNLP:

https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz

The program takes two options: the model (model) and where to place the output file (out_file) saved in CSV-format.

``` r
>>>text = ["The red fox jumped the old fence",
         "the brown cat likes milk",
         "the red fox hates the brown cat"]


>>>dsg.DSG(text, out_file = 'test.csv')
The red fox jumped the old fence. the brown cat likes milk. the red fox hates the brown cat
                S        V  ...  T                                                txt
0     The red fox   jumped  ...  -  [ARG0: The red fox] [V: jumped] [ARG1: the old...
1   the brown cat    likes  ...  -  The red fox jumped the old fence . [ARG0: the ...
2     the red fox    hates  ...  -  The red fox jumped the old fence . the brown c...

[3 rows x 7 columns]
>>> 



