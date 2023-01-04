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

from element_from_address import element_from_address

# ============================================================ #

LANGUAGE_CODE = "toa"
DICT_ADDRESS = "./tests/test_toakao.json"
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

def _access(entry, key, f):
  return f(entry, key)

def read(entry, key):
  if "→" in key:
    return element_from_address(entry, key)
  else:
    if not key in entry:
      raise ValueError(f"⚠ Error: ⟪{key}⟫ is not a valid key!")
    return entry[key]

def write(entry, key, value):
  if key == "tags":
    value = value.split(" ")
  i = _index_of_last(lambda c: c == "→", key)
  if i != None:
    e = element_from_address(entry, key[:i])
    key = key[i + 1:].strip()
    e[key] = value
  else:
    entry[key] = value
  return entry

def predilex_id_of(lexicon, id):
  return (
    lexicon[id]["predilex_id"] if "predilex_id" in lexicon[id] else "")

def lemmas_of(lexicon, id):
  return {
    e["toaq"] for e in lexicon[id]["toaq_forms"]
  } if id < len(lexicon) else set()

def _index_of_last(ℙ, 𝕃):
  i = len(𝕃) - 1
  while i > 0:
    if ℙ(𝕃[i]):
      return i
    i -= 1
  return None

