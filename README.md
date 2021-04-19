# ETF_tracker

[![Python application](https://github.com/shristov1/ETF_tracker/actions/workflows/Python%20application.yml/badge.svg)](https://github.com/shristov1/ETF_tracker/actions/workflows/Python%20application.yml)

A personal project that tracks ETF prices

As a lot of people (incl. myself) are overwhelmed by the amount of the investing opportunities out there, I decided to make a simple notebook which will look at the data from Investment.com and sort out the high return ETFs in the past year in which I may want to invest. 

I do live in Germany so I limit the ETFs that I can get in Germany and also the ones offered by BlackRock and Amundi - otherwise the list might get too overwhelming. 

### Packages used:
- numpy
- pandas
- matplotlib
- seaborn
- investpy

### Files in repo:
- ETF_scraping_download.ipynb - Jupyter notebook with the main portion of the work
- README.md - readme for the project

### Findings:
- plenty of ETFs that have > 30% change in the past year - but that is not representative due to Covid.
- I will move to analysing larger historical dataset to check for a longer trend.
- I understand that there are multiple variables that would have an effect on the prices of ETFs and their RoI, but I only use that to filter the names of highly yielding ETFs.

Once a more robust analysis is done I will post it on Medium.


### Acknowledgments:
- stackoverflow (of course) 
- Investment.com
- investpy
