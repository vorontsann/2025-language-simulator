from typing import Optional

from pydantic import BaseModel, Field

from .progress import Progress


class User(BaseModel):
    """Represents a user of the quiz system."""

    user_id: str = Field(..., description='Unique user identifier')
    name: str
    progress: Optional[Progress] = Field(default_factory=Progress, description='User progress data')

    class Config:
        """Initialize class for Pydantic to store the Progress object."""

        arbitrary_types_allowed = True
