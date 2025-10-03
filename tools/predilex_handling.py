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
      "syntactic_class": "",
      "lemma": "",
      "slot_reordering": ""
    }
    j = 0
    k = -1
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
          j = max(i, min(k + 1, len(s)))
          break
    # r = [e.strip() for e in s[j:].split(",")]
    r = s[j:].strip()
    if len(r) <= 0:
      continue
      # raise Exception(f"Invalid lemma data: ⟪{s}⟫")
    PU1 = "\u0091"
    r = re.sub("\\[([^]]*) +([^]]*)\\]", f"\\1{PU1}\\2", r)
    if '#' in r:
      try:
        m["lemma"], r2 = r.split('#')
      except:
        raise Exception(f"⚠ Invalid lemma syntax: ⟪{s}⟫")
      if ' ' in r2:
        try:
          m["syntactic_class"], m["slot_reordering"] = r2.split(' ')
        except:
          raise Exception(f"⚠ Invalid lemma syntax: ⟪{s}⟫")
      else:
        m["syntactic_class"] = r2
    else:
      if ' ' in r:
        try:
          m["lemma"], m["slot_reordering"] = r.split(' ')
        except:
          raise Exception(f"⚠ Invalid lemma syntax: ⟪{s}⟫")
      else:
        m["lemma"] = r
    if len(m["lemma"]) > 0 and m["lemma"][0] == "[":
      x = m["lemma"][1:]
      if "]" in x:
        x = x[x.index("]")]
      m["lemma"] = x
    m["lemma"] = m["lemma"].replace(PU1, " ")
    data.append(m)
  return data

