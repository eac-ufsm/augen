function [] = xml_save_array(array, fname, toolbox)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Function tested under MATLAB (version: R2021a)
    %
    % Function used to save a microphe array in a XML file, following the format
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
    %       array = Microphone array geometry positions
    %       fname = XML file name to save (also used to set the attribute "name"
    %               value inside XML file)
    %       toolbox = 'none' -> If the array is an array.
    %                 'beamap' -> If the array is a MicArray object (from the Beamap Toolbox)
    %                 'ita' -> If the array is an itaMicArray object (from the ITA-Toolbox)
    %
    %   Example:
    %       xml_save_array(spiral, 'spiral_64', 'beamap');
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if nargin < 3; toolbox = 'none'; end
    if ~exist('toolbox', 'var') || isempty(toolbox); toolbox = 'none'; end

    % Extracts the positions of the microphone array into temp. variables
    if strcmp(string(toolbox), 'none')
        x = array(:, 1);
        y = array(:, 2);
        z = array(:, 3);
        mics = length(x);
    elseif strcmp(string(toolbox), 'beamap')
        x = array.position('x');
        y = array.position('y');
        z = array.position('z');
        mics = array.n_mic;
    elseif strcmp(string(toolbox), 'ita')
        x = array.x;
        y = array.y;
        z = array.z;
        mics = array.nPoints;
    else
        error('"toolbox" must either be "none", "beamap" or "ita"!')
    end

    docNode = com.mathworks.xml.XMLUtils.createDocument('MicArray'); % To be changed if it breaks
    marr = docNode.getDocumentElement;
    marr.setAttribute('name', fname);

    if ~endsWith(fname, '.xml')
        fname = [fname, '.xml']; % Adds .xml to the end of the fname string
    end

    disp('Formating microphone array positions in to XML format!');

    for idx = 1:mics
        curr_node = docNode.createElement('pos');

        curr_file = ['Point ' num2str(idx)];
        curr_node.setAttribute('Name', curr_file);
        curr_node.setAttribute('x', num2str(round(x(idx), 6)));
        curr_node.setAttribute('y', num2str(round(y(idx), 6)));
        curr_node.setAttribute('z', num2str(round(z(idx), 6)));

        marr.appendChild(curr_node);
    end

    xmlwrite(fname, docNode);
    disp('XML file was successfully saved!');

end
