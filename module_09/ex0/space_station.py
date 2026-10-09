"""Exercise 0: Space Station Data.

Basic Pydantic model creation with BaseModel and Field validation.
"""
from datetime import datetime

from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    """Validated data reported by a space station."""

    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def display_station(station: SpaceStation) -> None:
    """Print the station information in a readable format."""
    status = "Operational" if station.is_operational else "Offline"
    print("Valid station created:")
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print(f"Status: {status}")


def main() -> None:
    """Demonstrate valid and invalid space station creation."""
    separator = "=" * 40
    print("Space Station Data Validation")
    print(separator)

    # Valid station built from raw data (e.g. parsed JSON).
    # model_validate converts the ISO string into a datetime automatically.
    raw_station: dict[str, object] = {
        "station_id": "ISS001",
        "name": "International Space Station",
        "crew_size": 6,
        "power_level": 85.5,
        "oxygen_level": 92.3,
        "last_maintenance": "2024-01-15T10:30:00",
    }
    try:
        station = SpaceStation.model_validate(raw_station)
        display_station(station)
    except ValidationError as error:
        print(f"Unexpected validation error: {error}")

    print()
    print(separator)

    # Invalid station: crew_size exceeds the maximum of 20
    try:
        SpaceStation(
            station_id="BAD001",
            name="Overcrowded Station",
            crew_size=25,
            power_level=50.0,
            oxygen_level=60.0,
            last_maintenance=datetime.now(),
        )
    except ValidationError as error:
        print("Expected validation error:")
        for detail in error.errors():
            print(detail["msg"])


if __name__ == "__main__":
    main()