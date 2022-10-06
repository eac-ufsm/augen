# Matlab

The **Matlab** folder includes functions used to read and write XML files, as well as saving in HDF5 files the data from the microphone array _point spread function_ (PSF).

## Available functions

The following functions written in **Matlab** are available:

- **xml_read_array:** read the XML file of the microphone array geometry.
- **xml_save_array:** write the XML file with the microphone array geometry.
- **h5_save_bw_dr:** save the microphone array _beamwidth_ and _dynamic range_, obtained from the PSF simulation, in an HDF5 file. This function also saves into the HDF5 file the: _frequency_ list of queried frequencies; _distance_ from the punctual source; aperture _angle_ of the array; and the _image size_ used in the PSF.
