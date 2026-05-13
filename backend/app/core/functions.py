"""工具函数定义模块，为各 Agent 提供可用的工具 schema。"""

coder_tools = [
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
]

# have installed: numpy scipy pandas matplotlib seaborn scikit-learn xgboost

# TODO: pip install python

# TODO: read files

# TODO: get_cites


# Web 搜索工具 schema
search_web_tool = {
    "type": "function",
    "function": {
        "name": "search_web",
        "description": "Search the web for real-world data, statistics, and facts. Returns structured data evidence with source URLs, units, time ranges, and regions.",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query, be specific about what data you need",
                },
                "data_type": {
                    "type": "string",
                    "description": "Type of data expected: 'statistical', 'timeseries', 'categorical', or 'general'",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return (1-10)",
                },
            },
            "required": ["query", "data_type", "max_results"],
            "additionalProperties": False,
        },
    },
}

# RAG 知识检索工具 schema
search_knowledge_tool = {
    "type": "function",
    "function": {
        "name": "search_knowledge",
        "description": "Search the knowledge base for mathematical modeling methods, code templates, and paper writing references.",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query describing what knowledge you need",
                },
                "scope": {
                    "type": "string",
                    "description": "Knowledge scope: 'method' for modeling methods, 'code' for code templates, 'paper' for writing references",
                },
                "method_name": {
                    "type": "string",
                    "description": "Specific method name to search for (e.g. 'TOPSIS', 'AHP'), or empty string for general search",
                },
            },
            "required": ["query", "scope", "method_name"],
            "additionalProperties": False,
        },
    },
}

## writeragent tools
writer_tools = [
    {
        "type": "function",
        "function": {
            "name": "search_papers",
            "description": "Search for papers using a query string.",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The query string"}
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
]
