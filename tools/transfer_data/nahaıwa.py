# -*- coding: utf-8 -*-
# PYTHON 3.10

# ============================================================ #

import importlib.util

def import_from_path(name, path):
  spec = importlib.util.spec_from_file_location(name, path)
  mod = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(mod)
  return mod

# ============================================================ #

import sys, os
assert sys.version_info >= (3, 10)

SELF_PATH = os.path.dirname(os.path.realpath(__file__))
common = import_from_path("common", SELF_PATH + "/../common.py")

# ============================================================ #

LANGUAGE_CODE = "qnh"
DICT_ADDRESS = "nahaıwa.tsv"
#DICT_ADDRESS = "https://raw.githubusercontent.com/Ntsekees/Nahaiwa/main/roots.tsv"
FORMAT = "TSV"
PREDILEX_ID_ADDRESS = "predilex_id"

# ============================================================ #

dictionary_header = None

def load():
  global dictionary_header
  if DICT_ADDRESS.startswith("http"):
    d = common.table_from_csv_url(
      DICT_ADDRESS, delimiter = '\t')
  else:
    d = common.table_from_csv_path(
      SELF_PATH + '/' + DICT_ADDRESS, delimiter = '\t')
  dictionary_header = d[0]
  return d[1:]

def save(data, path):
  global dictionary_header
  common.save_as_csv_file(
    [dictionary_header] + data, path, delimiter = '\t')

def read(entry, key):
  global dictionary_header
  if isinstance(key, str):
    key = dictionary_header.index(key)
  if key >= len(entry):
    raise ValueError(f"⚠ Error: index ⟪{key}⟫ is out of range!")
  return entry[key]

def write(entry, key, value):
  global dictionary_header
  if isinstance(key, str):
    key = dictionary_header.index(key)
  entry[key] = value
  return entry

def predilex_id_of(lexicon, id):
  return lexicon[id][0]

def lemmas_of(lexicon, id):
  return {_normalized_id(id)} if id in lexicon else set()

def _normalized_id(id):
  if not isinstance(id, str):
    return id
  assert len(id) != 0
  if id[0] in "aeiou":
    return id.replace(" ", "")
  else:
    return id

