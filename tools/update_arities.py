# -*- coding: utf-8 -*-

from common import edit_csv_from_path

def entrypoint():
  edit_csv_from_path(
    "./predilex.csv", predilex_with_arities_updated, output_path = "./predilex-out.csv")

def predilex_with_arities_updated(predilex):
  arity_i = predilex[0].index("arity")
  eng_def_i = predilex[0].index("eng_def")
  l = len(predilex)
  i = 2
  while i < l:
    eng_def = predilex[i][eng_def_i]
    if eng_def != "":
      α = predilex[i][arity_i]
      β = str(arity_from_eng_def(eng_def))
      predilex[i][arity_i] = β
      if α != β:
        print(f"  @{i+1}: {α} → {β}.")
    i = i + 1
  return predilex

def arity_from_eng_def(eng_def):
  # Caveat: if the arity is actually above 6, this function will return 6 nevertheless.
  slot_symbols = ["⓿", "➊", "➋", "➌", "➍", "➎", "➏"]
  i = len(slot_symbols)
  while i > 0:
    i = i - 1
    if slot_symbols[i] in eng_def:
      return i
  return 0

entrypoint()

