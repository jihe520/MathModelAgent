"""证据数据模型定义，为 Web Search 和 RAG 提供统一的数据抽象。"""

from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime
from typing import Literal


class Evidence(BaseModel):
    """证据基类，所有搜索/检索产出的统一抽象。"""

    id: str = Field(default_factory=lambda: str(uuid4()))
    content: str
    evidence_type: Literal["data", "knowledge", "code", "paper"]
    source_url: str | None = None
    source_title: str | None = None
    source_level: Literal["official", "academic", "media", "unknown"] = "unknown"
    collected_at: datetime = Field(default_factory=datetime.now)
    confidence: float = Field(default=0.5, ge=0, le=1)
    metadata: dict = Field(default_factory=dict)


class DataEvidence(Evidence):
    """Web Search 产出的结构化数据证据。"""

    evidence_type: Literal["data", "knowledge", "code", "paper"] = "data"
    unit: str | None = None
    time_range: str | None = None
    region: str | None = None
    original_excerpt: str | None = None
    data_format: Literal["table", "timeseries", "categorical"] | None = None


class KnowledgeEvidence(Evidence):
    """RAG 检索产出的知识证据。"""

    evidence_type: Literal["data", "knowledge", "code", "paper"] = "knowledge"
    method_name: str | None = None
    source_type: Literal["paper", "textbook", "code", "problem"] = "textbook"
    source_file: str | None = None
