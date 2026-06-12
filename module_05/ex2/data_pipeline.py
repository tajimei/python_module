#! /usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any, Protocol


class DataProcessor(ABC):
    """Common interface for all data processors of the Code Nexus."""

    def __init__(self, name: str) -> None:
        self._name: str = name
        self._storage: list[tuple[int, str]] = []
        self._rank: int = 0

    @property
    def name(self) -> str:
        """Display name of the processor."""
        return self._name

    @property
    def total(self) -> int:
        """Total number of items ingested since creation."""
        return self._rank

    @property
    def remaining(self) -> int:
        """Number of items still stored, waiting to be output."""
        return len(self._storage)

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

    def __init__(self) -> None:
        super().__init__("Numeric Processor")

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

    def __init__(self) -> None:
        super().__init__("Text Processor")

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

    def __init__(self) -> None:
        super().__init__("Log Processor")

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


class ExportPlugin(Protocol):
    """Structural contract for export plugins (duck typing)."""

    def process_output(self, data: list[tuple[int, str]]) -> None:
        """Export a list of (rank, value) tuples."""
        ...


class CSVExportPlugin:
    """Export data as a manually built CSV line."""

    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        print(",".join(value for _, value in data))


class JSONExportPlugin:
    """Export data as a manually built JSON object string."""

    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("JSON Output:")
        pairs: str = ", ".join(
            f'"item_{rank}": "{value}"' for rank, value in data
        )
        print("{" + pairs + "}")


class DataStream:
    """Route stream elements to registered processors polymorphically
    and export processed data through pluggable export plugins."""

    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        """Register a new data processor on the stream."""
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        """Send each element of the stream to the first processor
        able to handle it. Print an error if none can."""
        for element in stream:
            for proc in self._processors:
                if proc.validate(element):
                    proc.ingest(element)
                    break
            else:
                print("DataStream error - "
                      f"Can't process element in stream: {element}")

    def print_processors_stats(self) -> None:
        """Print statistics for every registered processor."""
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            print(f"{proc.name}: total {proc.total} items processed, "
                  f"remaining {proc.remaining} on processor")

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        """Consume up to nb elements from each registered processor
        and export them using the provided plugin."""
        for proc in self._processors:
            batch: list[tuple[int, str]] = []
            try:
                for _ in range(min(nb, proc.remaining)):
                    batch.append(proc.output())
            except IndexError:
                pass
            if batch:
                plugin.process_output(batch)


def main() -> None:
    """Demonstrate the complete Code Nexus data pipeline."""
    print("=== Code Nexus - Data Pipeline ===\n")

    print("Initialize Data Stream...\n")
    stream: DataStream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Processors")
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())

    first_batch: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {"log_level": "WARNING",
             "log_message": "Telnet access! Use ssh instead"},
            {"log_level": "INFO",
             "log_message": "User wil is connected"},
        ],
        42,
        ["Hi", "five"],
    ]
    print(f"\nSend first batch of data on stream: {first_batch}\n")
    stream.process_stream(first_batch)
    stream.print_processors_stats()

    print("\nSend 3 processed data from each processor "
          "to a CSV plugin:")
    csv_plugin: CSVExportPlugin = CSVExportPlugin()
    stream.output_pipeline(3, csv_plugin)
    print()
    stream.print_processors_stats()

    second_batch: list[Any] = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR",
             "log_message": "500 server crash"},
            {"log_level": "NOTICE",
             "log_message": "Certificate expires in 10 days"},
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]
    print(f"\nSend another batch of data: {second_batch}\n")
    stream.process_stream(second_batch)
    stream.print_processors_stats()

    print("\nSend 5 processed data from each processor "
          "to a JSON plugin:")
    json_plugin: JSONExportPlugin = JSONExportPlugin()
    stream.output_pipeline(5, json_plugin)
    print()
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
