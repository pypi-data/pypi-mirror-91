# -*- coding: utf-8 -*-
import ast
import sys
# from .utils import skipif_known_failing

from nbsafety.analysis.live_refs import compute_live_dead_symbol_refs


def _remove_callpoints(symbols):
    return set(sym for sym in symbols if isinstance(sym, str))


def test_simple():
    live, dead = compute_live_dead_symbol_refs("""
x = 5
print(foo, x)""")
    live, dead = _remove_callpoints(live), _remove_callpoints(dead)
    assert live == {'foo', 'print'}
    assert dead == {'x'}


def test_function_body():
    fbody = ast.parse("""
def func():
    y = 42
    print(foo, bar, baz, x)
    x = 5
""").body[0].body
    live, dead = compute_live_dead_symbol_refs(fbody)
    live, dead = _remove_callpoints(live), _remove_callpoints(dead)
    assert live == {'foo', 'bar', 'baz', 'x', 'print'}
    assert dead == {'x', 'y'}


if sys.version_info >= (3, 8):
    def test_walrus():
        live, dead = compute_live_dead_symbol_refs("""
if (y := (x := x + 1) + 1) > 0:
    z = y + 1
""")
        assert live == {'x'}
        assert dead == {'y', 'z'}
