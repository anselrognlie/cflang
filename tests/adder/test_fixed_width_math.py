import cflang.cfsm.fixed_width_math as FixedWidthAdder

def test_add_with_overflow():
    n1 = 0x7f
    n2 = 0x01
    r, flags = FixedWidthAdder.add(1, n1, n2)

    assert r == 0x80
    assert flags.overflow is True
    assert flags.zero is False
    assert flags.carry is False
    assert flags.negative is True

def test_add_wrap_no_overflow():
    n1 = 0xff
    n2 = 0x01
    r, flags = FixedWidthAdder.add(1, n1, n2)

    assert r == 0x00
    assert flags.overflow is False
    assert flags.zero is True
    assert flags.carry is True
    assert flags.negative is False

def test_sub_with_overflow():
    n1 = 0x80
    n2 = 0x01
    r, flags = FixedWidthAdder.sub(1, n1, n2)

    assert r == 0x7f
    assert flags.overflow is True
    assert flags.zero is False
    assert flags.carry is False
    assert flags.negative is False

def test_sub_wrap_no_overflow():
    n1 = 0x00
    n2 = 0x01
    r, flags = FixedWidthAdder.sub(1, n1, n2)

    assert r == 0xff
    assert flags.overflow is False
    assert flags.zero is False
    assert flags.carry is True
    assert flags.negative is True

