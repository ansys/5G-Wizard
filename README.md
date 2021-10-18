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
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ariensligar/5G-Wizard">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
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

[![Product Name Screen Shot][product-screenshot]](https://example.com)

The Ansys 5G Wizard can be used to calculate Power Density or Cumulative Distribution Function. These calculations use a codebook to define the mag/phase value on ports for each beam ID. The codebook definition will be imported into your HFSS design, where you can now control the mag/phase on all ports  by simply changing the post processing variable “BeamID.”

Power Density (PD): 
The PD is calculated based on IEC_IEEE_63195-2_2021_05_06_V301. The calculations described in this document are implemented in the 5G Wizard. Specifically, equations (4), 5(), and (8) are implemented as PD_N+, PD_Tot+ and PD_Mod+ as described in section 8.5. The calculation from the local Poynting vector to each PD type is validated using the IEEE provided reference data. These can also be validated within the 5G wizard by selecting “Run Validation.” The average PD for each PD type is performed by rotating a square around each evaluation point on the grid, performing the average for each rotation, then selecting the maximum across all these rotations as the averaged value. This process is described in more detail in Annex D of the 63195-2 document. The result of the averaging algorithm implemented in the 5G wizard can be compared with the provided reference data by running “Run Validation” from within the wizard. The resulting validation shows less than 1% difference between validation data and the output from the 5G wizard. 

Cumulative Distribution Function (CDF):
CDF if calculated as the maximum gain across all beam ID’s defined in the codebook. 

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Next.js](https://nextjs.org/)
* [React.js](https://reactjs.org/)
* [Vue.js](https://vuejs.org/)
* [Angular](https://angular.io/)
* [Svelte](https://svelte.dev/)
* [Laravel](https://laravel.com)
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

The 5G wizard can be run by executing the standalone 5G_Wizard.exe or by using one of the scripts (5G_Wizard_Standalone_NoGUI.py or 5G_Wizard.py)


1. Clone the repo
   ```sh
   git clone https://github.com/ariensligar/5G-Wizard.git
   ```

If you want to run the 5G wizard as a script (not using the executable), a python environment will need to be configured. See README_python_env.txt for an example of how to setup a python envionrment. If you want to built the applicaiton as an exe, see README_creating_application.txt.



<!-- USAGE EXAMPLES -->
## Usage

Power Density:
Select the PD type to be calculated, area, and surface to calculate PD over. The grid spacing on the surface will be defined as 1mm or lambda/10, whichever is smaller. Beam power can be renormalized, if a single value is used, all beams will be renormalized to this amount of radiated power. If an array of values (ie. 1,3,1,0.5). The beams corrosponding to the order they are defined in the codebook, would be renomalized to these different amount of radiated power. 

CDF: 
CDF is calculated based on user selected coordinate system. The peak (100th percentile) CDF can be renormalized to a user specified value.

Multi-Run:
If multi-run is selected as the operation mode, a single file can be loaded with multiple jobs (calculations to run). This multi-run file effectively has all the required inputs for CDF or PD within a single csv file. Each row of the file is one calculation, where each column would correspond to the inputs of the GUI. This will allow any number of calculations to be run with a single user interaction. For example, if you wanted to calculate the PD on multiple surfaces using the same codebook, the multirun file would look something like the following:
Job_ID,Project_Name,Design_Name,Solution_Name,Freq,Evaluation_Surface,PD_Type,Averaging_Area,Codebook_Name
0, test_project, design1,Setup1:sweep, 28GHz, rectangle1, PD_n_plus, 1cm^2, Codebook.csv
1, test_project, design1,Setup1:sweep, 28GHz, rectangle1, PD_n_plus, 1cm^2, Codebook.csv

With CDF, if multi-run is selected, the CDF for each individual job will be reported along with the CDF across all jobs. This total CDF will reprsent if all the jobs were included in a single simulation. For example, you may want to calculate the CDF of multiple 5G modules on a single device. But instead of running a single simulation with all the devices in them, you may run multiple simulations, where each simulation only contains a single 5G module. The total CDF will incorporate tehh sum of all the different designs in a single CDF report.

Results will be written to an HTML file located in your specified output directory. The results displayed in the html file are also availble directly within the results folder. This includes data stored as json and hdf5 formats for easy access by users for output customization

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

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

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