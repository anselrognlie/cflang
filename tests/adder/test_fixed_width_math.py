import cflang.cfsm.fixed_width_math as FixedWidthAdder

def test_add_with_overflow():
    n1 = 0x7f
    n2 = 0x01
    r, v = FixedWidthAdder.add(1, n1, n2)

    assert r == 0x80
    assert v is True

def test_add_wrap_no_overflow():
    n1 = 0xff
    n2 = 0x01
    r, v = FixedWidthAdder.add(1, n1, n2)

    assert r == 0x00
    assert v is False

def test_sub_with_overflow():
    n1 = 0x80
    n2 = 0x01
    r, v = FixedWidthAdder.sub(1, n1, n2)

    assert r == 0x7f
    assert v is True

def test_sub_wrap_no_overflow():
    n1 = 0x00
    n2 = 0x01
    r, v = FixedWidthAdder.sub(1, n1, n2)

    assert r == 0xff
    assert v is False

