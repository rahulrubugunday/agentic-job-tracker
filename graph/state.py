from typing import TypedDict, Annotated
import operator


class JobState(TypedDict):
    jobs: Annotated[list, operator.add]
    analyzed: Annotated[list, operator.add]
    errors: Annotated[list, operator.add]