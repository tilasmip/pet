from enum import Enum


class AdoptionStatus(Enum):
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"
    PENDING = "PENDING"
    CANCELED = "CANCELED"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
