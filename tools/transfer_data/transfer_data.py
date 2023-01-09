# -*- coding: utf-8 -*-
# PYTHON 3.10

# COPYRIGHT LICENSE: ISC license. See LICENSE.md in the top level directory.
# SPDX-License-Identifier: ISC

"""
  PURPOSE:
    Transfer data between Predilex and a Loglang Lexicon (henceforth “LL”).
    The direction of the transfer (to or from Predilex) is indicated as part of the input.
 
  INPUT:
    FILES:
      • ⟦transfer_data_input⟧ JSON
        JSON representing a map containing the following keys:
          • ⟦path⟧ Text
            Filesystem path to a Python module serving as the interface between this program and the LL of arbitrary format, defining functions for loading, saving, reading and writing the LL data.
          • ⟦shall_be_from_predilex⟧ Boolean
            Indication of whether the data is to be transfered FROM Predilex (as opposed as TO it) to the LL.
          • ⟦shall_be_by_keywords⟧ Boolean
            Indication of whether the target entries are identified by language keywords, as opposed of by Predilex ID stored in the LL data.
          • ⟦map⟧ Map
            Map of data field names from the transfer source to the target data field names of the transfer destination (which of Predilex and the LL is the destination or the source is chosen with the ⟦shall_be_from_predilex⟧ switch, mentioned above).
            For example, a map of the form ⟪{"tags": "predilex_tags"}⟫, combined with ⟦shall_be_from_predilex⟧ being True, will trigger transfer of the content of the ⟦tags⟧ column of Predilex to data fields named ⟪predilex_tags⟫ in the LL data.
    
    The ⟦transfer_data_input⟧ file is the only input taken by this program. Standard Arguments and STDIN are ignored.
  
  OUTPUT:
    STDOUT:
      • Duration of execution, along with possible warnings or error messages.
    
    FILES:
      • ⟦transfer_data_output⟧ Any
        Modified version of the transfer destination (either Predilex or the LL), with the selected data field having been imported. The format is the same as that of the original LL file.
  
  USAGE EXAMPLES:
    ⎈ python3 transfer_data.py
"""

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
predilex_handling = import_from_path(
  "predilex_handling", SELF_PATH + "/../predilex_handling.py")

import json, re, time
from typing import Any, Callable
from dataclasses import dataclass

# ============================================================ #


TEST_PREDILEX_PATH = "tests/test_predilex.csv"
PREDILEX_PATH = "../../predilex.csv"

PREDILEX_ADDRESS = PREDILEX_PATH
PREDILEX_MAXLEN = 4500

# ============================================================ #

def entrypoint():
  start_time = time.time()
  idata = common.object_from_json_path(
    SELF_PATH + "/transfer_data_input")
  assert all([k in idata for k in (
    "path", "map", "shall_be_from_predilex",
    "shall_be_by_keywords"
  )])
  shall_be_from_predilex = idata["shall_be_from_predilex"]
  shall_be_by_keywords = idata["shall_be_by_keywords"]
  map = idata["map"]
  module = import_from_path(
    "module", SELF_PATH + "/" + idata["path"])
  assert all([hasattr(module, varname) for varname in (
    'LANGUAGE_CODE', 'FORMAT'
  )])
  predilex = from_csv_address(
    SELF_PATH + "/" + PREDILEX_ADDRESS)
  def f(s):
    if s not in predilex[0]:
      raise Exception(f"⚠ ⟪{s}⟫ is not a Predilex column identifier!")
    return predilex[0].index(s)
  if shall_be_from_predilex:
    map = {f(v): k for v, k in map.items()}
  else:
    map = {v: f(k) for v, k in map.items()}
  if shall_be_by_keywords:
    lcci = predilex[0].index(module.LANGUAGE_CODE + "_kw")
    # ↑ ⟪lcci⟫: “Language Code Column Index”
  else:
    lcci = None
  lexicon = module.load()
  proceed(
    predilex[2:PREDILEX_MAXLEN], lexicon, module,
    map, shall_be_from_predilex, lcci)
  out_path = SELF_PATH + "/transfer_data_output"
  if shall_be_from_predilex:
    module.save(lexicon, out_path)
  else:
    save_as_csv_file(predilex, out_path)
  print("Execution time: {:.3f}s.".format(
    time.time() - start_time))

@dataclass
class Item:
  idx: int
  data: Any  # list or dict
  read: Callable
  write: Callable
  
def proceed(
  predilex, lexicon, module, map, shall_be_from_predilex, lcci
):
  src, dst = reversed_if_not(
    shall_be_from_predilex, (
      Item(None, predilex, read_predilex, write_predilex),
      Item(None, lexicon, module.read, module.write)
    )
  )
  predilex_is_outer = isinstance(lcci, int)
  src_is_outer = (predilex_is_outer == shall_be_from_predilex)
  outer, inner = reversed_if_not(
    predilex_is_outer, (predilex, lexicon)
  )
  outer_iter = indexes_of(outer)
  inner_iter = indexes_of(inner)
  for i in outer_iter:
    if (
      (predilex_is_outer and "" != predilex[i][lcci]) or (
        not predilex_is_outer and "" != module.predilex_id_of(
          lexicon, i)
      )
    ):
      for j in inner_iter:
        src.idx, dst.idx = reversed_if_not(src_is_outer, (i, j))
        pi, li = reversed_if_not(predilex_is_outer, (i, j))
        if predilex_is_outer:
          p_lemmas = lexemes_from_predilex_keywords(
            predilex[pi][lcci])
          l_lemmas = module.lemmas_of(lexicon, li)
          if p_lemmas == l_lemmas:
            move_data(src, dst, map)
            predilex_id = predilex[pi][0]
            lexicon_id = module.predilex_id_of(lexicon, li)
            if lexicon_id not in ("", predilex_id):
              print(f"⚠ PREDILEX ID MISMATCH: Predilex ⟪{predilex_id}⟫ ≠ Lexicon ⟪{lexicon_id}⟫!")
          elif p_lemmas.intersection(l_lemmas) != set():
            print(f"◈ ⚠ PARTIAL INTERSECTION BETWEEN THE FOLLOWING LEMMA SETS:")
            print(f"  • From Predilex: {str(p_lemmas)}")
            print(f"  • From Lexicon:  {str(l_lemmas)}")
        else:
          if predilex[pi][0] == module.predilex_id_of(
            lexicon, li
          ):
            move_data(src, dst, map)

# ============================================================ #

def read_predilex(entry, key):
  if key >= len(entry):
    raise ValueError(f"⚠ Error: ⟪{key}⟫ is not a valid key!")
  return entry[key]

def write_predilex(entry, key, value):
  entry[key] = value
  return entry

def indexes_of(d):
  if isinstance(d, (list, tuple)):
    return range(0, len(d))
  elif isinstance(d, dict):
    return d
  else:
    raise TypeError(f"⚠ Unsupported dictionary type: {type(d)}")
    return None

def move_data(src, dst, map):
  for k in map:
    if k == "":
      v = src.idx
    else:
      v = src.read(src.data[src.idx], k)
    dst.data[dst.idx] = dst.write(
      dst.data[dst.idx], map[k], v)

def reversed_if_not(prop, α):
  return α if prop else reversed(α)

def lexemes_from_predilex_keywords(pkwl):
  α = predilex_handling.parsed_predilex_keywords(pkwl)
  return {β["keyword"] for β in α}

def index_of_first(ℙ, 𝕃):
  l = len(𝕃)
  i = 0
  while i < l:
    if ℙ(𝕃[i]):
      return i
    i += 1
  return None


# ============================================================ #

def from_yaml_address(address):
  if address.startswith("http"):
    return common.object_from_yaml_url(address)
  else:
    return common.object_from_yaml_path(address)

def from_csv_address(address):
  if address.startswith("http"):
    return common.table_from_csv_url(address)
  else:
    return common.table_from_csv_path(address)

# ============================================================ #

# === ENTRY POINT === #

entrypoint()

