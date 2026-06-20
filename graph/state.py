from typing import TypedDict, Annotated
import operator


class JobState(TypedDict):
    jobs: list
    analyzed: list
    errors: Annotated[list, operator.add]