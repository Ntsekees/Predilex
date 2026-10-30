# -*- coding: utf-8 -*-
# PYTHON 3.10

# COPYRIGHT LICENSE: ISC license. See LICENSE.md in the top level directory.
# SPDX-License-Identifier: ISC

# ============================================================ #

import sys, os, time

from common import table_from_csv_path

SELF_PATH = os.path.dirname(os.path.realpath(__file__))

# ============================================================ #

def entrypoint():
	start_time = time.time()
	path = SELF_PATH + "/../predilex_with_lemmas.csv"
	proceed(table_from_csv_path(path))
	print("Execution time: {:.3f}s.".format(
		time.time() - start_time))

def proceed(predilex):
	header, body = predilex[:2], predilex[2:]
	field_stats = {k : 0 for k in header[0]}
	for e in body:
		for k in header[0]:
			if e[header[0].index(k)] != "":
				field_stats[k] += 1
	for k in field_stats:
		if k != "":
			print(f"  {k} ↦ {field_stats[k]}")
	return

# ============================================================ #

# === ENTRY POINT === #

entrypoint()
 
