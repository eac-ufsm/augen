# -*- coding: utf-8 -*-
"""
Classes for handling data
=================
@Author: Michael Markus Ackermann
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Tuple

from acoular import RectGrid
from amiet_tools import (
    AirfoilGeom,
    FrequencyVars,
    Phi_2D,
    ShearLayer_matrix,
    TestSetup,
    calc_airfoil_Sqq,
    dipole_shear,
    ky_vector,
    rect_grid,
)
from h5py import File
from numpy import (
    array,
    complex64,
    concatenate,
    float64,
    int64,
    linalg,
    ndarray,
    ones,
    pi,
    transpose,
    zeros,
    zeros_like,
)

from .utils import index_of_value


@dataclass
class AmietFrequencyData:
    """Class used to store a frequency data (frequency, csm and steering_vector)
        from a HDF5 file that is gettered with the use of AmietDataReader.
    Args:
        frequency (float): Frequency of the data.
        steering_vector (ndarray): Steering vector.
        csm (ndarray): Cross spectral matrix.

    Returns:
        AmietFrequencyData instance.
    """

    frequency: float
    steering_vector: ndarray
    csm: ndarray

    def __repr__(self) -> str:
        return f"AmietFrequencyData for {self.frequency} Hz."


@dataclass
class AmietDataReader:
    """Class used to create object to extract the data contained in tha HDF5 file.

    Args:
        file_name (str): Name of the HDF5 file (with the directory location).

    Returns:
        AmietDataReader instance.
    """

    file_name: str

    def __post_init__(self) -> None:
        """Post initializes the object to avoid conceptual OOP errors.

        Returns:
            None.
        """

        self.frequencies = self.__extract_frequencies()
        return None

    def __extract_frequencies(self):
        """Handles the data extraction from the HDF5 file.

        Returns:
            frequencies: List of frequencies inside the group.
        """
        file_instance = File(self.file_name, "r")
        fq = file_instance.get("Frequency data")
        frequencies = fq.get("frequencies")[()]
        file_instance.close()

        return frequencies

    def get_frequency_data(self, frequency: float) -> AmietFrequencyData:
        """Extracts the data for the frequency in the given index position.

        Args:
            frequency (float): Frequency to extract.

        Returns:
            AmietFrequencyData: Object instance with the data of the frequency.
        """
        f_pos = index_of_value(self.frequencies, frequency)
        hdf = File(self.file_name, "r")
        fq = hdf.get("Frequency data")
        freq_x = fq.get(f"freq_{f_pos}")
        freq = float(freq_x.get("frequency")[()])
        steering_vector = transpose(freq_x.get("steering_vector")[()])
        # CSM for Acoular: (number of frequencies, numchannels, numchannels).
        raw_csm = freq_x.get("CSM")[()]
        csm = [zeros_like(raw_csm)]
        csm.append(raw_csm)
        csm = array(csm)
        hdf.close()

        return AmietFrequencyData(freq, steering_vector, csm)

    def get_mic_array(self) -> Tuple[str, ndarray, int]:
        """Extract the related informations of the microphe array used in the
            data generation.

        Returns:
            Tuple[str, np.ndarray, int]: name of the xml file, microphone array
                matrix and number of microphones.
        """
        hdf = File(self.file_name, "r")
        ma = hdf.get("Microphone array")  # ma -> Microphone array
        file_name = ma.get(f"file_name")[()]
        mic_array = ma.get(f"mic_array")[()]
        mics_number = ma.get(f"mics_number")[()]
        hdf.close()
        return (file_name, mic_array, mics_number)

    def get_grid(self) -> RectGrid:
        """Extract the related information of the grid used in the data
            generation and returns an acoular.RectGrid instance.

        Returns:
            RectGrid: RectGrid object.
        """
        hdf = File(self.file_name, "r")
        gi = hdf.get("Grid info")  # gi -> Grid info
        return RectGrid(
            x_min=gi.get("x_min")[()],
            x_max=gi.get("x_max")[()],
            y_min=gi.get("y_min")[()],
            y_max=gi.get("y_max")[()],
            z=gi.get("z")[()],
            increment=gi.get("increment")[()],
        )

    def get_airfoil(self) -> AirfoilGeom:
        """Extract the airfoil geometry used in the data generation and returns
            an AirfoilGeom instance.

        Returns:
            AirfoilGeom : AirfoilGeom object.
        """
        hdf = File(self.file_name, "r")
        ag = hdf.get("AirfoilGeom")  # ag -> AirfoilGeom
        b = ag.get(f"b")[()]
        d = ag.get(f"d")[()]
        Nx = ag.get(f"Nx")[()]
        Ny = ag.get(f"Ny")[()]
        hdf.close()
        return AirfoilGeom(b, d, Nx, Ny)

    def get_setup(self) -> TestSetup:
        """Extract the test setup used in the main data generation and returns
            an TestSetup instance.

        Returns:
            TestSetup: TestSetup object.
        """
        hdf = File(self.file_name, "r")
        ts = hdf.get("TestSetup")  # ts -> TestSetup
        c0 = ts.get(f"c0")[()]
        rho0 = ts.get(f"rho0")[()]
        p_ref = ts.get(f"p_ref")[()]
        Ux = ts.get(f"Ux")[()]
        turb_intensity = ts.get(f"turb_intensity")[()]
        length_scale = ts.get(f"length_scale")[()]
        z_sl = ts.get(f"z_sl")[()]
        hdf.close()
        return TestSetup(c0, rho0, p_ref, Ux, turb_intensity, length_scale, z_sl)

    def get_run_data(self) -> Tuple[str, str, str]:
        """Extract the running data information used in the data generation.

        Returns:
            Tuple[str, str, str]: date of run, start time and end time of the
                data generation.
        """
        hdf = File(self.file_name, "r")
        rd = hdf.get("Run data")  # rd -> Run data
        date = rd.get(f"date")[()]
        start_time = rd.get(f"start_time")[()]
        end_time = rd.get(f"end_time")[()]
        hdf.close()
        return (date, start_time, end_time)

    def __str__(self) -> str:
        # Get only the date value, and ignore the others.
        date, *_ = self.get_run_data()
        return f"""AmietData for:
                    frequencies -> {self.frequencies}
                    created on -> {date}
                """


@dataclass
class AmietDataGenerator:
    """Object with the focus to generate the data for the Airfoil, using the
        amiet_tools toolbox by Fabio Casagrande Hirono.

    Args:
        test_setup (object): TestSetup object instance.
        airfoil_geom (object): AirfoilGeom object instance.
        mic_array (object): Acoular's MicArray instane.
        frequencies (list): List containing all the frequencies values to be
            used. If it isn't a list it would also work, but needs to be an int
            or a float.
        distance (float): If the array position in z axis if different from
            the one in the MicArray object instance.
        scan_length (list): Maximum size of the scan grid.
        scan_spacing (list): Spacing between the scanning points.
        data_name (str): Data file name, used for saving the data file.
            Defaults to 'Unknown'.
        steps (bool): If True, prints the code steps with timestamp.
            Defaults to False.
    Returns:
        GenerateData instance.
    """

    test_setup: object
    airfoil_geom: object
    mic_array: object
    frequencies: list
    distance: float
    scan_length: list
    scan_spacing: list
    data_name: str = "Unknown"
    steps: bool = False

    def __post_init__(self) -> None:
        """Post initializes the object to configure the future steps to generate
        the airfoil simulated data.

        Returns:
            None.
        """
        # Starts an empty data file
        hdf = File(f"{self.data_name}.h5", "w")
        hdf.close()

        self._init_test_setup()
        self._init_grid_info()
        if self.airfoil_geom:
            self._init_airfoil_geom()
            self._XYZ_airfoil_calc = self._XYZ_airfoil.reshape(3, self._Nx * self._Ny)
        if self.mic_array:
            self._XYZ_array = self._init_mic_array()

        return None

    def _init_mic_array(self) -> ndarray:
        """Initiliazes the microphone array as a numpy array, it uses the
        object from the Acoular toolbox, MicArray. It also checks if a different
        distance it given and applies it. In the end saves the microphone array
        positions to the HDF5 file.

        Returns:
            None.
        """
        self._M = self.mic_array.num_mics

        if self.distance:
            z = self.distance * ones(self._M)
            arr = array([self.mic_array.mpos[0], self.mic_array.mpos[1], z])
        else:
            arr = array(
                [self.mic_array.mpos[0], self.mic_array.mpos[1], self.mic_array.mpos[2]]
            )
            self.distance = self.mic_array.mpos[2][0]

        hdf = File(f"{self.data_name}.h5", "a")
        ma = hdf.create_group("Microphone array")
        ma.create_dataset("file_name", data=self.mic_array.basename)
        ma.create_dataset("mics_number", data=self._M, dtype=int64)
        ma.create_dataset("mic_array", data=arr, dtype=float64)
        hdf.close()

        self.__timeit("Microphone array has been successfully initialized!")

        return arr

    def _init_test_setup(self) -> None:
        """Extract the data from the TestSetup object, using an already existing
        instance, passed to the class when setting up the object. Also saves the
        necessary data to the HDF5 file.

        Returns:
            None.
        """
        (
            self._c0,
            self._rho0,
            self._p_ref,
            self._Ux,
            self._turb_intensity,
            self._length_scale,
            self._z_sl,
            self._Mach,
            self._beta,
            self._flow_param,
            self._dipole_axis,
        ) = self.test_setup.export_values()

        hdf = File(f"{self.data_name}.h5", "a")
        ts = hdf.create_group("TestSetup")
        ts.create_dataset("c0", data=self._c0, dtype=float64)
        ts.create_dataset("rho0", data=self._rho0, dtype=float64)
        ts.create_dataset("p_ref", data=self._p_ref, dtype=float64)
        ts.create_dataset("Ux", data=self._Ux, dtype=float64)
        ts.create_dataset("turb_intensity", data=self._turb_intensity, dtype=float64)
        ts.create_dataset("length_scale", data=self._length_scale, dtype=float64)
        ts.create_dataset("z_sl", data=self._z_sl, dtype=float64)
        hdf.close()

        self.__timeit("TestSetup variables have been successfully initialized!")
        return None

    def _init_airfoil_geom(self) -> None:
        """Initializes ArifoilGeom object and saves the necessary data to the
        HDF5 file.

        Returns:
            None.
        """
        (
            self._b,
            self._d,
            self._Nx,
            self._Ny,
            self._XYZ_airfoil,
            self._dx,
            self._dy,
        ) = self.airfoil_geom.export_values()

        hdf = File(f"{self.data_name}.h5", "a")
        ag = hdf.create_group("AirfoilGeom")
        ag.create_dataset("b", data=self._b, dtype=float64)
        ag.create_dataset("d", data=self._d, dtype=float64)
        ag.create_dataset("Nx", data=self._Nx, dtype=int64)
        ag.create_dataset("Ny", data=self._Ny, dtype=int64)
        hdf.close()

        self.__timeit("AirfoilGeom variables have been successfully initialized!")
        return None

    def _init_grid_info(self) -> None:
        """Saves the grid data to the HDF5 file.

        Returns:
            None.
        """

        hdf = File(f"{self.data_name}.h5", "a")
        gi = hdf.create_group("Grid info")
        gi.create_dataset("scan_length", data=self.scan_length, dtype=float64)
        gi.create_dataset("scan_spacing", data=self.scan_spacing, dtype=float64)
        gi.create_dataset("x_min", data=-self.scan_length[0] / 2, dtype=float64)
        gi.create_dataset("x_max", data=self.scan_length[0] / 2, dtype=float64)
        gi.create_dataset("y_min", data=-self.scan_length[1] / 2, dtype=float64)
        gi.create_dataset("y_max", data=self.scan_length[1] / 2, dtype=float64)
        gi.create_dataset(
            "increment",
            data=(
                self.scan_spacing[0]
                if self.scan_spacing[0] == self.scan_spacing[1]
                else 0
            ),
            dtype=float64,
        )
        gi.create_dataset("z", data=self.distance, dtype=float64)
        hdf.close()
        self.__timeit("Grid info has been successfully initialized!")
        return None

    def _frequency_vars(self, frequency: float) -> None:
        """Intializes the FrequencyVars object from amiet_tools, that will be
        used to generate the data.

        Args:
            frequency (float): Frequency value to be used. If it isn't a float
            it will cast into one.

        Returns:
            None.
        """
        self._frequency = float(frequency)
        self._FreqVars = FrequencyVars(self._frequency, self.test_setup)
        (self._k0, self._Kx, self._Ky_crit) = self._FreqVars.export_values()
        self.__timeit("FrequencyVars variables have been successfully initialized!")
        return None

    def _fwd_problem(self) -> None:
        """Calculates the general ShearLayer Matrix from amiet_tools. This
        matrix is the same for all frequencies and only depends on the airfoil
        geometry and microphone array to be used.

        Returns:
            None.
        """
        self._T_sl_fwd, self._XYZ_sl_fwd = ShearLayer_matrix(
            self._XYZ_airfoil_calc, self._XYZ_array, self._z_sl, self._Ux, self._c0
        )
        self.__timeit("foward problem has been successfully calculated!")
        return None

    def _pre_csm(self) -> None:
        """Previous step before the actual CSM is calculated, here it calculates
        the aerofoil surface pressure jump cross-spectral density matrix.

        Returns:
            None.
        """
        # vector of spanwise gust wavenumbers
        self._Ky = ky_vector(self._b, self._d, self._k0, self._Mach, self._beta)
        # Turbulence spectrum (von Karman)
        self._Phi2 = Phi_2D(
            self._Kx,
            self._Ky,
            self._Ux,
            self._turb_intensity,
            self._length_scale,
            model="K",
        )[0]
        # calculate source CSM
        self._Sqq, self.Sqq_dxy = calc_airfoil_Sqq(
            self.test_setup, self.airfoil_geom, self._FreqVars, self._Ky, self._Phi2
        )
        self._Sqq *= self.Sqq_dxy  # apply weighting for airfoil grid areas
        self.__timeit("Pre-CSM has been successfully calculated!")

        return None

    def _calculate_csm(self) -> None:
        """Calculates the CSM with the use of the ShearLayer Matrix from the
        foward problem step.

        Returns:
            None.
        """
        # create fwd transfer function
        self._G_fwd = dipole_shear(
            self._XYZ_airfoil_calc,
            self._XYZ_array,
            self._XYZ_sl_fwd,
            self._T_sl_fwd,
            self._k0,
            self._c0,
            self._Mach,
        )
        # CSM calculation
        self._csm = (self._G_fwd @ self._Sqq @ self._G_fwd.conj().T) * 4 * pi
        self.__timeit("CSM has been successfully calculated!")
        return None

    def _scan_grid(self) -> None:
        """Generates the scaning grid related data.

        Returns:
            None.
        """

        scan_xy = rect_grid(self.scan_length, self.scan_spacing)
        # Número de pontos do plano
        self._N = scan_xy.shape[1]
        # Create array with (x, y, z) coordinates of the scan points
        self._scan_xyz = concatenate((scan_xy, zeros((1, self._N))))
        self.__timeit("Scanning grid has been successfully calculated!")

        return None

    def _pre_steering_vector(self) -> None:
        """Obtains the propagation time and shearlayer crossing point for
        every scan-mic pair.

        Returns:
            None.
        """
        self._T_sl, self._XYZ_sl = ShearLayer_matrix(
            self._scan_xyz, self._XYZ_array, self._z_sl, self._Ux, self._c0
        )
        self.__timeit("Shearlayer matrix has been successfully calculated!")
        return None

    def _calculate_steering_vector(self) -> None:
        """Applies the classical beamforming algorithm to get the steering
        vector.

        Returns:
            None.
        """
        # Creates steering vector and beamforming filters
        self._G_grid = zeros((self._M, self._N), "complex")
        self._W = zeros((self._M, self._N), "complex")
        # monopole grid without flow
        # G_grid = ArT.monopole3D(scan_xyz, XYZ_array, k0)
        # dipole grid with shear layer correction
        self._G_grid = dipole_shear(
            self._scan_xyz,
            self._XYZ_array,
            self._XYZ_sl,
            self._T_sl,
            self._k0,
            self._c0,
            self._Mach,
        )
        # calculate beamforming filters
        for n in range(self._N):
            self._W[:, n] = self._G_grid[:, n] / (
                linalg.norm(self._G_grid[:, n], ord=2) ** 2
            )

        self.__timeit("Beamforming algorithm has been successfully calculated!")
        return None

    def run(self) -> None:
        """Runs the simulation to generate the data.

        Returns:
            None.
        """
        hdf = File(f"{self.data_name}.h5", "a")

        rd = hdf.create_group("Run data")
        rd.create_dataset("date", data="{}".format(datetime.now().strftime("%d/%m/%Y")))
        rd.create_dataset(
            "start_time", data="{}".format(datetime.now().strftime("%H:%M:%S"))
        )

        fd = hdf.create_group("Frequency data")
        fd.create_dataset("frequencies", data=array(self.frequencies), dtype=float64)

        self.__timeit("Starting the 'foward problem'...")
        self._fwd_problem()
        self.__timeit(
            "The 'foward problem' is finished.\nEntering the frequency loop..."
        )
        for i in range(len(self.frequencies)):
            self.__timeit(f"Current frequency: {self.frequencies[i]} Hz")
            self._frequency_vars(self.frequencies[i])
            self._pre_csm()
            self._calculate_csm()
            self._scan_grid()
            self._pre_steering_vector()
            self._calculate_steering_vector()
            freq_x = fd.create_group(f"freq_{i}")
            freq_x.create_dataset("frequency", data=self.frequencies[i], dtype=float64)
            freq_x.create_dataset("steering_vector", data=self._W, dtype=complex64)
            freq_x.create_dataset("CSM", data=self._csm, dtype=complex64)
            self.__timeit(f"Finished {self.frequencies[i]} Hz")

        rd.create_dataset(
            "end_time", data="{}".format(datetime.now().strftime("%H:%M:%S"))
        )
        hdf.close()

        self.__timeit("All frequencies have been calculated. Simulation as ended!")
        return None

    def __timeit(self, message) -> None:
        """Internal class function used for to timestamp the steps of the
        simulation, only used if self.steps is set to True.

        Args:
            message (str): message to follow the timestamp.

        Returns:
            None
        """
        if self.steps == True:
            dt_obj = datetime.now()
            t_obj = str(dt_obj.time())[:-7]
            print(f"{t_obj} - {message}")
            del dt_obj, t_obj
        return None
