#!/usr/bin/env python

"""Tests for `fastidious2` package."""
import pytest

from fastidious2.expression import (
        AnyChar, RuleSet, RuleDef, Expr, NoMatch, Literal, Action, Label,
        Choice, Seq, Discard, Slice, Concat
)
from fastidious2.reader import Reader
from fastidious2.compiler import compile_peg


class _Parser:
    def __init__(self, *rules: Expr, ns=None):
        _rules = []
        for i, r in enumerate(rules):
            if not isinstance(r, RuleDef):
                r = RuleDef(f"rule_{i}", r)
            _rules.append(r)

        self.p = RuleSet(*_rules)
        compile_peg(self.p, ns=ns)

    def __call__(self, src: str):
        self.reader = Reader(src)
        return self.p(self.reader)


def test_nomatch():
    r = Reader("abc")
    e = Literal("d")
    n = NoMatch(e, 0, r)
    assert str(n) == '"d" doesn\'t match at 0'


def test_any_char():
    # rule <- .
    expr = AnyChar()
    assert expr.as_grammar() == "."

    p = _Parser(expr)
    assert str(p("ab")) == "a"

    with pytest.raises(NoMatch) as exc:
        str(p(""))
    assert exc.value.pos == 0


def test_literal():
    # rule <- "a"
    expr = Literal("a")
    assert expr.as_grammar() == '"a"'

    p = _Parser(expr)
    assert str(p("ab")) == "a"

    with pytest.raises(NoMatch) as exc:
        str(p("b"))
    assert exc.value.pos == 0


def test_seq():
    expr = Seq(Literal("a"), Literal("b"), Literal("c"))
    assert expr.as_grammar() == '"a" "b" "c"'

    p = _Parser(expr)
    assert [str(i) for i in p("abc")] == ["a", "b", "c"]

    with pytest.raises(NoMatch) as exc:
        str(p("b"))
    assert exc.value.pos == 0


def test_discard():
    expr = Seq(Literal("a"), Discard(Literal("b")), Literal("c"))
    assert expr.as_grammar() == '"a" -"b" "c"'

    p = _Parser(expr)
    assert [str(i) for i in p("abc")] == ["a", "c"]


def test_slice():
    expr = Slice(Seq(Literal("a"), Literal("b"), Literal("c")))
    assert expr.as_grammar() == '$( "a" "b" "c" )'

    p = _Parser(expr)
    assert str(p("abc")) == "abc"


def test_concat():
    expr = Concat(Seq(Literal("a"), Discard(Literal("b")), Literal("c")))
    assert expr.as_grammar() == '$$( "a" -"b" "c" )'

    p = _Parser(expr)
    assert str(p("abc")) == "ac"


def test_actions():
    # rule <- a:. { f"foo_{a}" }
    expr = Action(Label("a", AnyChar()), 'f"foo_{a}"')
    assert expr.as_grammar() == 'a:. { f"foo_{a}" }'
    p = _Parser(expr)

    assert str(p("c")) == "foo_c"

    # rule <- b:. { f"foo_{a}" }
    p = _Parser(Action(Label("b", AnyChar()), 'f"foo_{a}"'))

    with pytest.raises(NameError) as exc:
        str(p("c"))
    assert exc.value.args[0] == "name 'a' is not defined"

    # rule <- a:"c" {f"foo_{a}"}/ b:"a" {f"bar_{b}"}
    p = _Parser(
            Choice(
                Action(
                    Label(
                        "a",
                        Literal("c")),
                    'f"foo_{a}"'),
                Action(
                    Label(
                        "b",
                        Literal("a")),
                    'f"bar_{b}"')))
    assert str(p("cba")) == "foo_c"
    assert str(p("abc")) == "bar_a"

    # rule <- out:.
    #         result:(
    #           a:"c" {f"foo_{out}_{a}"}
    #           / b:"a" {f"bar_{out}_{b}"}
    #         )
    #         {result}
    p = _Parser(
            Action(
                Seq(
                    Label(
                        "out",
                        AnyChar()),
                    Label(
                        "result",
                        Choice(
                            Action(
                                Label(
                                    "a",
                                    Literal("c")),
                                'f"foo_{out}_{a}"'),
                            Action(
                                Label(
                                    "b",
                                    Literal("a")),
                                'f"bar_{out}_{b}"')))),
                "result"))
    assert str(p("ecba")) == "foo_e_c"
    assert str(p("eabc")) == "bar_e_a"

    # Iff a label is defined in **all** branches of a choice expression,
    # it becomes available for outer actions

    # rule <- out:.(
    #           a:"c"
    #         / a:"a")
    #         {f"got {out} {a}"}
    p = _Parser(
            Action(
                Seq(
                    Label(
                        "out",
                        AnyChar()),
                    Choice(
                        Label(
                            "a",
                            Literal("c")),
                        Label(
                            "a",
                            Literal("a")))),
                'f"got {out} {a}"'))
    assert str(p("ecba")) == "got e c"
    assert str(p("eabc")) == "got e a"

    # rule <- out:.(
    #           a:"c"
    #         / "a")
    #         {f"got {out} {a}"}
    p = _Parser(
            Action(
                Seq(
                    Label(
                        "out",
                        AnyChar()),
                    Choice(
                        Label(
                            "a",
                            Literal("c")),
                        Literal("a"))),
                'f"got {out} {a}"'))
    with pytest.raises(TypeError) as exc:
        str(p("ecba"))
    assert (exc.value.args[0]
            == "__call__() got an unexpected keyword argument 'a'")


def test_actions_with_namespace():
    # rule <- a:. { math.sqrt(int(str(a))) }
    expr = Action(Label("a", AnyChar()), 'math.sqrt(int(str(a)))')

    import math
    p = _Parser(expr, ns={"math": math})

    assert p("4") == 2.0

    p = _Parser(expr)

    with pytest.raises(NameError) as exc:
        p("4")
    assert exc.value.args[0] == "name 'math' is not defined"
