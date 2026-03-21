import hesperides.api as hapi


def test_health_check():

    result = hapi.health_check()

    assert result == "ok"