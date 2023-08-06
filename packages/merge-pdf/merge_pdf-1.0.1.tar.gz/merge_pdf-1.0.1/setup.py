#! python3
import os
from setuptools import setup, find_packages

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup (
	name = "merge_pdf",
	version = "1.0.1", 
	description = "Merge by name, all pdfs in the current folder, or specific list of files, into a single pdf file",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	author = "Dari Developer",
	author_email = "hernandezdarifrancisco@gmail.com",
	license = "MIT",
	keywords = "pdf, merge, merge pdf, pdf files, manage pdf",
	project_urls = {
		"Documentation": "https://github.com/DariHernandez/merge_pdf/blob/master/README.md",
		"Funding": "https://www.paypal.com/paypalme/FranciscoDari",
		"Source": "https://github.com/DariHernandez/merge_pdf"
		},
	packages = find_packages(include=["merge_pdf", "merge_pdf.*"]),
	install_requires = ["pyperclip", "PyPDF2"],
	python_requires = ">=3.7"
)
