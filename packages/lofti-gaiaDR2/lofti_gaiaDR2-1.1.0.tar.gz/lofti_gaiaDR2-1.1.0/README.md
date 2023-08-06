# lofti_gaiaDR2
### Python package for orbit fitting with Gaia astrometry
Written by Logan A. Pearce, 2019<br>
If you use LOFTI in your work please cite Pearce et al. 2020

## Complete documentation at [http://lofti-gaiadr2.rtfd.io](http://lofti-gaiadr2.rtfd.io)


### To install lofti_gaiaDR2:
    pip install lofti_gaiaDR2
   
### Required packages:
numpy, matplotlib, astropy, astroquery, pickle

Written for python 3.7 (I haven't tried it on python 2... may work?)

### Description:
lofti_gaia is a basic orbit fitter designed to fit orbital parameters for one wide stellar binary relative to the other, when both objects are resolved in Gaia DR2.  It takes as input only the Gaia DR2 source id of the two components, and their masses.  It retrieves the relevant parameters from the Gaia archive, computes observational constraints for them, and fits orbital parameters to those measurements using a method based on Orbits for the Impatient (OFTI; Blunt et al. 2017).  It assumes the two components are bound in an elliptical orbit.  

Also included are some suggested basic statistics and plotting tools to examining the output from the fitter.

Caution:
 - It will give you answers, even if the two source ids you give it aren't actually bound.
 - It will give you answers even if the two Gaia astrometric solutions are not of good quality.
 
 Use with appropriate care and consideration of the reasonableness of your results!  If you give it garbage, it will give you garbage in return!
 
 For a detailed analysis of when using Gaia to constrain stellar binary orbits is and is not appropriate, see Pearce et al. (2019) (currently in prep, email corresponding author for a copy)

Please see the tutorial on the RTD page for how to use the package.

[![Documentation Status](https://readthedocs.org/projects/lofti-gaiadr2/badge/?version=latest)](https://lofti-gaiadr2.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/lofti-gaiaDR2.svg)](https://badge.fury.io/py/lofti-gaiaDR2)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3955152.svg)](https://doi.org/10.5281/zenodo.3955152)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

Copyright Logan Pearce, 2019

loganpearce1@email.arizona.edu
