from typing import List, Dict, Any
from app.tools.openalex_scholar import OpenAlexScholar

tools = [
    {
        "type": "function",
        "function": {
            "name": "execute_code",
            "description": "This function allows you to execute Python code and retrieve the terminal output. If the code "
            "generates image output, the function will return the text '[image]'. The code is sent to a "
            "Jupyter kernel for execution. The kernel will remain active after execution, retaining all "
            "variables in memory."
            "You cannot show rich outputs like plots or images, but you can store them in the working directory and point the user to them. ",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "The code text"}
                },
                "required": ["code"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_literature",
            "description": "Search for academic literature using a query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query."},
                    "author": {"type": "string", "description": "Filter by author name."},
                    "year": {"type": "integer", "description": "Filter by publication year."},
                },
                "required": ["query"],
            },
        },
    },
]

def search_literature(query: str, author: str = None, year: int = None) -> List[Dict[str, Any]]:
    """Search for academic literature."""
    scholar = OpenAlexScholar()
    papers = scholar.search_papers(query, author=author, year=year)
    return papers


## writeragent tools
