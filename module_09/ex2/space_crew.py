"""Exercise 2: Space Crew Management.

Nested Pydantic models: a SpaceMission holds a list of CrewMember.
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    """Crew ranks, from lowest to highest."""

    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    """A single crew member."""

    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    """A mission with its crew; each crew entry is a nested CrewMember."""

    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    # On a list, min_length / max_length limit the number of items
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def check_safety_rules(self) -> "SpaceMission":
        """Check mission-wide safety rules.

        Runs only after every CrewMember has been validated, so each
        item in self.crew is already a CrewMember object.
        """
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        leaders = (Rank.COMMANDER, Rank.CAPTAIN)
        if not any(member.rank in leaders for member in self.crew):
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        if self.duration_days > 365:
            experienced = sum(
                1 for member in self.crew if member.years_experience >= 5
            )
            # Integer form of "experienced / total >= 50%"
            if experienced * 2 < len(self.crew):
                raise ValueError(
                    "Long missions (> 365 days) need at least 50% "
                    "experienced crew (5+ years)"
                )

        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        return self


def display_mission(mission: SpaceMission) -> None:
    """Print mission details and the crew list."""
    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(f"- {member.name} ({member.rank.value}) - "
              f"{member.specialization}")


def print_errors(error: ValidationError) -> None:
    """Print only the human-readable part of each validation error."""
    for detail in error.errors():
        print(detail["msg"].removeprefix("Value error, "))


def main() -> None:
    """Demonstrate a valid mission and an invalid one."""
    separator = "=" * 41
    print("Space Mission Crew Validation")
    print(separator)

    # Crew entries are plain dicts; Pydantic turns each into a CrewMember
    valid_mission: dict[str, object] = {
        "mission_id": "M2024_MARS",
        "mission_name": "Mars Colony Establishment",
        "destination": "Mars",
        "launch_date": "2024-06-01T09:00:00",
        "duration_days": 900,
        "budget_millions": 2500.0,
        "crew": [
            {"member_id": "CM001", "name": "Sarah Connor",
             "rank": "commander", "age": 45,
             "specialization": "Mission Command", "years_experience": 20},
            {"member_id": "CM002", "name": "John Smith",
             "rank": "lieutenant", "age": 35,
             "specialization": "Navigation", "years_experience": 10},
            {"member_id": "CM003", "name": "Alice Johnson",
             "rank": "officer", "age": 28,
             "specialization": "Engineering", "years_experience": 4},
        ],
    }
    try:
        mission = SpaceMission.model_validate(valid_mission)
        display_mission(mission)
    except ValidationError as error:
        print("Unexpected validation error:")
        print_errors(error)

    print()
    print(separator)

    # No Commander or Captain in the crew
    invalid_mission: dict[str, object] = {
        "mission_id": "M2024_LUNA",
        "mission_name": "Lunar Survey",
        "destination": "Moon",
        "launch_date": "2024-09-15T12:00:00",
        "duration_days": 30,
        "budget_millions": 300.0,
        "crew": [
            {"member_id": "CM010", "name": "Emma Brown",
             "rank": "lieutenant", "age": 32,
             "specialization": "Pilot", "years_experience": 8},
            {"member_id": "CM011", "name": "David Lopez",
             "rank": "cadet", "age": 22,
             "specialization": "Research", "years_experience": 1},
        ],
    }
    try:
        SpaceMission.model_validate(invalid_mission)
    except ValidationError as error:
        print("Expected validation error:")
        print_errors(error)


if __name__ == "__main__":
    main()