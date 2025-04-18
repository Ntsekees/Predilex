﻿# -*- coding: utf-8 -*-

import os, time, re

from common import edit_csv_from_path

SELF_PATH = os.path.dirname(os.path.realpath(__file__))

# ============================================================ #


def entrypoint():
  start_time = time.time()
  path = SELF_PATH + "/../predilex.csv"
  edit_csv_from_path(
    path, predilex_with_arities_updated, output_path = path)
  print("Execution time: {:.3f}s.".format(
    time.time() - start_time))

def predilex_with_arities_updated(predilex):
  arity_i = predilex[0].index("arity")
  eng_def_i = predilex[0].index("eng_def")
  l = len(predilex)
  i = 2
  while i < l:
    eng_def = predilex[i][eng_def_i]
    if eng_def != "":
      α = predilex[i][arity_i]
      if None != re.search(
        r"➍,? \(…\)", predilex[i][eng_def_i]
      ):
        β = "∞"
      else:
        β = str(arity_from_eng_def(eng_def))
      predilex[i][arity_i] = β
      if α != β:
        print(f"  @{i + 1}: {α if α != '' else '∅'} → {β}.")
    i = i + 1
  return predilex

def arity_from_eng_def(eng_def):
  slot_symbols = [
    "⓿", "➊", "➋", "➌", "➍", "➎", "➏", "➐", "➑", "➒", "➓"
  ]
  l = len(slot_symbols)
  i = l
  while i > 0:
    i = i - 1
    if slot_symbols[i] in eng_def:
      if i == l:
        print(f"⚠ Arity ≥{l} found for definition ⟪{eng_def}⟫!")
      return i
  return 0


# === ENTRY POINT === #

entrypoint()

