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

HIERARCHY_S = "constant, contextual_constant, basic, mereology, context_handling, worlds, modality, thematic_role, logic, mathematics, cardinality, ordinality, prop_cardinality, language, linguistics, syntax, deixis, aspect, spacetime, time, space, shape, room, directional_part, position, spatiotemporal_position, temporal_position, spatial_position, causality, physics, measure_unit, amount, physical_property, texture, change, chemical_element, substance, material, chemistry, science, semiotics, philosophy, evidentiality, perception, has_color, mind, cognition, emotion, psychology, sociology, culture, cultural, artifact, involuntary_action, action, body_part, biology, kinship, has_illness, illness, medical_condition, medicine, food, beverage, dwelling, ethny, game, computer_language, computer_science, currency, geographic_entity, geographic_feature, landscape, geology, natural_feature, natural_phenomenon, weather, season, astronomy, joke, profession, religion, supernatural, taxonomy, quaternary_predicate, duplicate, ⚠"
HIERARCHY = HIERARCHY_S.split(", ")

# ============================================================ #

# === ENTRY POINT === #

entrypoint()

