# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import django

# Добавляем путь к Django проекту
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../hw_checker'))

# Настраиваем Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'hw_checker.settings'
django.setup()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'HW Checker'
copyright = '2025, SE-XP Team'
author = 'SE-XP Team'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',           # Автоматическая документация из docstrings
    'sphinx.ext.napoleon',          # Поддержка Google и NumPy стилей docstrings
    'sphinx.ext.viewcode',          # Добавляет ссылки на исходный код
    'sphinx.ext.intersphinx',       # Ссылки на документацию других проектов
    'sphinx.ext.todo',              # Поддержка TODO
    'sphinx_autodoc_typehints',     # Автоматическая документация типов
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Options for autodoc -----------------------------------------------------

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# -- Options for intersphinx -------------------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'django': ('https://docs.djangoproject.com/en/5.0/', 
               'https://docs.djangoproject.com/en/5.0/_objects/'),
}

# -- Options for todo --------------------------------------------------------

todo_include_todos = True

