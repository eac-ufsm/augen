# -*- coding: utf-8 -*-
"""
Classes for beamforming with Acoular using Amiet Tools data.
=================
@Author: Michael Markus Ackermann
"""

from dataclasses import dataclass
from typing import List

from acoular import (
    BeamformerBase,
    BeamformerCapon,
    BeamformerDamas,
    BeamformerEig,
    BeamformerMusic,
    L_p,
    MicGeom,
    RectGrid,
    SamplesGenerator,
    SteeringVector,
)

from .dummies import DummyPowerSpectra


@dataclass
class __BasicBeamer:
    """A base class for SimpleBeamer and EasyBeamer.

    Args:
        block_size (int, optional): Block size value. Defaults to None.
        remove_diag (bool, optional): If True removes the diagonals from the
            beamformings. Defaults to None.
        modifier (float, optional): Modifier to help with the pressure level
            normalization. Defaults to None.

    Returns:
        SimpleBeamer instance.
    """

    block_size: int
    remove_diag: bool
    modifier: int

    def _init_time_dummy(self, frequency, bsize, chnumber) -> SamplesGenerator:
        """Initializes a dummy time data object.

        Returns:
            acoular.SamplesGenerator: A dummy signal processing block.
        """
        sample_frequency = frequency * bsize
        time_dummy = SamplesGenerator(
            sample_freq=sample_frequency, numchannels=chnumber
        )
        return time_dummy

    def _init_power_spectra(self, frequency, bsize, chnumber, csm) -> DummyPowerSpectra:
        """Initializes the cross spectral matrix (CSM) based on the instance
        giving attributes.

        Returns:
            DummyPowerSpectra: A dummy object based on acoular.PowerSpectra.
        """
        time_dummy = self._init_time_dummy(frequency, bsize, chnumber)

        ps = DummyPowerSpectra(
            time_data=time_dummy, csm=csm, numchannels=chnumber, block_size=bsize
        )
        ps.ind_high = 2
        ps.ind_low = 1
        return ps

    def _init_steering_vector(self, steering_vector):
        """Initializes the steering vector based on the instance
        giving attributes.

        Returns:
            DummySteeringVector: A dummy object based on acoular.SteeringVector.
        """
        st_vec = steering_vector

        class TempDummySteeringVector(SteeringVector):
            def steer_vector(self, f, ind=None):
                return st_vec

        return TempDummySteeringVector(grid=self.grid, mics=self.array)

    def _init_grid(self, grid) -> RectGrid:
        """Initializes the rectangular grid. Currently only supports
        rectangular grids.

        Raises:
            ValueError: If the grid isn't `rect` type raises an error.
            ValueError: If the grid type is not a `RectGrid` neither a `dict`
                raises an error.

        Returns:
            acoular.RectGrid: Acoular rectangular grid object.
        """
        if type(grid) == dict:
            if grid.get("type") == "rect":
                return RectGrid(
                    x_min=grid.get("x_min"),
                    x_max=grid.get("x_max"),
                    y_min=grid.get("y_min"),
                    y_max=grid.get("y_max"),
                    z=grid.get("z"),
                    increment=grid.get("increment"),
                )
            else:
                raise ValueError(f"Grid type is not defined!")
        elif type(grid) == RectGrid:
            return grid
        else:
            raise ValueError(f"Grid type isn't a RectGrid neither a dict!")


@dataclass
class SimpleBeamer(__BasicBeamer):
    """Simple object to help with the integration of acoular with amiet_tools.

    Args:
        data (AmietFrequencyData): AmietFrequencyData instance that holds the
            data to be used on the beamforming.
        array (acoular.MicGeom): Microphone array used on to generate the data
            and to be used for the beamforming.
        grid_config (dict): Dictionary holding the grid informations to be used
            on the beamforming.
        block_size (int, optional): Block size value, if none is giving it's
            going to use a default value of 128. Recomended to define a value,
            even if it's the same as the default of 128, to avoid warnings.
        remove_diag (bool, optional): If True removes the diagonals from the
            beamformings. Defaults to False.
        modifier (float, optional): Modifier to help with the pressure level
            normalization. Defaults to 0.

    Returns:
        SimpleBeamer instance.
    """

    def __init__(
        self,
        data: object,
        array: object,
        grid_info: dict,
        block_size: int = 128,
        remove_diag: bool = False,
        modifier: float = 0,
    ) -> None:
        self.data = data
        self.array = array
        self.grid_info = grid_info
        super().__init__(block_size, remove_diag, modifier)
        self.__post_init__()

    def __post_init__(self) -> None:
        """Post initializes the object to avoid conceptual OOP errors.

        Returns:
            None.
        """
        self.frequency = self.data.frequency
        self.grid = self._init_grid(self.grid_info)
        self.power_spectra = self._init_power_spectra(
            self.frequency, self.block_size, self.array.num_mics, self.data.csm
        )
        self.steering_vector = self._init_steering_vector(self.data.steering_vector)
        return None

    def get_beamforming(self, n: int = 1) -> List[float]:
        """Gets the beamforming using the basic delay-and-sum algorithm in the frequency domain.

        Observation: Working only for one frequency at the time.

        Args:
            n (int): Controls the width of the frequency bands considered.
                Defaults to 0 (single frequency line).
                =  =====================
                n  frequency band width
                =  =====================
                0  single frequency line
                1  octave band
                3  third-octave band
                n  1/n-octave band
                =  =====================

        Returns:
            List[float]: The sound pressure level, ready for plotting.
        """
        base = BeamformerBase(
            freq_data=self.power_spectra,
            steer=self.steering_vector,
            r_diag=self.remove_diag,
        )
        pressure = base.synthetic(self.frequency, n)
        # Normalizing by the maxium value and adding a modifier (if needed)
        pressure_level = L_p(pressure / pressure.max()) + self.modifier
        return pressure_level

    def get_damas(self, iter: int = 100, n: int = 1):
        """Gets the DAMAS deconvolution.

        Observation: Working only for single frequency.

        Args:
            iter (int, optional): Number of iterations. Defaults to 100.
            n (int): Controls the width of the frequency bands considered.
                Defaults to 0 (single frequency line).
                =  =====================
                n  frequency band width
                =  =====================
                0  single frequency line
                1  octave band
                3  third-octave band
                n  1/n-octave band
                =  =====================

        Returns:
            List[float]: The sound pressure level, ready for plotting.
        """
        base = self.get_beamforming(n)
        damas = BeamformerDamas(beamformer=base, n_iter=iter)
        pressure = damas.synthetic(self.frequency, n)
        pressure_level = L_p(pressure / pressure.max()) + self.modifier
        return pressure_level

    def get_eigen(self, num: int = -1, n: int = 1):
        """Gets the beamforming using eigenvalue and eigenvector techniques.

        Observation: Working only for single frequency.

        Args:
            num (int, optional): Number of eigenvalue. Defaults to -1.
            n (int): Controls the width of the frequency bands considered.
                Defaults to 0 (single frequency line).
                =  =====================
                n  frequency band width
                =  =====================
                0  single frequency line
                1  octave band
                3  third-octave band
                n  1/n-octave band
                =  =====================

        Returns:
            List[float]: The sound pressure level, ready for plotting.
        """
        eig = BeamformerEig(
            freq_data=self.power_spectra,
            steer=self.steering_vector,
            r_diag=self.remove_diag,
            n=num,
        )
        pressure = eig.synthetic(self.frequency, n)
        pressure_level = L_p(pressure / pressure.max()) + self.modifier
        return pressure_level

    def get_music(self, nsources: int = 1, n: int = 1):
        """Gets the beamforming using the MUSIC algorithm.

        Observation: Working only for single frequency.

        Args:
            nsources (int, optional): Assumed number of sources. Defaults to 1.
            n (int, optional): Width of the frequency bands considered.
                Defaults to 1 (octave band).
                =  =====================
                n  frequency band width
                =  =====================
                0  single frequency line
                1  octave band
                3  third-octave band
                n  1/n-octave band
                =  =====================

        Returns:
            List[float]: The sound pressure level, ready for plotting.
        """
        base = BeamformerMusic(
            freq_data=self.power_spectra, steer=self.steering_vector, n=nsources
        )
        pressure = base.synthetic(self.frequency, n)
        # Normalizing by the max value
        pressure_level = L_p(pressure / pressure.max()) + self.modifier
        return pressure_level

    def get_capon(self, n: int = 1) -> List[float]:
        """Gets the beamforming using the Capon (Mininimum Variance) algorithm.

        Observation: Working only for single frequency.

        Args:
            n (int): Controls the width of the frequency bands considered.
                Defaults to 1 (octave band).
                =  =====================
                n  frequency band width
                =  =====================
                0  single frequency line
                1  octave band
                3  third-octave band
                n  1/n-octave band
                =  =====================

        Returns:
            List[float]: The sound pressure level, ready for plotting.
        """
        base = BeamformerCapon(
            freq_data=self.power_spectra,
            steer=self.steering_vector,
            r_diag=self.remove_diag,
        )
        pressure = base.synthetic(self.frequency, n)
        # Normalizing by the max value
        pressure_level = L_p(pressure / pressure.max()) + self.modifier
        return pressure_level


@dataclass
class EasyBeamer(__BasicBeamer):
    """A easier-to-use version of SimpleBeamer, where does almost everything by
        itself.

    Args:
        data (AmietDataReader): AmietDataReader instance that holds the
            data to be used on the beamforming.
        block_size (int, optional): Block size value. Defaults to 128.
            even if it's the same as the default of 128, to avoid warnings.
        remove_diag (bool, optional): If True removes the diagonals from the
            beamformings. Defaults to False.
        modifier (int, optional): Modifier to help with the pressure level
            normalization. Defaults to 0.

    Returns:
        EasyBeamer instance.
    """

    def __init__(
        self,
        data: object,
        block_size: int = 128,
        remove_diag: bool = False,
        modifier: float = 0,
    ) -> None:
        self.data = data
        super().__init__(block_size, remove_diag, modifier)
        self.__post_init__()

    def __post_init__(self) -> None:
        """Post initializes the object to avoid conceptual OOP errors.

        Returns:
            None.
        """

        self.frequencies = self.data.frequencies
        self.grid = self._init_grid(self.data.get_grid())
        self.array = MicGeom(mpos_tot=self.data.get_mic_array()[1])
        return None

    def __init_frequency_data(self, frequency: float) -> None:
        """Initializes the power spectra and steering vector for Acoular after
            the frequency data is extracted as an AmietFrequencyData instance.

        Args:
            frequency (float): Frequency to extract the data. Defaults to None.
        """

        if frequency in self.frequencies:
            freq_data = self.data.get_frequency_data(frequency)
            self._power_spectra = self._init_power_spectra(
                freq_data.frequency,
                self.block_size,
                self.array.num_mics,
                freq_data.csm,
            )
            self._steering_vector = self._init_steering_vector(
                freq_data.steering_vector
            )
        else:
            raise ValueError(
                f"""The given `frequency` isn\'t in the
                    avalaible frequencies.\nList of the availabe
                    frequencies: {self.frequencies}."""
            )
        return None

    def get_beamforming(self, frequency: float = None, n: int = 1) -> List[float]:
        """Gets the beamforming using the basic delay-and-sum algorithm in the frequency domain.

        Observation: Working only for single frequency.

        Args:
            frequency (float): Frequency. Defaults to None.
            n (int): Controls the width of the frequency bands considered.
                Defaults to 1 (octave band).
                =  =====================
                n  frequency band width
                =  =====================
                0  single frequency line
                1  octave band
                3  third-octave band
                n  1/n-octave band
                =  =====================

        Returns:
            List[float]: The sound pressure level, ready for plotting.
        """
        self.__init_frequency_data(frequency)
        base = BeamformerBase(
            freq_data=self._power_spectra,
            steer=self._steering_vector,
            r_diag=self.remove_diag,
        )
        pressure = base.synthetic(frequency, n)
        # Normalizing by the max value
        pressure_level = L_p(pressure / pressure.max()) + self.modifier
        return pressure_level

    def get_damas(self, frequency: float = None, iter: int = 100, n: int = 1):
        """Gets the DAMAS deconvolution.

        Observation: Working only for single frequency.

        Args:
            frequency (float): Frequency. Defaults to None.
            iter (int, optional): Number of iterations. Defaults to 100.
            n (int, optional): Width of the frequency bands considered.
                Defaults to 1 (octave band).
                =  =====================
                n  frequency band width
                =  =====================
                0  single frequency line
                1  octave band
                3  third-octave band
                n  1/n-octave band
                =  =====================

        Returns:
            List[float]: The sound pressure level, ready for plotting.
        """
        self.__init_frequency_data(frequency)
        base = BeamformerBase(
            freq_data=self._power_spectra,
            steer=self._steering_vector,
            r_diag=self.remove_diag,
        )
        damas = BeamformerDamas(beamformer=base, n_iter=iter)
        pressure = damas.synthetic(frequency, n)
        pressure_level = L_p(pressure / pressure.max()) + self.modifier
        return pressure_level

    def get_eigen(self, frequency: float = None, num: int = -1, n: int = 1):
        """Gets the beamforming using eigenvalue and eigenvector techniques.

        Observation: Working only for single frequency.

        Args:
            frequency (float): Frequency. Defaults to None.
            num (int, optional): Number of eigenvalue. Defaults to -1.
            n (int, optional): Width of the frequency bands considered.
                Defaults to 1 (octave band).
                =  =====================
                n  frequency band width
                =  =====================
                0  single frequency line
                1  octave band
                3  third-octave band
                n  1/n-octave band
                =  =====================

        Returns:
            List[float]: The sound pressure level, ready for plotting.
        """
        self.__init_frequency_data(frequency)
        eig = BeamformerEig(
            freq_data=self._power_spectra,
            steer=self._steering_vector,
            r_diag=self.remove_diag,
            n=num,
        )
        pressure = eig.synthetic(frequency, n)
        pressure_level = L_p(pressure / pressure.max()) + self.modifier
        return pressure_level

    def get_music(self, frequency: float = None, nsources: int = 1, n: int = 1):
        """Gets the beamforming using the MUSIC algorithm.

        Observation: Working only for single frequency.

        Args:
            frequency (float): Frequency. Defaults to None.
            nsources (int, optional): Assumed number of sources. Defaults to 1.
            n (int, optional): Width of the frequency bands considered.
                Defaults to 1 (octave band).
                =  =====================
                n  frequency band width
                =  =====================
                0  single frequency line
                1  octave band
                3  third-octave band
                n  1/n-octave band
                =  =====================

        Returns:
            List[float]: The sound pressure level, ready for plotting.
        """
        self.__init_frequency_data(frequency)
        base = BeamformerMusic(
            freq_data=self._power_spectra, steer=self._steering_vector, n=nsources
        )
        pressure = base.synthetic(frequency, n)
        # Normalizing by the max value
        pressure_level = L_p(pressure / pressure.max()) + self.modifier
        return pressure_level

    def get_capon(self, frequency: float = None, n: int = 1) -> List[float]:
        """Gets the beamforming using the Capon (Mininimum Variance) algorithm.

        Observation: Working only for single frequency.

        Args:
            frequency (float): Frequency. Defaults to None.
            n (int): Controls the width of the frequency bands considered.
                Defaults to 1 (octave band).
                =  =====================
                n  frequency band width
                =  =====================
                0  single frequency line
                1  octave band
                3  third-octave band
                n  1/n-octave band
                =  =====================

        Returns:
            List[float]: The sound pressure level, ready for plotting.
        """
        self.__init_frequency_data(frequency)
        base = BeamformerCapon(
            freq_data=self._power_spectra,
            steer=self._steering_vector,
            r_diag=self.remove_diag,
        )
        pressure = base.synthetic(frequency, n)
        # Normalizing by the max value
        pressure_level = L_p(pressure / pressure.max()) + self.modifier
        return pressure_level
