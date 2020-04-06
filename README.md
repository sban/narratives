# The Digital Story Grammar package (DSG)
A package for the statistical software program R to perform digital story grammar analyses on textual data

## Install
Install the program by downloading the DSG-package from this site and run the following command in R: <br/>

``` r
load(DSG)
```

##  Usage
The package requires `plyr`,`rJava`, `NLP`, `openNLP` and `stingr`

System pipeline
<img src="https://github.com/sban/narratives/blob/master/SystemPipelineW2.png" >



``` r
> txt <- c("The red fox jumped the old fence", 
         "the brown cat likes milk", 
         "the red fox hates the brown cat")
> dsg.res <- DSG(txt)
> dsg.res
  SubSen   S      V     O     S.mod    O.mod    txt
1      1 fox jumped fence     red      old     The red fox jumped the old fence
2      1 cat  likes  milk     brown    -        the brown cat likes milk
3      1 fox  hates   cat     red      brown    the red fox hates the brown cat
```

The result can easily be plotted as a network graph.

<img src="https://github.com/sban/narratives/blob/master/network.png" >



