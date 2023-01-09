# -*- coding: utf-8 -*-
# PYTHON 3.10

# COPYRIGHT LICENSE: ISC license. See LICENSE.md in the top level directory.
# SPDX-License-Identifier: ISC

# ============================================================ #

import re

def parsed_predilex_keywords(keywords):
  data = []
  for s in keywords.split(";"):
    m = {
      "is_certain": True,
      "is_approximative": False,
      "lexical_status": "official",
      "arity_mismatch": None,
      "syntactic_class": None,
      "keyword": "",
      "slots": []
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
    r = [e.strip() for e in s[j:].split(",")]
    assert len(r) > 0
    if ':' in r[0]:
      m["syntactic_class"], m["keyword"] = r[0].split(':')
    else:
      m["keyword"] = r[0]
    m["slots"] = r[1:]
    data.append(m)
  return data

