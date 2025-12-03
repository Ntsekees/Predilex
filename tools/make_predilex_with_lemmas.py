# -*- coding: utf-8 -*-
# PYTHON 3.10

# COPYRIGHT LICENSE: ISC license. See LICENSE.md in the top level directory.
# SPDX-License-Identifier: ISC

# ============================================================ #

import sys, os, time, re

from common import table_from_csv_path, save_as_csv_file
from sort import predilex_sorted_from

SELF_PATH = os.path.dirname(os.path.realpath(__file__))

# ============================================================ #

NATLANG_MAP = {
	"eng": "English",
	"cmn": "Mandarin",
	"hin": "Hindi",
	"spa": "Spanish",
	"ara": "Standard Arabic",
#	"urd": "Urdu",
	"ben": "Bengali",
	"fra": "French",
	"ind": "Indonesian",
	"por": "Portuguese",
	"rus": "Russian",
	"pcm": "Nigerian Pidgin",
	"arz": "Egyptian Arabic",
	"hau": "Hausa",
	"swa": "Swahili",
	"deu": "German",
	"mar": "Marathi",
	"vie": "Vietnamese",
	"tel": "Telugu",
	"jpn": "Japanese",
#	"lah": "Lahnda",
#	"amh": "Amharic",
	"tgl": "Tagalog",
#	"tam": "Tamil",
	"tur": "Turkish",
#	"pes": "Persian",
#	"kor": "Korean",
	"eus": "Basque",
#	"lat": "Latin",
#  "grc": "Ancient Greek",
#	"san": "Sanskrit"
}

CONLANGS = ["Esperanto", "Klingon", "Lojban", "Loglan", "Nijbo", "Toaq", "New Ithkuil", "Xextan", "Eberban", "Nahaıwa"]


# ============================================================ #

def entrypoint():
	start_time = time.time()
	predilex_path = SELF_PATH + "/../predilex.csv"
	predilex_with_lemmas_path = (
		SELF_PATH + "/../predilex_with_lemmas.csv")
	predilex = table_from_csv_path(predilex_path)
	langs = []
	for code in NATLANG_MAP.keys():
		try:
			lexicon = table_from_csv_path(natlang_path_for(code))
		except:
			print(f"⚠ Natlang ⟦{code}⟧ not found!")
			lexicon = []
		langs.append({
			"code": code,
			"name": NATLANG_MAP[code],
			"lexicon": lexicon
		})
	for name in CONLANGS:
		try:
			lexicon = table_from_csv_path(conlang_path_for(name))
		except:
			print(f"⚠ Conlang ⟦{name}⟧ not found!")
			lexicon = []
		langs.append({
			"code": name.lower(),
			"name": name,
			"lexicon": lexicon
		})
	save_as_csv_file(
		proceed(predilex, langs),
		predilex_with_lemmas_path,
		eol = "\n"
	)
	print("Execution time: {:.3f}s.".format(
		time.time() - start_time))

def natlang_path_for(code):
	return SELF_PATH + "/../natlangs/" + code + ".csv"

def conlang_path_for(name):
	return SELF_PATH + "/../conlangs/" + name + ".csv"

def index_of_field(data, name):
	for n in (name.lower(), name.capitalize()):
		if n in data:
			return data.index(n)
	return None

def proceed(predilex_full, languages):
	header, predilex = predilex_full[:2], predilex_full[2:]
	pfields = header[0]
	pfields_names = header[1]
	pid_i = pfields.index("id")
	predilex = sorted(predilex, key = lambda entry: entry[pid_i])
	nlangs = len(languages)
	for i, e in enumerate(predilex):
		predilex[i] = e + [""] * nlangs
	idmap = idmap_of(predilex, pid_i)
	for lang in languages:
		lkey = lang["code"].replace(" ", "_") + "_lem"
		pfields.append(lkey)
		pfields_names.append(lang["name"] + " lemmas")
		lcol = pfields.index(lkey)
		if len(lang["lexicon"]) == 0:
			continue
		lfields = lang["lexicon"][0]
		sememe_i = index_of_field(lfields, "sememe")
		lemma_i = index_of_field(lfields, "lemma")
		discr_i = index_of_field(lfields, "discriminator")
		type_i = index_of_field(lfields, "supertype")
		traits_i = index_of_field(lfields, "features")
		if traits_i is None:
			traits_i = index_of_field(lfields, "traits")
			if traits_i is None:
				print(f"⚠ ⟦traits_i⟧ = ∅ for language ⟪{lang['code']}⟫!")
		if type_i is None:
			type_i = index_of_field(lfields, "type")
		if sememe_i is None:
			print(f"⚠ No Sememe in header for language ⟦{lang['code']}⟧!")
			continue
		for le in lang["lexicon"][1:]:
			superframing_type = ""
			sememe = le[sememe_i]
			if sememe.startswith("ruruni-"):
				i = sememe.index("-")
				sememe, superframing_type = sememe[i + 1 :], sememe[: i]
			r = re.match(r"([a-z]+)(.*)", sememe)
			if r == None or r.groups() == ():
				continue
			sid, framing = r.group(1, 2)
			start, end = idmap[sid[0]]
			target_pi = None
			def f(i):
				nonlocal target_pi
				if i >= end:
					return False
				if sid == predilex[i][pid_i]:
					target_pi = i
					return False
				return True
			traverse_while(f, init = start)
			if target_pi != None:
				d = with_replaced_chars(
					le[discr_i],
					"0123456789AVNP",
					"₀₁₂₃₄₅₆₇₈₉ₐᵥₙₚ")
				lemval = ""
				if superframing_type != "":
					lemval += "<{" + superframing_type + "} "
				lemval += le[lemma_i] + d
				if le[type_i] != "":
					lemval += " ∈" + le[type_i]
					if not traits_i is None:
						ts = le[traits_i].split(" ")
						if len(ts) > 0:
							lemval += "·".join(ts)
				if framing != "":
					lemval += " " + framing
				if "" != predilex[target_pi][lcol]:
					predilex[target_pi][lcol] += "; "
				predilex[target_pi][lcol] += lemval.strip()
	return predilex_sorted_from([pfields, pfields_names] + predilex)

def traverse_while(P, Q = lambda _: True, init = 0, step = 1):
  # Homologuous to a C-language “for” loop.
  # The index initialization and incrementation are kept in one place, away from the body of the loop.
  i = init
  while P(i) and Q(i):
    i += step

def idmap_of(predilex, i):
	m = dict()
	pc = ""
	pci = 0
	for j, e in enumerate(predilex):
		if len(e[i]) > 0:
			#if i != len(predilex) - 1:
			if e[i][0] == pc:
				continue
			c = e[i][0]
			if pc != "" and pc not in m:
				m[pc] = [pci, j]
			pc = c
			pci = j
	if pc != "" and pc not in m:
		m[pc] = [pci, len(predilex)]
	return m

def with_replaced_chars(s, srclist, dstlist):
	r = ""
	for c in s:
		for i, sc in enumerate(srclist):
			if c == sc:
				c = dstlist[i]
		r += c
	return r

# ============================================================ #

# === ENTRY POINT === #

entrypoint()
 
