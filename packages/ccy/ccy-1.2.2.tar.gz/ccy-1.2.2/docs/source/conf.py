# -*- coding: utf-8 -*-
#
import os
import sys
from datetime import date

os.environ["BUILDING-PULSAR-DOCS"] = "yes"
p = lambda x: os.path.split(x)[0]
source_dir = p(os.path.abspath(__file__))
ext_dir = os.path.join(source_dir, "_ext")
docs_dir = p(source_dir)
base_dir = p(docs_dir)
# sys.path.append(os.path.join(source_dir, "_ext"))
sys.path.insert(0, base_dir)
sys.path.insert(0, ext_dir)
import ccy

version = ccy.__version__
release = version
year = date.today().year

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath('.'))

# -- General configuration -----------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.pngmath",
    "sphinx.ext.viewcode",
    "table",
]

# Beta version is published in github pages
if ccy.VERSION[3] == "beta":
    extensions.append("sphinxtogithub")
html_context = {"release_version": ccy.VERSION[3] == "final"}
# The suffix of source filenames.
source_suffix = ".rst"

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "ccy"
copyright = "2009-%s, %s" % (year, ccy.__author__)

html_theme = "pulsar"
pygments_style = "sphinx"
templates_path = ["_templates"]
html_static_path = ["_static"]
html_theme_path = ["_theme"]
exclude_trees = ["_build"]
html_sidebars = {
    "index": [
        "sidebarlogo.html",
        "sidebarintro.html",
        "sourcelink.html",
        "searchbox.html",
    ],
    "**": [
        "sidebarlogo.html",
        "localtoc.html",
        "relations.html",
        "sourcelink.html",
        "searchbox.html",
    ],
}
exclude_trees = []

# -- Options for HTML output ---------------------------------------------------


# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = 'favicon.ico'

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Output file base name for HTML help builder.
# htmlhelp_basename = 'pulsardoc'


# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letter' or 'a4').
# latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
# latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
# latex_documents = [
#  ('index', 'pulsar.tex', 'pulsar Documentation',
#   'Luca Sbardella', 'manual'),
# ]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Additional stuff for the LaTeX preamble.
# latex_preamble = ''

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
# man_pages = [
#    ('index', 'pulsar', 'pulsar Documentation',
#     ['Luca Sbardella'], 1)
# ]
