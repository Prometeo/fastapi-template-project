<a id="readme-top"></a>


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->



<!-- PROJECT LOGO -->
<br />
<div align="center">
<h3 align="center">FastAPI Project structure generator</h3>

  <p align="center">
    Create fastapi projects from template
    <br />
    <a href="https://github.com/Prometeo/fastapi-template-project"><strong>Explore the docs »</strong></a>
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
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
Template for generating Fastapi projects

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* Python
* FastAPI
* Docker
* Docker Compose
* loguru
* uv

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Prerequisites

Install copier
* Pip
  ```sh
  pip install copier --user
  ```
* uv
  ```sh
  uv tool install install copier
  ```

### Usage

2. Generate project
   ```sh
   copier copy https://github.com/Prometeo/fastapi-template-project {project-path}
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] Cache Configuration
- [ ] Queue Integration

<p align="right">(<a href="#readme-top">back to top</a>)</p>
