<p align="left">
  <a href="https://github.com/eac-ufsm/augen/" target="_blank">
    <img alt="Version" src="https://img.shields.io/badge/Version-0.1.1-brightgreen">
  </a>

  <a href="https://www.python.org/downloads/release/python-3810/" target="_blank">
    <img alt="Python version" src="https://img.shields.io/badge/Python-3.8.10-blue">
  </a>

  <a href="https://github.com/eac-ufsm/augen/commits/master" target="_blank">
    <img src="https://img.shields.io/github/last-commit/eac-ufsm/augen" alt="GitHub last commit">
  </a>

  <a href="https://github.com/psf/black" target="_blank">
    <img alt="code style" src="https://img.shields.io/badge/code style-black-black">
  </a>
</p>

*This is the English version of this documentation file. For the Brazilian Portuguese version of this text [click here](README_PT-BR.md).*

# Augen (version: 0.1.1)

Augen is a toolbox designed to create a direct integration between [Acoular](https://github.com/acoular/acoular) [[1]](#1) and [Amiet Tools](https://github.com/fchirono/amiet_tools) [[2]](#2). It also provides a few functions written in Matlab to provide support for using toolboxes like [ITA-Toolbox](https://git.rwth-aachen.de/ita/toolbox) [[3]](#3) and [Beamap](https://github.com/eac-ufsm/beamap) [[4]](#4).

The name **Augen** is an acronym for **A**miet-Aco**u**lar Inte**g**ration Modul**e** in Pytho**n**.

**The article that presents this toolbox is available on [Research Gate](https://www.researchgate.net/publication/363031873_Integracao_de_multiplas_toolboxes_para_aplicacao_em_beamforming_e_aeroacustica):**

- *Integration of multiple toolboxes for application in beamforming and aeroacoustics.*

## Installation

**Note:** If you are a GitHub Desktop user, you still will need to follow the steps below.

### Procedure

1.0 There are two methods to use the toolbox, **1.1** which uses directly the Python installation or **1.2** with an Anaconda environment.

1.1 Install Python 3.8.10 and [git](https://git-scm.com/) to be able to proceed with the installation.

1.2 Create an Anaconda environment for Python 3.8.10 with ```conda create -n env_name python=3.8.10```.

2.0 Install all the dependencies from list below (read [[A]](#A)):
- **[Python](https://www.python.org/downloads/release/python-3810/) == 3.8.10**
- [SciPy](https://scipy.org/) == 1.7.1
- [NumPy](https://numpy.org/) == 1.20.3
- [Amiet Tools](https://github.com/fchirono/amiet_tools) == 0.0.2
- [Acoular](https://github.com/acoular/acoular) == 21.5
  - [scikit-learn](https://scikit-learn.org/stable/) (a.k.a. sklearn)== 0.24.2
  - [Numba](https://numba.pydata.org/) == 0.54.0
  - [six](https://github.com/benjaminp/six) >= 1.1.0
  - [pytables](https://github.com/PyTables/PyTables) (a.k.a. tables) == 3.6.1
  - [Traits](https://docs.enthought.com/traits/index.html) == 6.2.0
  - [TraitsUI](https://docs.enthought.com/traitsui/) == 7.2.1
  - libpython
- Matplotlib == 3.7.4
- PyQt5 == 5.15.10
- h5py == 3.10.0

**Warning**: Since **Amiet Tools** isn't yet available in [PyPI](https://pypi.org/), make sure to run the following command before installing **Augen**:

```pip install git+https://github.com/fchirono/amiet_tools```

2.1 Check with the command ```pip list``` if all the dependecides are installed with the correct version. Don't forget to read [[A]](#A).

3.0. After installing all the dependencies required, the next step is the installation of Augen by simply running the following command via PIP:

```pip install git+https://github.com/eac-ufsm/fia2022-augen```


### <a id="A">[A]</a> How to install an old version of a dependency 

To install in Python a module/package via PIP the following command is used:
```pip install example_module```.

In cases where a specific version of a module is required, the following command is applied:

```pip install example_module==x.x.x```,

in which **x.x.x** should be the desired version, an example is that instead of **x.x.x** it would be **1.7.1**.

## Tutorial

The [examples](examples) folder has scripts that are focused on exemplifying the usage of the toolbox, with scripts well commented on.

### The results from the spiral microphone array example

![Results for the spiral mic. array](examples/fia22/images/Spiral_MicArray.png)

## Important notes

- The folder [simple_tests](simple_tests) contains a small number of scripts focused on testing the different classes and scripts provided by the tool. This folder isn't a folder of *pythonic* testing.

- The folder [Matlab](matlab) makes available a few functions written in Matlab to be used together with toolboxes like ITA-Toolbox and Beamap — geared towards saving/reading in XML file format, the microphone array geometry.

## About the authors

**[Michael Markus Ackermann](https://www.researchgate.net/profile/Michael-Ackermann-3)** is an Acoustical Engineering undergraduate student at the Federal University of Santa Maria (UFSM) in south Brazil. Augen is created by Michael as part of his Bachelor's Thesis — which focused on Aeroacoustics and Acoustical Beamforming (moreover, it expands a Python branch from Beamap).

**[William D'Andrea Fonseca](https://www.researchgate.net/profile/William-Fonseca-4)** is a Professor of the Acoustical Engineering undergraduate course in South Brazil (advising master and undergrad projects) at the Federal University of Santa Maria (UFSM). William does research in Acoustic Engineering, Electrical Engineering, and Aerospace Engineering. His current projects includes: Beamforming, Instrumentation, Signal Processing, and Education in Acoustics, Audio, and Vibration (more research information in his [RG profile](http://will.eng.br)).

## Cite us

M. M. Ackermann, W. D’A. Fonseca, P. H. Marezev, and F. C. Hirono. *Integration of multiple toolboxes for application in beamforming and aeroacoustics  (original: Integracão de múltiplas toolboxes para aplicação em beamforming e aeroacústica).* In 12th Iberoamerican Congress of Acoustics (FIA 2020/22) & Meeting of the Brazilian Society of Acoustics - Sobrac. Florianópolis, SC, Brazil, 2022. URL: <https://bit.ly/fia2022-augen>.

**BibTex**:

```bibtex
@article{augen-2022,
author = {Ackermann, Michael Markus and Fonseca, William {\relax D'A}ndrea, and Mareze, Paulo Henrique and Casagrande Hirono, Fábio},
title = {Integration of multiple toolboxes
for application in beamforming and aeroacoustics  (original: Integracão de múltiplas toolboxes para aplicação em beamforming e aeroacústica)},
booktitle = {In 12th Iberoamerican Congress of Acoustics (FIA 2020/22) \& Meeting of the Brazilian Society of Acoustics - Sobrac.},
date = {2022},
address = {Florianópolis, SC, Brazil},
url = {https://bit.ly/fia2022-augen}
}
```

## References

<a id="1">[1]</a> Sarradj, Ennes and Herold, Gert. *A Python framework for microphone array data processing (Acoular - Acoustic Testing and Source Mapping Software).* Applied Acoustics, 116:50–58, 2017. ISSN 0003-682X. DOI: [10.1016/j.apacoust.2016.09.015.](https://doi.org/10.1016/j.apacoust.2016.09.015.) The toolbox available at: <http://acoular.org>.

<a id="2">[2]</a> Casagrande Hirono, Fabio; Joseph, Phillip; and Fazi, Filippo M. *An Open–Source Implementation of Analytical Turbulence–Airfoil Interaction Noise Model*. In AIAA Aviation 2020 Forum, number AIAA 2020-2544, pages 1–21. American Institute of Aeronautics and Astronautics, 2020. DOI: [10.2514/6.2020-2544](https://doi.org/10.2514/6.2020-2544). The toolbox is available at: <https://github.com/fchirono/amiet_tools>.

<a id="3">[3]</a> Dietrich, Pascal; Guski, Martin; Pollow, Martin; Müller-Trapet, Markus; Masiero, Bruno; Scharrer, Ro man and Vorlaender, Michael. *ITA-Toolbox – An Open Source Matlab Toolbox for Acousticians*. In 38th German Annual Conference on Acoustics (DAGA), number 38, pages 151–152, Darmstadt, Germany, 2012. Available in: <https://pub.dega-akustik.de/DAGA_2012/data/articles/000164.pdf>. The toolbox is available at: <https://git.rwth-aachen.de/ita/toolbox>.

<a id="4">[4]</a> Fonseca, William D’Andrea; Mareze, Paulo H.; Mello, Felipe R. and Fonseca, Carlos Calixto. *Teaching Acoustical Beamforming via Active Learning Approach*. In 9th Berlin Beamforming Conference (BeBeC), number BeBeC-2022-D4, Berlim, Germany, June 2022. Available in: [BeBeC 2022](https://bit.ly/bebec2022).
