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
	path = SELF_PATH + "/../predilex.csv"
	edit_csv_from_path(
		path, predilex_sorted_from, output_path = path)
	print("Execution time: {:.3f}s.".format(
		time.time() - start_time))

def predilex_sorted_from(predilex):
	header, body = predilex[:2], predilex[2:]
	for col in ("eng_def", "tags"):
		body = sorted_by_col_id(body, header[0].index(col))
	body = sorted(
		body,
		key = lambda row: tag_rank_of_row(row, header[0].index("tags")))
	return header + body

def sorted_by_col_id(table, cid):
	return sorted(table, key = lambda t: (t[cid] == "", t[cid]))

def tag_rank_of_row(row, tags_col_id):
	tags = row[tags_col_id]
	l = tags.split(" ")
	first = "" if l == [] else l[0]
	if first in HIERARCHY:
		return HIERARCHY.index(first)
	else:
		return len(HIERARCHY)

HIERARCHY_S = "constant, basic, mereology, context_handling, worlds, logic, mathematics, cardinality, ordinality, prop_cardinality, shape, spacetime, time, space, causality, philosophy, perception, has_color, mind, emotion, psychology, sociology, cognition, evidentiality, deixis, aspect, directional_part, position, spatiotemporal_position, temporal_position, spatial_position, physics, physical_property, action, involuntary_action, action, body_part, biology, substance, material, artifact, chemical_element, culture, cultural, amount, astronomy, food, beverage, change, chemistry, computer_language, computer_science, currency, duplicate, dwelling, ethny, game, geographic_entity, geographic_feature, geology, has_illness, illness, joke, kinship, landscape, language, linguistics, measure_unit, medical_condition, modality, natural_feature, natural_phenomenon, medicine, profession, programming_language, pseudo-absolute, quaternary_predicate, religion, room, science, season, semiotics, supernatural, syntax, taxonomy, weather, texture, thematic_role, toaq_copy, ⚠"
HIERARCHY = HIERARCHY_S.split(", ")

# ============================================================ #

# === ENTRY POINT === #

entrypoint()

