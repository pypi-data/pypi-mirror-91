import textwrap as tw

from fastidious2.reader import Reader
from fastidious2.expression import (
        Literal, AnyChar, Seq, Choice, OneOrMore,
        Repeat, Optional, LookAhead, Not, CharRange,
        Action, Label, RuleSet, Rule, RuleDef, ActionFunc,
        LeftAssocInfix, RightAssocInfix, Prefix, Postfix, Slice,
        PrecedenceRule, Concat, Discard
        )
from fastidious2.compiler import compile_peg


parser = RuleSet(
    # grammar <- __ rules:( rule __ )+ { RuleSet(rules) }
    RuleDef(
        "grammar",
        Action(
            Seq(
                Rule("__"),
                Label(
                    "rules",
                    OneOrMore(
                        Seq(
                            Rule("rule"),
                            Rule("__"))))),
            "RuleSet(rules)")),
    # rule <- name:identifier __ "<-" __ expr:expression EOS
    RuleDef(
        "rule",
        Action(
            Seq(
                Label(
                    "name",
                    Rule("identifier")),
                Rule("__"),
                Literal("<-"),
                Rule("__"),
                Label(
                    "expr",
                    Rule("expression")),
                Rule("EOS")),
            "RuleDef(str(name), expr)")),
    # expression <- choice_expr
    RuleDef(
        "expression",
        Rule("choice_expr")),
    # choice_expr <- first:seq_expr rest:( __ "/" __ seq_expr )* {
    #     if not rest:
    #         return first
    #     else:
    #         return Choice([first] + rest)
    RuleDef(
        "choice_expr",
        Action(
            Seq(
                Label(
                    "first",
                    Rule("seq_expr")),
                Label(
                    "rest",
                    Repeat(
                        Seq(
                            Rule("__"),
                            Literal("/"),
                            Rule("__"),
                            Rule("seq_expr"))))),
            tw.dedent("""\
                if not rest:
                    return first
                else:
                    return Choice([first] + rest)"""))),
    # seq_expr <-
    #     first:labeled_expr
    #     rest:( __ labeled_expr )*
    #     action:code_block? {
    #         if not rest:
    #             expr = first
    #         else:
    #             expr = Seq([first] + rest)
    #         if action:
    #             return Action(expr, action)
    #         else:
    #             return expr}
    RuleDef(
        "seq_expr",
        Action(
            Seq(
                Label(
                    "first",
                    Rule("labeled_expr")),
                Label(
                    "rest",
                    Repeat(
                        Seq(
                            Discard(Rule("__")),
                            Rule("labeled_expr")))),
                Label(
                    "action",
                    Optional(
                        Rule("code_block")))),
            tw.dedent("""\
                if not rest:
                    expr = first
                else:
                    parts = [first] + [r[0] for r in rest]
                    expr = Seq(*parts)
                if action:
                    return Action(expr, action)
                else:
                    return expr"""))),
    # code_block <- "{" code:code "}" { code }
    RuleDef(
        "code_block",
        Action(
            Seq(
                Literal("{"),
                Label(
                    "code",
                    Rule("code"))),
            "code")),
    # code <-
    #     code:$(
    #         (
    #           ( ![{}] source_char )+
    #           / "{" code "}"
    #         )*
    #     ) {str(code).strip()}
    RuleDef(
        "code",
        Action(
            Label(
                "code",
                Slice(
                    Repeat(
                        Choice(
                            OneOrMore(
                                Seq(
                                    Not(
                                        CharRange("{}")),
                                    AnyChar())),
                            Seq(
                                Literal("{"),
                                Rule("code"),
                                Literal("}")))))),
            "str(code).strip()")),
    # labeled_expr <-
    #     label:$$(identifier -__ -':' -__)? expr:prefixed_expr {
    #         if label:
    #             return Label(label, expr)
    #         else:
    #             return expr}
    RuleDef(
        "labeled_expr",
        Action(
            Seq(
                Label(
                    "label",
                    Optional(
                        Concat(
                            Seq(
                                Rule("identifier"),
                                Discard(Rule("__")),
                                Discard(Literal(":")),
                                Discard(Rule("__")))))),
                Label(
                    "expr",
                    Rule("prefixed_expr"))),
            tw.dedent("""\
                if label:
                    return Label(str(label), expr)
                else:
                    return expr"""))),
    # prefixed_expr <- prefixes:( $$(prefix -__) )* expr:suffixed_expr {
    #     prefix_classes = {
    #         "-": Discard,
    #         "!": Not,
    #         "&": LookAhead,
    #         "$": Slice,
    #         "$$": Concat,
    #     }
    #     for p in reversed(prefixes):
    #         expr = prefix_classes[str(p)](expr)}
    RuleDef(
        "prefixed_expr",
        Action(
            Seq(
                Label(
                    "prefixes",
                    Repeat(
                        Concat(
                            Seq(
                                Rule("prefix"),
                                Discard(
                                    Rule("__")))))),
                Label(
                    "expr",
                    Rule("suffixed_expr"))),
            tw.dedent("""\
                prefix_classes = {
                    "-": Discard,
                    "!": Not,
                    "&": LookAhead,
                    "$": Slice,
                    "$$": Concat,
                }
                for p in reversed(prefixes):
                    expr = prefix_classes[str(p)](expr)
                expr"""))),
    # suffixed_expr <- expr:primary_expr suffix:( __ suffix )?
    RuleDef(
        "suffixed_expr",
        Action(
            Seq(
                Label(
                    "expr",
                    Rule("primary_expr")),
                Label(
                    "suffix",
                    Optional(
                        Seq(
                            Rule("__"),
                            Rule("suffix"))))),
            tw.dedent("""\
                if not suffix:
                    return expr
                suffix_classes = {
                    "?": Optional,
                    "+": OneOrMore,
                    "*": Repeat,
                }
                return suffix_classes[str(suffix)](expr)"""))),
    # suffix <- [?+*]
    RuleDef(
        "suffix",
        CharRange("?+*")),
    # prefix <- "$$" / [-$!&]
    RuleDef(
        "prefix",
        Choice(
            Literal("$$"),
            CharRange("-$!&"))),
    # primary_expr <-
    #     lit_expr
    #     / char_range_expr
    #     / any_char_expr
    #     / rule_expr
    #     / SemanticPredExpr
    #     / sub_expr
    RuleDef(
        "primary_expr",
        Choice(
            Rule("any_char_expr"),
            Rule("rule_expr"),
            Rule("sub_expr")
            )),
    # sub_expr <- "(" __ expr:expression __ ")" { expr }
    RuleDef(
        "sub_expr",
        Action(
            Seq(
                Literal("("),
                Rule("__"),
                Label(
                    "expr",
                    Rule("expression")),
                Rule("__")),
            "expr")),
    # lit_expr <- lit:string_literal ignore:"i"?
    # string_literal <-
    #     '"' content:double_string_char* '"'
    #     / "'" single_string_char* "'"
    # double_string_char <-
    #     !( '"' / "\\" / EOL ) source_char
    #     / "\\" double_string_escape
    # single_string_char <-
    #     !( "'" / "\\" / EOL ) char:source_char
    #     / "\\" char:single_string_escape
    # single_string_escape <- char:"'" / char:common_escape
    # double_string_escape <- char:'"' / char:common_escape
    # common_escape <-
    #    single_char_escape
    #    / OctalEscape
    #    / HexEscape
    #    / LongUnicodeEscape
    #    / ShortUnicodeEscape
    # single_char_escape <- 'a' / 'b' / 'n' / 'f' / 'r' / 't' / 'v' / '\\'
    # any_char_expr <- "." { AnyChar() }
    RuleDef(
        "any_char_expr",
        Action(
            Literal("."),
            "AnyChar()")),
    # rule_expr <- name:identifier !( __ "<-" ) { Rule(str(name)) }
    RuleDef(
        "rule_expr",
        Action(
            Seq(
                Label(
                    "name",
                    Rule("identifier")),
                Not(
                    Seq(
                        Rule("__"),
                        Literal("<-")))),
            "Rule(str(name))")),
    # char_range_expr <-
    #    '[' content:(
    #        class_char_range
    #        / class_char
    #        / "\\" UnicodeClassEscape )*
    #     ']' ignore:'i'?
    # class_char_range <- class_char '-' class_char
    # class_char <-
    #     !( "]" / "\\" / EOL ) char:source_char
    #     / "\\" char:char_class_escape
    # char_class_escape <- ']' / common_escape
    # comment <- "#" ( !EOL source_char )*
    RuleDef(
        "comment",
        Seq(
            Literal("#"),
            Repeat(
                Seq(
                    Not(Rule("EOL")),
                    AnyChar())))),
    # source_char <- .
    # identifier <- $([a-zA-Z_] [a-zA-Z0-9_]*)
    RuleDef(
        "identifier",
        Slice(
            Seq(
                CharRange("_", (["a", "z"], ["A", "Z"])),
                Repeat(
                    CharRange("_", (["a", "z"], ["A", "Z"], ["0", "9"])))))),
    # __ <- ( whitespace / EOL / comment )*
    RuleDef(
        "__",
        Repeat(
            Choice(
                Rule("whitespace"),
                Rule("EOL"),
                Rule("comment")))),
    # _ <- whitespace*
    RuleDef(
        "_",
        Repeat(
            Rule("whitespace"))),
    # whitespace <- [ \t\r]
    RuleDef(
        "whitespace",
        CharRange(" \t\r")),
    # EOL <- "\n"
    RuleDef(
        "EOL",
        Literal("\n")),
    # EOS <- _ comment? EOL / __ EOF
    RuleDef(
        "EOS",
        Choice(
            Seq(
                Rule("_"),
                Optional(
                    Rule("comment")),
                Rule("EOL")),
            Seq(
                Rule("__"),
                Rule("EOF")))),
    # EOF <- !.
    RuleDef(
        "EOF",
        Not(AnyChar()))
)

ns = globals()

compile_peg(parser, ns=ns)
