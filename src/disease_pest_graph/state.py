"""病虫害防治智能体 State"""

from typing import Annotated, TypedDict, Optional, Dict, Any

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from src.graph_common.state import State


class DiseasePestState(TypedDict):
    """
    病虫害防治智能体 State结构
    """

    messages: Annotated[list[AnyMessage], add_messages]
    img_path: Optional[str] = None # 图像路径
    sensor_data: Optional[str] = None # 传感器数据
    analysis_mode: Optional[str] = None
    enhance_image: Optional[bool] = None
    sensor_analysis: Optional[Dict[str, Any]]  # 传感器分析结果
    image_analysis: Optional[Dict[str, Any]]   # 图像分析结果  
    treatment_decision: Optional[Dict[str, Any]]  # 决策结果