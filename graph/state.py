from typing import TypedDict, Annotated, Optional
import operator


class JobState(TypedDict):
    jobs: list
    analyzed: list
    errors: Annotated[list, operator.add]
    profile_text: Optional[str]
