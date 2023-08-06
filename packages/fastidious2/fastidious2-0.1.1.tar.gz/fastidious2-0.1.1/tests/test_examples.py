def test_calculator():
    import sys
    sys.path.append(".")
    from examples.calculator import run
    assert run("3+2") == 5

