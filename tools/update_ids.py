# -*- coding: utf-8 -*-

from common import edit_csv_from_path
import re

def entrypoint():
  edit_csv_from_path(
    "./predilex.csv", predilex_with_ids_updated, output_path = "./predilex-out.csv")

def predilex_with_ids_updated(predilex):
  tcns = ["homoeventives", "similar", "antonyms", "hypernyms", "hyponyms", "holonyms", "meronyms", "related", "alt", "definition"]
    # ^ Target column names
  tcs = [predilex[0].index(n) for n in tcns]
  l = len(predilex)
  i = 2  # Skipping the two header lines of Predilex
  while i < l:
    for tc in tcs:
      predilex[i][tc] = updated_id_list(predilex[i][tc], predilex)
    i += 1
  return predilex

def updated_id_list(id_list :str, predilex):
  assert(isinstance(id_list, str))
  if id_list == "":
    return ""
  # print(f"❖ id_list = {id_list}")
  #s = re.split(",? +", id_list)
  s = re.split("([a-zšŋ’]+)", id_list)
  l = len(s)
  i = 1
  while i < l:
    s[i] = updated_id(s[i], predilex)
    i += 2
  # l = ", ".join([updated_id(old_id, predilex) for old_id in s])
  # print(f"❖ >>>>>>>>> {l}")
  return "".join(s)

def updated_id(old_id, predilex):
  if old_id == "":
    return ""
  l = len(predilex)
  i = 2  # Skipping the two header lines of Predilex
  id_col     = predilex[0].index("id")
  old_id_col = predilex[0].index("old_id")
  for row in predilex:
    if old_id == row[old_id_col]:
      # print(f"• {old_id} → {row[id_col]}")
      return row[id_col]
  print(f"* Old ID \"{old_id}\" not found!")
  return old_id
  # return "▓▓▓"


# === ENTRY POINT === #

entrypoint()

