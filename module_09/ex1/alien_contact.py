"""Exercise 1: Alien Contact Logs.

Custom business-rule validation with @model_validator(mode='after').
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    """Allowed kinds of alien contact."""

    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    """Validated alien contact report."""

    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def check_business_rules(self) -> "AlienContact":
        """Check rules that involve several fields at once.

        Runs after every field has already been type-checked and
        constrained, so self.contact_type is a real ContactType here.
        """
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")

        if (self.contact_type == ContactType.PHYSICAL
                and not self.is_verified):
            raise ValueError("Physical contact reports must be verified")

        if (self.contact_type == ContactType.TELEPATHIC
                and self.witness_count < 3):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals (> 7.0) must include a message")

        # The 'after' validator must return the validated instance
        return self


def display_contact(contact: AlienContact) -> None:
    """Print a contact report in a readable format."""
    print("Valid contact report:")
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type.value}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    if contact.message_received is not None:
        print(f"Message: '{contact.message_received}'")


def print_errors(error: ValidationError) -> None:
    """Print only the human-readable part of each validation error."""
    for detail in error.errors():
        # Errors raised as ValueError get a "Value error, " prefix
        print(detail["msg"].removeprefix("Value error, "))


def main() -> None:
    """Demonstrate a valid report and an invalid one."""
    separator = "=" * 38
    print("Alien Contact Log Validation")
    print(separator)

    # Raw report data, as it would arrive from an external source.
    # Strings are converted to datetime / ContactType automatically.
    valid_report: dict[str, object] = {
        "contact_id": "AC_2024_001",
        "timestamp": "2024-01-15T14:30:00",
        "location": "Area 51, Nevada",
        "contact_type": "radio",
        "signal_strength": 8.5,
        "duration_minutes": 45,
        "witness_count": 5,
        "message_received": "Greetings from Zeta Reticuli",
    }
    try:
        contact = AlienContact.model_validate(valid_report)
        display_contact(contact)
    except ValidationError as error:
        print("Unexpected validation error:")
        print_errors(error)

    print()
    print(separator)

    # Telepathic contact with only one witness breaks a business rule
    invalid_report: dict[str, object] = {
        "contact_id": "AC_2024_002",
        "timestamp": "2024-01-16T09:15:00",
        "location": "Roswell, New Mexico",
        "contact_type": "telepathic",
        "signal_strength": 6.2,
        "duration_minutes": 30,
        "witness_count": 1,
    }
    try:
        AlienContact.model_validate(invalid_report)
    except ValidationError as error:
        print("Expected validation error:")
        print_errors(error)


if __name__ == "__main__":
    main()