# -*- coding: utf-8 -*-

# Remove duplicate Toaq keywords

from common import edit_csv_from_path

def entrypoint():
  edit_csv_from_path("../predilex.csv", with_duplicates_removed)

def with_duplicates_removed(table):
  defx = table[0].index("eng def")
  toax = table[0].index("toa keywords")
  defs = set()
  l = len(table)
  y = 0
  while y < l:
    is_duplicate = False
    for dy, dd in defs:
      if table[y][defx] == dd:
        is_duplicate = True
        if table[dy][toax] != "":
          table[dy][toax] += ", "
        table[dy][toax] += table[y][toax]
        table[y][defx] = "∎"
        break
    if not is_duplicate:
      defs.add((y, table[y][defx]))
    y += 1
  return table

entrypoint()

