#! /usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    """Common interface for all data processors of the Code Nexus."""

    def __init__(self) -> None:
        self._storage: list[tuple[int, str]] = []
        self._rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Return True if the data can be ingested by this processor."""
        raise NotImplementedError

    @abstractmethod
    def ingest(self, data: Any) -> None:
        """Process and store the given data."""
        raise NotImplementedError

    def _store(self, item: str) -> None:
        """Store one item with its processing rank."""
        self._storage.append((self._rank, item))
        self._rank += 1

    def output(self) -> tuple[int, str]:
        """Extract and remove the oldest stored item with its rank."""
        if not self._storage:
            raise IndexError("No data available in this processor")
        return self._storage.pop(0)


class NumericProcessor(DataProcessor):
    """Processor for int, float and lists of both (mixed allowed)."""

    @staticmethod
    def _is_number(value: Any) -> bool:
        return isinstance(value, (int, float)) and not isinstance(
            value, bool
        )

    def validate(self, data: Any) -> bool:
        if self._is_number(data):
            return True
        if isinstance(data, list) and len(data) > 0:
            return all(self._is_number(item) for item in data)
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                self._store(str(item))
        else:
            self._store(str(data))


class TextProcessor(DataProcessor):
    """Processor for str and lists of str."""

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list) and len(data) > 0:
            return all(isinstance(item, str) for item in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            for item in data:
                self._store(item)
        else:
            self._store(data)


class LogProcessor(DataProcessor):
    """Processor for dicts of str key-value pairs and lists of them."""

    @staticmethod
    def _is_log(value: Any) -> bool:
        return (
            isinstance(value, dict)
            and len(value) > 0
            and all(
                isinstance(key, str) and isinstance(val, str)
                for key, val in value.items()
            )
        )

    @staticmethod
    def _format(log: dict[str, str]) -> str:
        return ": ".join(log.values())

    def validate(self, data: Any) -> bool:
        if self._is_log(data):
            return True
        if isinstance(data, list) and len(data) > 0:
            return all(self._is_log(item) for item in data)
        return False

    def ingest(
        self, data: dict[str, str] | list[dict[str, str]]
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        if isinstance(data, list):
            for item in data:
                self._store(self._format(item))
        else:
            self._store(self._format(data))


def test_numeric() -> None:
    """Test the NumericProcessor class."""
    print("Testing Numeric Processor...")
    numeric: NumericProcessor = NumericProcessor()
    print(f"Trying to validate input '42': {numeric.validate(42)}")
    print(f"Trying to validate input 'Hello': {numeric.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' "
          "without prior validation:")
    try:
        numeric.ingest("foo")  # intentional mypy warning
    except ValueError as exc:
        print(f"Got exception: {exc}")
    data: list[int | float] = [1, 2, 3, 4, 5]
    print(f"Processing data: {data}")
    numeric.ingest(data)
    print("Extracting 3 values...")
    for _ in range(3):
        rank, value = numeric.output()
        print(f"Numeric value {rank}: {value}")


def test_text() -> None:
    """Test the TextProcessor class."""
    print("\nTesting Text Processor...")
    text: TextProcessor = TextProcessor()
    print(f"Trying to validate input '42': {text.validate(42)}")
    data: list[str] = ["Hello", "Nexus", "World"]
    print(f"Processing data: {data}")
    text.ingest(data)
    print("Extracting 1 value...")
    rank, value = text.output()
    print(f"Text value {rank}: {value}")


def test_log() -> None:
    """Test the LogProcessor class."""
    print("\nTesting Log Processor...")
    log: LogProcessor = LogProcessor()
    print(f"Trying to validate input 'Hello': {log.validate('Hello')}")
    data: list[dict[str, str]] = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f"Processing data: {data}")
    log.ingest(data)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = log.output()
        print(f"Log entry {rank}: {value}")


def main() -> None:
    """Run all the Code Nexus data processor tests."""
    print("=== Code Nexus - Data Processor ===\n")
    test_numeric()
    test_text()
    test_log()


if __name__ == "__main__":
    main()
