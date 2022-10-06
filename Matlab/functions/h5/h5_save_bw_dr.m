function [] = h5_save_bw_dr(fname, farray, distance, angle, image_size, dr, bw)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Function tested under MATLAB (version: R2021a)
    %
    % Function used to save beamwidth and dynamic range data of a microphone array
    % PSF simulation, using the Beamap toolbox.
    %
    % NOTICE 1: The user must have Beamap toolbox or ITA-Toolbox installed to
    % this function to work without any errors.
    %
    % NOTICE 2: Also saves important data about the PSF simulation, like distance,
    % frequencies, and others.
    %
    %   Made by: Michael Markus Ackermann
    %   Changed by: Michael Markus Ackermann
    %
    %   Last change: 07/06/2022
    %
    %   Parameters:
    %       fname = H5 file name to save
    %       farray = frequencies array
    %       distance = distance of the array
    %       angle = aperture angle of the PSF sim.
    %       image_size = size of the image (size x size (m))
    %       dr = array with the dynamic range
    %       bw = array with the beamwidth
    %
    %   Example:
    %       h5_save_bw_dr(x)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if ~endsWith(fname, '.h5')
        fname = append(fname, '.h5'); % Appends .h5 to the end of the fname string
    end

    h5.frequencies = farray; % Frequencies array

    h5.distance = distance; h5.array_angle = angle; % Distance and aperture angle

    h5.image_size = image_size; % Image size for x and y

    h5.dynamic_range = dr; h5.beamwidth = bw; % Data arrays extracted from the PSF simulation

    fields = fieldnames(h5); nfs = length(fields);

    if isfile(fname) % Only allows to save if the file doesn't exist!
        error('A HDF5 file with that name already exists! Please use a different file name.');
    else
        % For each struct field creates a H5 attribute and saves the respective
        % data
        for i = 1:nfs
            cfield = string(fields(i, :));
            h5create(fname, append('/', cfield), size(h5.(cfield)));
            h5write(fname, append('/', cfield), h5.(cfield));
        end

        disp(append(fname, ' was successfully created!'));
    end

end
