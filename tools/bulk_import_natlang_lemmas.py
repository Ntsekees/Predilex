# -*- coding: utf-8 -*-
# PYTHON 3.10

# COPYRIGHT LICENSE: ISC license. See LICENSE.md in the top level directory.
# SPDX-License-Identifier: ISC

# ============================================================ #

import sys, os, time

from common import table_from_csv_path, edit_csv_from_path

SELF_PATH = os.path.dirname(os.path.realpath(__file__))

# ============================================================ #

def entrypoint():
	start_time = time.time()
	path = SELF_PATH + "/bulk_import.csv"
	do_bulk_import(table_from_csv_path(path))
	print("Execution time: {:.3f}s.".format(
		time.time() - start_time))

def do_bulk_import(data):
	if len(data) <= 1:
		print(f"⚠⚠⚠ EMPTY BULK IMPORT FILE!")
		return
	data_header, data_body = data[:1][0], data[1:]
	langs = dict()
	for e in data_body:
		lang = e[data_header.index("Language")]
		if not lang in langs:
			langs[lang] = []
		langs[lang] += [e]
		xx = [(l, len(langs[l])) for l in langs]
	for lang in langs:
		n = len(langs[lang])
		print(f"𖡨 {lang} ➤ {n}")
		def edit(lex, entries):
			nonlocal lang
			if len(lex) == 0:
				print(f"⚠⚠⚠ EMPTY LEXICON FOR LANGUAGE ⟪{lang}⟫!")
				return lex
			if len(lex) == 1 and not isinstance(lex[0], list):
				lex = [lex]
			lex_header, lex_body = lex[:1][0], lex[1:]
			for lex_e in lex_body:
				for ee in entries:
					if forall(
						["Lemma", "Supertype", "Sememe"],
						lambda key:
							(ee[data_header.index(key)] ==
								lex_e[lex_header.index(key)])
					):
						l = lex_e[lex_header.index("Lemma")]
						st = lex_e[lex_header.index("Supertype")]
						sem = lex_e[lex_header.index("Sememe")]
						print(f"⚠⚠⚠ ⟨{l}, {st}, {sem}⟩ IS ALREADY IN THE LEXICON!")
			for ee in entries:
				lemmas = (ee[data_header.index("Lemma")]
					.replace("  ", " ")
					.replace(" /", "/")
					.replace("/ ", "/")
					.split("/"))
				reformated = [""] * len(lex_header)
				lex_lemma_keys = [k for k in lex_header if "Lemma" in k]
				for key in lex_lemma_keys:
					if len(lemmas) == 0:
						break
					reformated[lex_header.index(key)] = lemmas[0]
					lemmas = lemmas[1:]
				for key in data_header:
					if not key in ("Lemma", "Language"):
						val = ee[data_header.index(key)]
						if not key in lex_header:
							if val != "":
								print(f"⚠⚠⚠ For language ⟪{lang}⟫, field ⟪{key}⟫ is missing!")
						else:
							reformated[lex_header.index(key)] = val
				lex += [reformated]
			lex_body = sorted(
				lex_body,
				key = lambda row: row[lex_header.index("Lemma")])
			return [lex_header] + lex_body
		try:
			path = SELF_PATH + f"/../natlangs/{lang}.csv"
			edit_csv_from_path(
				path,
				lambda lex: edit(lex, langs[lang]),
				output_path = path)
		except FileNotFoundError:
			try:
				path = SELF_PATH + f"/../natlangs/.suspended/{lang}.csv"
				edit_csv_from_path(
					path,
					lambda lex: edit(lex, langs[lang]),
					output_path = path)
			except FileNotFoundError:
				raise(Exception(f"⚠ ERROR: No CSV file for language ⟪{lang}⟫!"))
	return

def forall(iterable, property):
	for e in iterable:
		if not property(e):
			return False
	return True

def equals(x, y, property):
	return property(x) == property(y)

# ============================================================ #

# === ENTRY POINT === #

entrypoint()


