# The Digital Story Grammar package (DSG)
A package for the statistical software program R to perform digital story grammar analyses on textual data

## Install
Install the program by downloading the DSG-package from this site and run the following command in R: <br/>

``` r
load(DSG)
```
## System pipeline
<img src="https://github.com/sban/narratives/blob/master/SystemPipeline.png" width="48">


##  Usage
The package requires `plyr`,`rJava`, `NLP`, `openNLP` and `stingr`

``` r
> txt <- c("The red fox jumped the fence", 
         "the brown cat likes milk", 
         "the red fox hates the cat")
> svo.res <- SVO(txt)
> svo.res
  SubSen   S      V     O                          txt
1      1 fox jumped fence The red fox jumped the fence
2      1 cat  likes  milk     the brown cat likes milk
3      1 fox  hates   cat    the red fox hates the cat
```

## License

This project is licensed under the GNU License - see the [LICENSE.md](LICENSE.md) file for details

