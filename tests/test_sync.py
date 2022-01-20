from Link.sync import Sync


def test_logarithm():
    sync = Sync(120, (4, 4))
    pattern = sync.pattern(0.486)
    assert pattern != 0
