# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Path setup --------------------------------------------------------------
# If your project is not in the root directory, add the project's path.
# Adjust '../' to the path of the folder containing your Python module.
sys.path.insert(0, os.path.abspath('.'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Lab 3 Tkinter'
copyright = '2024, Fadi Fleihan'
author = 'Fadi Fleihan'
release = '22'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc', 
    'sphinx.ext.viewcode',      # Automatically document your Python code
    'sphinx.ext.napoleon',      # Support for Google style docstrings
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Options for Autodoc -----------------------------------------------------
# This will allow autodoc to automatically document your code.

autodoc_default_options = {
    'members': True,            # Document all functions/methods in modules
    'undoc-members': True,      # Document functions/methods without docstrings
    'private-members': False,   # Only document public methods, set to True to include private
}
