# -- Path setup --------------------------------------------------------------

# If your modules aren’t on sys.path already, you can add them here:
# import os
# import sys
# sys.path.insert(0, os.path.abspath('..'))

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "mkdocstrings",
    # any other Sphinx extensions…
]

# -- Project information -----------------------------------------------------

project   = "PID Tuner CLI"
author    = "bMagSquatch"
release   = "0.1.0"

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = "alabaster"  # or your preferred theme
html_static_path = ["_static"]
