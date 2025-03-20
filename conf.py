# Project
project = "biodigitaljazz"
copyright = "2024, Kayce Basques"
author = "Kayce Basques"
release = "0.0.0"

# Templates
templates_path = ["_templates"]

# Excludes
exclude_patterns = [
    ".github",
    ".gitignore",
    "Makefile",
    "README.md",
    "_build",
    "boostrap.sh",
    "requirements.txt",
    "venv",
    "openbsd.txt",
]

# Theme
html_static_path = ["_static"]
html_extra_path = ["rss.xml"]
html_permalinks_icon = "#"

# Extensions
extensions = ["sphinx_reredirects"]

# Redirects
redirects = {}

# Code
pygments_style = "sphinx"
