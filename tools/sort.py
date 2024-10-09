# -*- coding: utf-8 -*-
# PYTHON 3.10

# COPYRIGHT LICENSE: ISC license. See LICENSE.md in the top level directory.
# SPDX-License-Identifier: ISC

# ============================================================ #

import sys, os, time

from common import edit_csv_from_path

SELF_PATH = os.path.dirname(os.path.realpath(__file__))

# ============================================================ #

def entrypoint():
  start_time = time.time()
  edit_csv_from_path(
    SELF_PATH + "/../predilex.csv",
    predilex_sorted_from,
    output_path = SELF_PATH + "/../predilex.csv"
  )
  print("Execution time: {:.3f}s.".format(
    time.time() - start_time))

def predilex_sorted_from(predilex):
  header, body = predilex[:2], predilex[2:]
  sorting_cols = ("tags", "subordering", "ordering")
  for c in sorting_cols:
    ci = header[0].index(c)
    body = sorted_by_col_id(body, ci)
  return header + body

def sorted_by_col_id(table, ci):
  return sorted(table, key = lambda t: (t[ci] == "", t[ci]))

# ============================================================ #

# === ENTRY POINT === #

entrypoint()

