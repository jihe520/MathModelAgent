"""请求数据模型定义。"""

from pydantic import BaseModel
from app.schemas.enums import CompTemplate, FormatOutPut


class ExampleRequest(BaseModel):
    """示例建模请求。"""
    example_id: str
    source: str


class Problem(BaseModel):
    """建模问题描述。"""
    task_id: str
    ques_all: str = ""
    comp_template: CompTemplate = CompTemplate.CHINA
    format_output: FormatOutPut = FormatOutPut.Markdown

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        data["comp_template"] = self.comp_template.value
        data["format_output"] = self.format_output.value
        return data
