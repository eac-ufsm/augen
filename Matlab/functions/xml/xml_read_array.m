function [array] = xml_read_array(fname, toolbox)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Function tested under MATLAB (version: R2021a)
    %
    % Function used to read a microphe array in a XML file, following the format
    % used by Acoular (toolbox in Python for beamforming).
    %
    % NOTICE: The user must have Beamap toolbox or ITA-Toolbox installed to
    % this function to work without any errors.
    %
    %   Made by: Michael Markus Ackermann
    %   Changed by: Michael Markus Ackermann
    %
    %   Last change: 07/06/2022
    %
    %   Parameters:
    %       fname = XML file name
    %       toolbox = 'none' -> Returns a matrix os NumberOfMics x 3
    %                 'beamap' -> Returns a MicArray object (from the Beamap Toolbox)
    %                 'ita' -> Returns an itaMicArray object (from the ITA-Toolbox)
    %
    %   Example:
    %       spiral64_arr = xml_read_array('spiral_64.xml', 'beamap');
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if nargin < 2; toolbox = 'none'; end
    if ~exist('toolbox', 'var') || isempty(toolbox); toolbox = 'none'; end

    xmlObj = readstruct(fname);
    mpos = zeros(length(xmlObj.pos), 3);

    for i = 1:length(xmlObj.pos)
        mpos(i, 1) = xmlObj.pos(i).xAttribute;
        mpos(i, 2) = xmlObj.pos(i).yAttribute;
        mpos(i, 3) = xmlObj.pos(i).zAttribute;
    end

    disp('Microphone array positions extracted from XML file!');

    if strcmp(toolbox, 'none')
        disp('Since a toolbox was not defined, initiliazing microphone array with default configuration.');
        array = [mpos(:, 1) mpos(:, 2) mpos(:, 3)];
        disp(['Returning a matrix of shape ', num2str(length(mpos(:, 1))), 'x3']);
    elseif strcmp(toolbox, 'beamap')
        disp('Trying to initiliaze the microphone array with Beamap!');
        array = MicArray('x', mpos(:, 1), 'y', mpos(:, 2), 'z', mpos(:, 3));
        disp('Microphone array initialized with Beamap!');
    elseif strcmp(toolbox, 'ita')
        disp('Trying to initiliaze the microphone array with ITA-Toolbox!');
        array = itaMicArray([mpos(:, 1) mpos(:, 2) mpos(:, 3)], 'cart');
        disp('Microphone array initialized with ITA-Toolbox!');
    else
        error('"toolbox" must either be "none", "beamap" or "ita"!');
    end
