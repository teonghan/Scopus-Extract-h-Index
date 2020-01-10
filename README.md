# Scopus-Extract-h-Index
A simple web scrapping script to extract h-index, citations &amp; number of publications from Scopus Author Profile

An input file (Excel xlsx) must be prepared before hand with at least the following headers
1. Main reference ID: any reference ID; just to identify unique person in your record
2. Scopus ID: Scopus ID corresponds to the individual; multiple Scopus ID of the same person can be separated by ;[space]

# Requirements
Python 3, Pandas, Selenium

# General Notes
1. There is even more efficient way of doing this, by using Scopus API. For more detail, please visit https://dev.elsevier.com/
2. The script is not perfect. Sometimes, perhaps due to the connection to Scopus.com, things like timeout, pending javascript rendering, etc. will resulted in certain indicators to be set to zero (I took the easy route to just catch all Exception and reset them indicators to zero). It is important to go through the output after finished mining and fix these errors manually.
