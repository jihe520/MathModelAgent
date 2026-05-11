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
