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
redirects = {
    "blog/ancestors": "https://web.archive.org/web/20250320231129/https://biodigitaljazz.net/blog/ancestors.html",
    "blog/picam": "https://web.archive.org/web/20250320231430/https://biodigitaljazz.net/blog/picam.html",
    "blog/diff2html": "https://web.archive.org/web/20250320231610/https://biodigitaljazz.net/blog/diff2html.html",
    "blog/littlebraincell": "./transistor.html",
}

# Code
pygments_style = "sphinx"
