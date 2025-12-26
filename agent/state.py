from typing import List, Optional
from typing_extensions import TypedDict

class AgentState(TypedDict):
    files: List[str]                 # remaining files
    current_file: Optional[str]      # file being processed
    category: Optional[str]          # chosen category
    step: int                        # step counter
