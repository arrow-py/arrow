# mypy: ignore-errors
# -- Path setup --------------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

about = {}
with open("../arrow/_version.py", encoding="utf-8") as f:
    exec(f.read(), about)

# -- Project information -----------------------------------------------------

project = "Arrow 🏹"
copyright = "2021, Chris Smith"
author = "Chris Smith"

release = about["__version__"]

# -- General configuration ---------------------------------------------------

extensions = ["sphinx.ext.autodoc", "sphinx_autodoc_typehints"]

templates_path = []

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

master_doc = "index"
source_suffix = ".rst"
pygments_style = "sphinx"

language = None

# -- Options for HTML output -------------------------------------------------

html_theme = "alabaster"
html_theme_path = []
html_static_path = []

html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True

# https://alabaster.readthedocs.io/en/latest/customization.html
html_theme_options = {
    "description": "Arrow is a sensible and human-friendly approach to dates, times and timestamps.",
    "github_user": "arrow-py",
    "github_repo": "arrow",
    "github_banner": True,
    "show_related": False,
    "show_powered_by": False,
    "github_button": True,
    "github_type": "star",
    "github_count": "true",  # must be a string
}

html_sidebars = {
    "**": ["about.html", "localtoc.html", "relations.html", "searchbox.html"]
}
