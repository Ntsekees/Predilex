# -*- coding: utf-8 -*-
# PYTHON 3.10

# COPYRIGHT LICENSE: ISC license. See LICENSE.md in the top level directory.
# SPDX-License-Identifier: ISC

# ============================================================ #

import re

def parsed_predilex_lemmas(lemmas):
  data = []
  for s in lemmas.split(";"):
    m = {
      "is_certain": True,
      "is_approximative": False,
      "lexical_status": "official",
      "arity_mismatch": None,
      "syntactic_class": None,
      "lemma": "",
      "slot_reordering": []
    }
    j = k = 0
    for i, c in enumerate(s):
      if i < k:
        continue
      match c:
        case ' ' | '}':
          continue
        case '?':
          m["is_certain"] = False
        case '~':
          m["is_approximative"] = True
        case "*":
          m["lexical_status"] = "proposed"
        case "⁑":
          m["lexical_status"] = "unpublished"
        case "⎊":
          m["lexical_status"] = "deprecated"
        case ">":
          m["arity_mismatch"] = '>'
        case "<":
          m["arity_mismatch"] = '<'
          if i < len(s) and s[i + 1] == "{":
            k = s[i:].index("}")
            id = s[i + 2 : k]
            m["arity_mismatch"] += id
        case _:
          break
      j = max(i, min(k + 1, len(s)))
    # r = [e.strip() for e in s[j:].split(",")]
    r = s[j:].strip()
    assert len(r) > 0
    if '#' in r:
      m["lemma"], r2 = r.split('#')
      if ' ' in r2:
        m["syntactic_class"], m["slot_reordering"] = r2.split(' ')
      else:
        m["syntactic_class"] = r2
    else:
      if ' ' in r:
        m["lemma"], m["slot_reordering"] = r.split(' ')
      else:
        m["lemma"] = r
    if len(m["lemma"]) > 0 and m["lemma"][0] == "[":
      x = m["lemma"][1:]
      if "]" in x:
        x = x[x.index("]")]
      m["lemma"] = x
    data.append(m)
  return data

