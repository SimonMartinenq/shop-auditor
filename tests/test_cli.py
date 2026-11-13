import pytest

from shop_auditor.cli import main


def test_unknown_command_fails() -> None:
    with pytest.raises(SystemExit):
        main(["nope"])
