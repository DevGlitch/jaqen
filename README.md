# Blackbeard - Team Jaqen

![Python version](https://img.shields.io/badge/python-v3.7-blue)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub contributors](https://img.shields.io/github/contributors/DevGlitch/jaqen)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

Team Members:
   * Nicolas Morant aka DevGlitch
   * Huayu (Jack) Tsu aka codejacktsu


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/DevGlitch/jaqen">
    <img src="images/blackbeard_logo.png" alt="Blackbeard logo" height="300">
  </a>
</p>


<!-- DESCRIPTION OF THE PROJECT -->
## Description
Team Jaqen wanted to build Blackbeard, a world class blackjack AI, that trains your ability to play blackjack 
from a wearable device in real time. The challenges Blackbeard is facing are as follow: object detection, 
object classification, mathematical probabilities, hand motion recognition, and more.

Disclaimer: The device is intended for academic use or training purposes only. Card counting is not illegal under Federal, State, or Local law. 


<!-- PROJECT REPORT-->
## Project Report
https://github.com/DevGlitch/jaqen/tree/master/project_report/


<!-- PROJECT PRESENTATION & DEMO-->
## Project Presentation & Demo
https://youtu.be/R2JZ_oEcPRQ


<!-- GETTING STARTED -->
## Getting Started

Follow the below instructions in order to run Blackbeard on your machine.

  
### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/DevGlitch/jaqen.git
   ```
2. Install any missing packages. 
   + We recommend using a conda environment with Python 3.7.
   + Install all the missing packages on your machine 
   + On the Raspeberry Pi:
        - Setting up a RTSP feed is needed
            + We used v42lrtspserver with h624
            + Make sure to adjust the settings of the v42lrtspserver
        - Put the mqtt_client.py file on your Pi

### Running

1. Launch on the Raspberry Pi:

```sh
   v42lrtspserver
   ```

```sh
   python 3 mqtt_client.py
   ```

2. Start Blackbeard on your Desktop:

```sh
   python __main_.py
   ```


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

Nicolas Morant - [Personal Website](https://www.nicolasmorant.com/)
 & [Github](https://github.com/DevGlitch)

Huayu (Jack) Tsu - [Github](https://github.com/codejacktsu)


<br>

Project Link: [https://github.com/DevGlitch/jaqen](https://github.com/DevGlitch/jaqen)
