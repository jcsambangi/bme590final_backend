from pin_lookup import pin


def test_pin():
    assert pin(261122326) == 435
    assert pin(261791206) == 9307
