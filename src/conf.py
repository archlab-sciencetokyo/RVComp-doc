# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'RVComp Guide'
copyright = '2025, Yuki Yagi'
author = 'Yuki Yagi'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser", "sphinx.ext.githubpages"]

# MyST Parser configuration
myst_enable_extensions = [
    "colon_fence",      # Enable ::: code blocks
    "deflist",          # Definition lists
    "tasklist",         # Task lists [ ] [x]
]

# Ensure code blocks with language specifiers are properly rendered
myst_fence_as_directive = []

# Syntax highlighting
highlight_language = 'bash'
pygments_style = 'default'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_baseurl = 'https://archlab-sciencetokyo.github.io/RVComp-doc/'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_title = "top"

root_doc = 'index'

def setup(app):
    app.add_css_file('base.css')