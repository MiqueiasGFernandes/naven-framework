def test_package_is_importable() -> None:
    import naven

    assert naven.__package__ == "naven"
