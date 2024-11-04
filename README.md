# Wrapper for The Digital Story Grammar (DSG) in Python

A simple wrapper for performing digital story grammar (DSG) analyses on textual data in Python using the AllenNLP framework. Please note that the original program was written in R, and the Python wrapper is still in beta. For empirical examples of DSG (based on the R program) that also explain the theory behind DSG, please see:

Andrade SB & Andersen D (2020). Digital story grammar: a quantitative methodology for narrative analysis. International Journal of Social Research Methodology. Volume 23, Issue 4. https://doi.org/10.1080/13645579.2020.1723205

Andrade SB, Sools A & Saghai Y (2022). Writing styles and modes of engagement with the future. Futures
Volume 141. https://doi.org/10.1016/j.futures.2022.102986.


## Install
Install the program by downloading the DSG-program file from this site (DSG.py), save the file to your working directory for your analysis, and run the following commands in python: <br/>

```python

from allennlp.predictors.predictor import Predictor
import pandas as pd
import re
import spacy
import DSG as dsg

```

##  Usage 
The module also requires a SRL model. For example, this excellent public model by AllenNLP:

https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz

The program takes two options: the model (model) and where to place the output file (out_file) saved in CSV-format.

```python
>>> text = ["Yesterday, the red fox jumped the old fence.",
         "The red fox hits the dog with her paw.",
         "In the UK, the red foxes hate brown dogs."]

>>> model_SRl = 'https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz'
>>> result = dsg.DSG(text, model = model_SRL, out_file = 'test.csv')
```

The result is stored as a DataFrame and includes variabel information about the subject (S), the verb (V), the object (O), the means for the action (M), the place (P), time (T) and the tagged sentence (txt):

```python
>>> result
               S         V               O                M             P               T               txt
0     the red fox   jumped   the old fence                -             -        Yesterday         [ARG0: The red fox] [V: jumped] [ARG1: the old...  
1     The red fox     hits         the dog     with her paw             -               -          The red fox jumped the old fence . [ARG0: the
2   the red foxes     hate      brown dogs                -      In the UK              -          The red fox jumped the old fence . the brown c...  

[3 rows x 7 columns]
>>> 
```

Before using the DSG algorithm, it may sometimes be necessary to link all words that refer to the same real-world entity (also known as coreference resolution). The module therefore includes the following function (taken from https://demo.allennlp.org/coreference-resolution):

```python 

>>> text = 'One afternoon, a fox which was out for a walk in the jungle came across a bunch of grapes hanging. Its mouth watered at the very sight of the grapes. The fox thought to himself that if it could get the bunch of grapes, it would be just the thing to quench its thirst in the sweltering heat of the afternoon.'
>>> model_CRF = 'https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2020.02.27.tar.gz'
>>> coref_text = dsg.coref(text, model = model_CRF)
>>> print(coref_text)
One afternoon, a fox which was out for a walk in the jungle came across a bunch of grapes hanging. a fox which was out for a walk in the jungle's mouth watered at the very sight of a bunch of grapes hanging. a fox which was out for a walk in the jungle thought to a fox which was out for a walk in the jungle that if a fox which was out for a walk in the jungle could get a bunch of grapes hanging, a bunch of grapes hanging would be just the thing to quench a fox which was out for a walk in the jungle's thirst in the sweltering heat of the afternoon.
>>> 

```

