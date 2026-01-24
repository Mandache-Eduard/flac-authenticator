<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Mandache-Eduard/flac-authenticator">
    <img src="Images/flac_authenticator_project_picture.jpg" alt="Logo" width="450" height="450">
  </a>

<h3 align="center">FLAC Authenticator</h3>

___

  <p align="center">
    A small tool that analyzes FLAC audio files to determine whether they are true lossless sources or upscaled from lower-quality formats.
    <br />
    <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/github_username/repo_name"><strong>View Demo (To be added)</a>
    &middot;
    <a href="https://github.com/github_username/repo_name/issues/new?labels=bug&template=bug-report---.md"><strong>Report Bug</a>
    &middot;
    <a href="https://github.com/github_username/repo_name/issues/new?labels=enhancement&template=feature-request---.md"><strong>Request Feature</a>
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

This is a program that scans FLAC audio files to determine whether they are genuinely lossless or upscaled from lower-quality sources. It's my first project written in [![Python][Python-shield]][Python-url] and serves as a hands-on way to explore concepts related to data analysis and data engineering. Built as a personal hobby project, it is intended to remain free and open-source, and to provide a simple, transparent alternative to existing tools that are either paid or limited in functionality

___

<!-- DISCLAIMER -->
## Disclaimer

This project is currently in **an early, experimental stage** and should be considered a prototype rather than a definitive verification tool. Determining whether a FLAC file is truly lossless is inherently complex and depends on multiple factors, such as spectral analysis, encoding characteristics, frequency cutoffs, metadata consistency, checksums (e.g. MD5), and knowledge of the original source and production chain. This tool, in its current stage, only covers a subset of these aspects and **does not guarantee** correct results in all cases; in particular, it currently focuses more on analyzing audio quality characteristics than on conclusively establishing the true origin of a file. As a result, it may produce **false positives (upscaled files identified as genuine)** or **false negatives (genuine files flagged as upscaled)**. Users are **strongly encouraged** to manually review and double-check files reported with low confidence — using additional tools and their own judgment.

___

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

___

<!-- INSTALLATION -->
### Installation

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```
5. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin github_username/repo_name
   git remote -v # confirm the changes
   ```
___

<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

___

<!-- ROADMAP -->
## Roadmap

### Future features
- [ ] Create a UI for ease of use
    - [ ] Rewrite program for multithreading (1 thread for UI, 1 thread for file processing)

### Features in development
- [ ] Implement FFmpeg spectrogram creation for low-confidence files
- [ ] Implement a loading bar to visualize progress

### Completed features
- [X] Save results in a log file (.CSV)
- [X] Scan a folder structure recursively
- [X] Scan multiple files in one run


See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

___

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

___

<!-- LICENSE -->
## License

Distributed under the GNU General Public License v3.0. See `LICENSE` or click the link below for more information.
<br>
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

___

<!-- CONTACT -->
## Contact

Mandache Eduard
<br>
[![LinkedIn][LinkedIn-shield]][LinkedIn-url]
<br>
![Outlook](https://img.shields.io/badge/Email-Outlook-0078D4?logo=microsoft-outlook&logoColor=white)
<br>
Project Link: [https://github.com/Mandache-Eduard/flac-authenticator](https://github.com/Mandache-Eduard/flac-authenticator)

___

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Best README Template](https://github.com/othneildrew/Best-README-Template)
* [Choose an Open Source License](https://choosealicense.com)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[LinkedIn-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[LinkedIn-url]: https://linkedin.com/in/linkedin_username](https://www.linkedin.com/in/eduard-mandache-89588035b/
[Python-shield]: https://img.shields.io/badge/Python-3.13-blue
[Python-url]: https://www.python.org/

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
