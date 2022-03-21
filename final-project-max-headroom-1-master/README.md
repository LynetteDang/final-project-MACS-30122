## Description

Team Name: Max Headroom 1

Team Members: Kaya Borlase, Lynette Dang, Isabella Duan, Joseph Helbing

Class Section: Section 2

GitHub Repository Link: https://github.com/cs-ssa-w22/final-project-max-headroom-1

Project Goal: To investigate the faculty hiring practices of the University of
Chicago and to analyze the educational background of current faculty at
University of Chicago, and to explore networks in careers in academia

## Package Dependencies

We use Python 3.10. The following python packages are required for program execution:

1.  bokeh 2.4.2
2.  bs4 0.0.1
3.  copy (built-in)
4.  csv (built-in)
5.  graph-tools 1.5
6.  json (built-in)
7.  matplotlib 3.5.0
8.  pandas 1.3.5
9.  plotly 5.6.0
10. queue (built-in)
11. regex 2021.11.2
12. requests 2.27.1
13. seaborn 0.11.2

To install any packages above, run `pip install <package name>` in terminal

## Project Organization

Below is an explanation of the purpose of each folder contained in this repository:

Main Directory:

- `Project_Execution.ipynb`: Python Notebook file explaining the steps that our code takes to run at each task
- `Max Headroom - MACS 30122 Final Project Progress Report.pdf`: Project Report from Week 6 with goals, tasks (divided up), and timeline
- `Max Headroom Final Presentation`: Presentation for class Week 9

Sub-directories:

- `Code`: This folder contains any code files for the different tasks in our project, including scraping, cleaning, and analysis. To see how to run these, see: "Project_Execution.ipynb"
- `visuals`: This folder contains all data visualizations

Subdirectories within Code directory:

- `helpers`: This folder contains all util/helper functions that we call from our code files
- `data`: This folder contains any data files we gathered or created during our process, including json, txt and csv files

## Executing program

### NOTE: all of our code, with detailed steps and results, can be found in the file "Project_Execution.ipynb"

### Crawling

`faculty_crawl.py` builds a crawler to visit and pull out links where faculty data can be found.

To run the web crawler, go to the `Code` directory and enter the following command:

```
python faculty_crawl.go(num_pages_to_crawl, index_filename, starting_url, limiting_domain)
```

### Scraping

`find_universities.py` crawls each of the gathered links to pull out faculty education data if it is on either the individual page or the directory page, and update the education values in the dictionary with raw text gathered from these pages. Note the main function takes in the following arguments:

1. faculty_data (dictionary): a dictionary mapping of faculty data, with at least name, Linked Page, Directory Page, and University as keys
2. filename (str): String filename where the output dictionary should be stored (without .json -- the code adds this to the end of the filename for you)

To scrape the information, go to the `Code` directory and enter the following command:

```
python find_universities.find_universities(faculty_data, filename)
```

### Cleaning and Basic Analysis

`find_universities.py` clean scraped educational data if the education was in a list form on the website, easily accessible.

`SSD_analysis.py` takes the data from `find_universities.py`, cleans education data if the education data is found within a paragraph, and triggers the generation of data visualization for the faculty from the Social Science Division;
`Harris_analysis.py` takes the data from `find_universities.py`, cleans education data if the education data is found within a paragraph and triggers the generation of data visualization for the faculty from the Harris School of Public Policy

To clean scraped educational data and generate the graphic analysis, go to the `Code` directory and enter the following command:

```
python SSD_analysis.py
```

```
python Harris_analysis.py
```

### Network and Regression Analysis

## text: to be filled out##

To prepare for network analysis, go to the `Code` directory and enter the following command:

```
python gender_race_network.py
```
