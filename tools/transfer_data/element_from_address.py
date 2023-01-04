# -*- coding: utf-8 -*-
# PYTHON 3.10

# COPYRIGHT LICENSE: ISC license. See LICENSE.md in the top level directory.
# SPDX-License-Identifier: ISC

_DIGITS = "0123456789↊↋"

def element_from_address(data, addr):
  addr = addr.replace(" ", "")
  path = addr.split("→")
  def find_match(data, condition):
    addr, val = condition.split("=")
    for i, e in enumerate(data):
      if element_from_address(e, addr) == val:
        return e
    return None
  for step in path:
    if data == None:
      break
    assert(step != "")
    if step[0] == "#":
      if step[1] == "@":
        data = find_match(data, step[2:])
      elif step[1] in _DIGITS:
        i = _DIGITS.index(step[1])
        assert isinstance(data, (list, tuple))
        data = data[i]
      else:
        raise Exception("Invalid #-expression.")
    elif step[0] == "@":
      data = find_match(data, step[1:])
    elif step[0] == "⊞":
      assert isinstance(data, (list, tuple))
      assert isinstance(data[0], (list, tuple))
      data = data[data[0].index(step[1:])]
    else:
      assert isinstance(data, dict)
      data = data[step]
  return data
  
