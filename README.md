<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ariensligar/5G-Wizard">
    <img src="images/logo.png" alt="Logo" width="200" height="200">
  </a>

<h3 align="center">Ansys 5G Wizard</h3>

  <p align="center">
    project_description
    <br />
    <a href="https://github.com/ariensligar/5G-Wizard"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/ariensligar/5G-Wizard">View Demo</a>
    ·
    <a href="https://github.com/ariensligar/5G-Wizard/issues">Report Bug</a>
    ·
    <a href="https://github.com/ariensligar/5G-Wizard/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://github.com/ariensligar/5G-Wizard)

The Ansys 5G Wizard can be used to calculate Power Density or Cumulative Distribution Function. These calculations use a codebook to define the mag/phase value on ports for each beam ID. The codebook definition will be imported into your HFSS design, where you can now control the mag/phase on all ports  by simply changing the post processing variable “BeamID.”

Power Density (PD): 
The PD is calculated based on IEC_IEEE_63195-2_2021_05_06_V301. The calculations described in this document are implemented in the 5G Wizard. Specifically, equations (4), 5(), and (8) are implemented as PD_N+, PD_Tot+ and PD_Mod+ as described in section 8.5. The average PD for each PD type is performed by rotating a square around each evaluation point on the grid, performing the average for each rotation, then selecting the maximum across all these rotations as the averaged value. This process is described in more detail in Annex D of the 63195-2 document.  

[![Power Density Example][pd_example]](https://github.com/ariensligar/5G-Wizard)


Cumulative Distribution Function (CDF):
CDF if calculated as the maximum gain across all beam ID’s defined in the codebook. 
[![CDF Example][cdf_example]](https://github.com/ariensligar/5G-Wizard)
[![CDF Envelope Example][cdf_envelope_example]](https://github.com/ariensligar/5G-Wizard)


Validation:
The calculation from the local Poynting vector to each PD type is validated using the IEEE provided reference data. These can also be validated within the 5G wizard by selecting “Run Validation.”

The result of the averaging algorithm implemented in the 5G wizard can be compared with the provided reference data by running “Run Validation” from within the wizard. The resulting validation shows less than 1% difference between validation data and the output from the 5G wizard.
[![Example of Validation Data][validation_screenshot]](https://github.com/ariensligar/5G-Wizard)

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [python](https://python.org/)
* [pyAEDT](https://github.com/pyansys/pyaedt)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Download stand-alone executable, or clone repository to run script version of the 5G wizard.

### Prerequisites

To run the 5G wizard, you must have a local licenced copy of AEDT 2021 R2.


### Installation

The 5G wizard can be run by executing the standalone 5G_Wizard.exe or by using one of the scripts (5G_Wizard_Standalone_NoGUI.py or 5G_Wizard.py)


1. Clone the repo
   ```sh
   git clone https://github.com/ariensligar/5G-Wizard.git
   ```

If you want to run the 5G wizard as a script (not using the executable), a python environment will need to be configured. See README_python_env.txt for an example of how to setup a python envionrment. If you want to built the applicaiton as an exe, see README_creating_application.txt.

   ```sh
	pip install pywin32
	pip install numpy
	pip install h5py
	pip install -U matplotlib
	pip install pyaedt==0.3.25
	pip install scipy
	pip install Jinja2
   ```

Standalone Executable with GUI:
   ```sh
	5G_Wizard.exe
   ```
Script with GUI:
   ```sh
	5G_Wizard.py
   ```
Script without GUI:
   ```sh
	5G_Wizard_Standalone_NoGUI.py
   ```

<!-- USAGE EXAMPLES -->
## Usage

Codebook:
The codebook defines the mag/phase values defined on each port per beam ID. The beamID is used for the basis of all CDF and PD calculations. For PD, every beam ID defined in the codebook will be evaluated for maximum average PD. For CDF, the envelope far field pattern, the corresponding beam ID for the max field pattern, and the CDF plot will be created using each beam ID.
The codebook should look like the following examples (saved as csv files).

Codebook Example:
   ```sh
	Beam_ID,Module_Name,Ant_Feed,Amplitude,Phase,Paired_With
	0,module1,2;4;6;8,1;1;1;1,0;0;0;0,-1
	1,module1,2;4;6;8,1;1;1;1,0;20;40;60,-1
	2,module1,2;4;6;8,1;1;1;1,0;40;80;120,-1
	3,module1,2;4;6;8,1;1;1;1,0;-20;-40;-60,-1
	4,module1,2;4;6;8,1;1;1;1,0;-40;-80;-120,-1
   ```
   
Codebook Example (including renormalization):
   ```sh
	Beam_ID,Module_Name,Ant_Feed,Amplitude,Phase,Paired_With,Prad_Renorm
	0,module1,2;4;6;8,1;1;1;1,0;0;0;0,-1,1
	1,module1,2;4;6;8,1;1;1;1,0;20;40;60,-1,1
	2,module1,2;4;6;8,1;1;1;1,0;40;80;120,-1,1
	3,module1,2;4;6;8,1;1;1;1,0;-20;-40;-60,-1,1
	4,module1,2;4;6;8,1;1;1;1,0;-40;-80;-120,-1,1
   ```
Each column of data is comma delimited. Within each column, subdivisions are defined with a semicolon, ";". In the above example, the Ant_Feed column contains "2;4;6;7" as the entries. This means ports with the name "2" "4" "6" and "8" are included in that beam ID definitions. The corresponding magnitude and phase defined in the Amplitude and Phase columns. For example, if we look at beamID=2, This beam excites port 2 with a magnitude 1 and phase 0. Port 4 is excited with a magnitude of 1 and phase 40...etc. A beamID can be paired with any other beam in the codebook. Using the Paired_With column, this will excite both beams simultaneously. If a -1 is defined for Paired_With, the beam does not have a beam pair and no other beams will be excited when the beam is selected. It is assumed that if a beam pair is used, it is reciprocal for both beams. Prad_Renorm is an optional parameter. This parameter can be used to renormalize the total radiated power to the specified value. If not defined, the total radiated power will be calculated based on the Amplitude defined for the ports. Note: if Prad_Renorm is not defined, the GUI interface will allow a renormalization to be defined. The value used in the codebook will always override any GUI settings

Power Density:
Select the PD type to be calculated, area, and surface to calculate PD over. The grid spacing on the surface will be defined as 1mm or lambda/10, whichever is smaller. Beam power can be renormalized, if a single value is used, all beams will be renormalized to this amount of radiated power. If an array of values (ie. 1,3,1,0.5). The beams corrosponding to the order they are defined in the codebook, would be renomalized to these different amount of radiated power. 

CDF: 
CDF is calculated based on user selected coordinate system. The peak (100th percentile) CDF can be renormalized to a user specified value.

Multi-Run:
If multi-run is selected as the operation mode, a single file can be loaded with multiple jobs (calculations to run). This multi-run file effectively has all the required inputs for CDF or PD within a single csv file. Each row of the file is one calculation, where each column would correspond to the inputs of the GUI. This will allow any number of calculations to be run with a single user interaction. For example, if you wanted to calculate the PD on multiple surfaces using the same codebook, the multirun file would look something like the following:

Multi-Run Example - Power Density:
   ```sh
	Job_ID,Project_Name,Design_Name,Solution_Name,Freq,Evaluation_Surface,PD_Type,Averaging_Area,Codebook_Name
	0, test_project, design1,Setup1:sweep, 28GHz, rectangle1, PD_n_plus, 1cm^2, Codebook.csv
	1, test_project, design1,Setup1:sweep, 28GHz, rectangle1, PD_n_plus, 1cm^2, Codebook.csv
   ```


With CDF, if multi-run is selected, the CDF for each individual job will be reported along with the CDF across all jobs. This total CDF will reprsent if all the jobs were included in a single simulation. For example, you may want to calculate the CDF of multiple 5G modules on a single device. But instead of running a single simulation with all the devices in them, you may run multiple simulations, where each simulation only contains a single 5G module. The total CDF will incorporate tehh sum of all the different designs in a single CDF report.

Multi-Run Example - CDF:
   ```sh
	Job_ID,Project_Name,Design_Name,Solution_Name,Freq,CS_Name,Codebook_Name
	0,5G_28GHz_AntennaModule,4x1_array2,Setup1:LastAdaptive,28GHz,Global,CodebookExample_Hpol.csv
	1,5G_28GHz_AntennaModule,4x1_array2,Setup1:LastAdaptive,28GHz,Global,CodebookExample_Vpol.csv
   ```


Results will be written to an HTML file located in your specified output directory. The results displayed in the html file are also available directly within the results folder. This includes data stored as json and hdf5 formats for easy access by users for output customization
[![Report Screenshot][report_screenshot]](https://github.com/ariensligar/5G-Wizard)


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [] Feature 1
- [] Feature 2
- [] Feature 3
    - [] Nested Feature

See the [open issues](https://github.com/ariensligar/5G-Wizard/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Arien Sligar - arien.sligar@ansys.com

Project Link: [https://github.com/ariensligar/5G-Wizard](https://github.com/ariensligar/5G-Wizard)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ariensligar/5G-Wizard.svg?style=for-the-badge
[contributors-url]: https://github.com/ariensligar/5G-Wizard/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ariensligar/5G-Wizard.svg?style=for-the-badge
[forks-url]: https://github.com/ariensligar/5G-Wizard/network/members
[stars-shield]: https://img.shields.io/github/stars/ariensligar/5G-Wizard.svg?style=for-the-badge
[stars-url]: https://github.com/ariensligar/5G-Wizard/stargazers
[issues-shield]: https://img.shields.io/github/issues/ariensligar/5G-Wizard.svg?style=for-the-badge
[issues-url]: https://github.com/ariensligar/5G-Wizard/issues
[license-shield]: https://img.shields.io/github/license/ariensligar/5G-Wizard.svg?style=for-the-badge
[license-url]: https://github.com/ariensligar/5G-Wizard/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[report_screenshot]: images/report_screenshot.png
[cdf_envelope_example]: images/cdf_envelope_example.png
[cdf_example]: images/cdf_example.png
[pd_example]: images/pd_example.png
[validation_screenshot]: images/validation_screenshot.png