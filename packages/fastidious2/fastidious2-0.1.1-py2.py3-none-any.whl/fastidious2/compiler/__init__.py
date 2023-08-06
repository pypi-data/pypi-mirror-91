from .compile_actions import compile_actions


def compile_peg(r, actions=True, ns=None):
    if actions:
        compile_actions(r, ns=ns)
