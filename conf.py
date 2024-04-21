project = 'biodigitaljazz'
copyright = '2024, Kayce Basques'
author = 'Kayce Basques'
release = '0.0.0'

extensions = []
templates_path = ['_templates']
exclude_patterns = [
    '.github',
    '.gitignore',
    'Makefile',
    'README.md',
    '_build',
    'boostrap.sh',
    'requirements.txt',
    'venv',
    'openbsd.txt'
]
pygments_style = 'sphinx'

html_static_path = ['_static']
html_extra_path = [
    'rss.xml'
]
html_permalinks_icon = '#'
