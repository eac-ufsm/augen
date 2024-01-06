# examples

This folder contains scripts that focus on exemplifying the usage of the toolbox, with scripts well documented. The routines are offered as a tutorial, also as a real application example.

## fia22

The folder named **fia22** contains scripts that were used for the creation of figures presented in the article published at the **Iberoamerican Congress of Acoustics (FIA 2020/22) and the Meeting of the Brazilian Society of Acoustics - Sobrac**.

To prevent the user from re-synthesizing the data, folder **fia22** has a subfolder named **supplies**, which contains the data used in the article. The folder also provides the **XML** files of the microphone array geometry (following the file standard adopted by the Acoular development team). Additionally, a folder named **images** contains the figures used in the article but adjusted to the English language.

## Scripts

1. ```augen_data_gen.py```: generates the data, the same as the one presented in the paper.
2. ```augen_beamforming.py```: plots the results, the same as the one presented in the paper.
3. ```common_functions.py```: it's a collective of functions that are used in ```augen_beamforming.py```, to make the code shorter and easier to understand.