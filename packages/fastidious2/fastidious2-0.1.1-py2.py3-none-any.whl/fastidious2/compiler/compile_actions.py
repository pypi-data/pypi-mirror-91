from copy import copy
from functools import reduce

from fastidious2.ast.visitor import NodeVisitor, visitor
from fastidious2.expression import (
        RuleDef, Action, Rule, PrecedenceRule, Choice, Label, Breakpoint)


class ActionsVisistor(NodeVisitor):
    def __init__(self, namespace=None, **kwargs):
        super().__init__(**kwargs)
        self.ctx = None
        self.namespace = namespace if namespace is not None else {}

    @visitor(PrecedenceRule)
    def visit_precedence_rule(self, n: PrecedenceRule):
        n.compile(self.namespace)
        self.visit(n.rules[-1])
        return False

    @visitor(Breakpoint)
    def visit_breakpoint(self, n: Breakpoint):
        import ipdb
        ipdb.set_trace()

    @visitor(RuleDef)
    def visit_ruledef(self, n: RuleDef):
        self.ctx = []

    @visitor(Rule)
    def visit_rule(self, n: Rule):
        return False

    @visitor(Action)
    def visit_action(self, n: Action):
        self.visit(n.expression)
        n.compile(self.ctx, self.namespace)
        return False

    @visitor(Choice)
    def visit_choice(self, n: Choice):
        ctx = self.ctx
        branch_contexts = []
        for e in n.expressions:
            self.ctx = copy(ctx)
            self.visit(e)
            branch_contexts.append(self.ctx)

        # names that are defined in all branch should be added to the context
        final_ctx = copy(ctx)
        branch_contexts = [set(c) for c in branch_contexts]
        allnames = reduce(lambda x, y: x | y, branch_contexts)
        common_names = reduce(lambda x, y: x & y, branch_contexts, allnames)
        for n in common_names:
            if n not in final_ctx:
                final_ctx.append(n)
        self.ctx = final_ctx

    @visitor(Label)
    def visit_label(self, n: Label):
        self.ctx.append(n.name)


def compile_actions(rs, ns=None):
    v = ActionsVisistor(ns)
    v.visit(rs)
