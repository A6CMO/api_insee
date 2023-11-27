from api_insee.request.request import RequestService


def test_format_setter_should_set_application_json_value() -> None:
    request = RequestService()
    request.format = "csv"
    request.format = "json"

    assert request.format == "json"
