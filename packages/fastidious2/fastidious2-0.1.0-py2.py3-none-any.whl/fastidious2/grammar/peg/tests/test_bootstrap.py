import textwrap as tw
from fastidious2.ast.sexpr import sexpr
from fastidious2.reader import Reader

from fastidious2.expression import (
        Literal, AnyChar, Seq, Choice, OneOrMore,
        Repeat, Optional, LookAhead, Not, CharRange,
        Action, Label, RuleSet, Rule, RuleDef, ActionFunc,
        LeftAssocInfix, RightAssocInfix, Prefix, Postfix, Slice,
        PrecedenceRule, Concat, Discard
        )

from ..bootstrap import parser


def test_identifier():
    result = parser(Reader("ident foo"), entrypoint="identifier")
    assert str(result) == "ident"


def test_rule():
    src = tw.dedent("""\
        rule <- . lab:other_rule""")
    result = parser(Reader(src), entrypoint="rule")
    assert result == RuleDef(
            "rule",
            Seq(
                AnyChar(),
                Label(
                    "lab",
                    Rule("other_rule"))))


def test_prefixes():
    src = "!."
    result = parser(Reader(src), entrypoint="expression")
    assert result == Not(AnyChar())
    src = "&."
    result = parser(Reader(src), entrypoint="expression")
    assert result == LookAhead(AnyChar())
    src = "-."
    result = parser(Reader(src), entrypoint="expression")
    assert result == Discard(AnyChar())
    src = "$."
    result = parser(Reader(src), entrypoint="expression")
    assert result == Slice(AnyChar())
    src = "$$."
    result = parser(Reader(src), entrypoint="expression")
    assert result == Concat(AnyChar())

