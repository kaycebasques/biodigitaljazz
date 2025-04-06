# Project
project = "Bio-digital jazz, man"
author = "Kayce Basques"
copyright = f"2025, {author}"
release = "1.0.0"

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
html_permalinks_icon = "§"

# Extensions
extensions = ["matplotlib.sphinxext.plot_directive", "sphinx_reredirects"]

# Redirects
redirects = {
    "blog/ancestors": "https://web.archive.org/web/20250320231129/https://biodigitaljazz.net/blog/ancestors.html",
    "blog/asm": "../asm.html",
    "blog/diff2html": "https://web.archive.org/web/20250320231610/https://biodigitaljazz.net/blog/diff2html.html",
    "blog/littlebraincell": "./transistor.html",
    "blog/history": "https://web.archive.org/web/20250320235612/https://biodigitaljazz.net/blog/history.html",
    "blog/pcrowdoodle": "../pcrowdoodle.html",
    "blog/picam": "https://web.archive.org/web/20250320231430/https://biodigitaljazz.net/blog/picam.html",
    "blog/stttgts": "https://web.archive.org/web/20250320235155/https://biodigitaljazz.net/blog/stttgts.html",
    "blog/systemantics": "../systemantics.html",
    "blog/transistor": "../transistor.html",
}

# Code
pygments_style = "github-dark"

# matplotlib
plot_html_show_formats = False
