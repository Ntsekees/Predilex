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

LANGUAGE_CODE = "toa"
DICT_ADDRESS = "./tests/test_toaq_official.json"
FORMAT = "JSON"
PREDILEX_ID_ADDRESS = "predilex_id"

# ============================================================ #

def load():
  if DICT_ADDRESS.startswith("http"):
    return common.object_from_json_url(DICT_ADDRESS)
  else:
    return common.object_from_json_path(DICT_ADDRESS)

def save(data, path):
  common.save_as_json_file(data, path)

def read(entry, key):
  if not key in entry:
    raise ValueError(f"⚠ Error: ⟪{key}⟫ is not a valid key!")
  return entry[key]

def write(entry, key, value):
  entry[key] = value
  return entry

def predilex_id_of(lexicon, id):
  return (
    lexicon[id]["predilex_id"] if "predilex_id" in lexicon[id] else "")

def lemmas_of(lexicon, id):
  return {lexicon[id]["toaq"]} if id < len(lexicon) else set()

