# Simpy Paper Printer

Ever since I did my masters degree, I've been working on and maturing code to make it easy to create pdf's of homework and my own writing.  My HomeworkHelper has matured into several routines that automates the process of print equations out in a pretty way and making PDF's (or other formats) with sources.  

All in all, there isn't much to this library.  There is a routine that prints out SciPy equations, does some cleanup on the terms in an equation, and makes pdf's or other formats of documents (with sources).  This is one of those cases where it's more about having (hopefully) easy-to-read code showing how to do these operations.

To make a basic environment to use this library (including the demo I've included):

'conda create --name SciPyPaperPrinterEnv python=3.9
conda activate SciPyPaperPrinterEnv
conda install sympy numpy pandas scipy matplotlib jupyter pytest p2j pandoc '

Note that converting Jupyter notebooks may requires LaTeX of some sort to be installed (on Windows, I'm using MiKTeX).

Also note that I used ealier iterations of this code in homework.  If you are working in an environment where students old homework might be used in an automated plagiarizing-check environment, I recommend checking with your environments policy on using code like this, as well as citing the use of this library to avoid potential violations.
