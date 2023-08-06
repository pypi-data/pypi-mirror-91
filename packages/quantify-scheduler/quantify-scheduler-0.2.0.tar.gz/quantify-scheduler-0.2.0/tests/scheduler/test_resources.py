from quantify.scheduler.resources import ClockResource, BasebandClockResource


def test_ClockResource():
    # clock associated with qubit
    clock = ClockResource('q0:cl:01', freq=6.5e9, phase=23.9)
    assert clock.data['name'] == 'q0:cl:01'
    assert clock.data['freq'] == 6.5e9
    assert clock.data['phase'] == 23.9

    # clock 3
    clock = ClockResource('cl3', freq=4.5e9)
    assert clock.data['name'] == 'cl3'
    assert clock.data['freq'] == 4.5e9
    assert clock.data['phase'] == 0


def test_BasebandClockResource():
    # clock associated with qubit
    clock = BasebandClockResource('baseband')
    assert clock.data['name'] == 'baseband'
    assert clock.data['freq'] == 0
