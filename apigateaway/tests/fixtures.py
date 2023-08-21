from typing import Any
from unittest.mock import AsyncMock, MagicMock

from pytest import fixture


class Nothing:
    pass


class MockFixture:
    def __init__(self, prefix: str):
        self.prefix = prefix

    def __call__(self, name: str, return_value: Any = Nothing, async_: bool = False):
        def mocking(clsself, mocker):
            if async_:
                mock = mocker.patch(
                    f"{self.prefix}.{name}",
                    new_callable=AsyncMock if async_ else MagicMock,
                )
            else:
                mock = mocker.patch(f"{self.prefix}.{name}")
            if return_value is not Nothing:
                if callable(return_value):
                    mock.return_value = return_value(self, clsself, mocker)
                else:
                    mock.return_value = return_value
                mock.return_value = return_value
            return mock

        return fixture(mocking)
