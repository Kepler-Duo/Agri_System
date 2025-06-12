from langchain_core.messages import ToolMessage
from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field
from datetime import datetime

from src.disease_pest_graph.assistant_graphs.images_analyzer_graph import (
    ImagesAnalyzerGraph,
)
from src.disease_pest_graph.state import DiseasePestState


class InvokeImagesAnalyzerAssistant(BaseModel):
    """
    调用图像分析助理，进行病害识别和图像增强分析。
    """

    img_path: str = Field(description="需要分析的图像路径")

    analysis_mode: str = Field(
        description="分析模式：disease_detection（病害检测）、\
                    pest_identification（虫害识别）、\
                    severity_assessment（严重程度评估）、"
    )

    enhance_image: bool = Field(description="是否需要图像增强处理")

    # request: str = Field(description="图像分析需求")

    assistant: str = Field(default="images_analyzer", description="图像分析助理节点名")

    class Config:
        json_schema_extra = {
            "示例": {
                "img_path": "crops/disease_sample.jpg",
                "analysis_mode": "disease_detection",
                "enhance_image": True,
            }
        }


graph = ImagesAnalyzerGraph().graph


async def consult_images_analyzer(state: DiseasePestState):
    """处理图像分析"""
    tool_call_id = None
    img_path = None
    analysis_mode = None
    enhance_image = None

    for tool_call in state["messages"][-1].tool_calls:
        if tool_call["name"] == InvokeImagesAnalyzerAssistant.__name__:
            tool_call_id = tool_call["id"]
            img_path = tool_call["args"]["img_path"]
            analysis_mode = tool_call["args"]["analysis_mode"]
            enhance_image = tool_call["args"]["enhance_image"]

    # 构建图像分析的输入消息
    system_message = f"""
    请对以下图像进行分析：
    
    图像路径：{img_path}
    分析模式：{analysis_mode}
    图像增强：{enhance_image}
    
    根据分析模式调用相应的函数：
    - disease_detection：检测图像中的植物病害，识别病害类型、位置和特征（可能需要调用病害检测工具）
    - pest_identification：识别图像中的害虫种类、数量和危害程度（可能需要调用虫害检测工具）
    - severity_assessment：评估病虫害的严重程度和影响范围
    
    请提供详细的分析结果，包括：
    1. 检测到的病虫害类型
    2. 严重程度评级（轻微/中等/严重）
    3. 影响区域百分比
    4. 病虫害特征描述
    5. 置信度评分
    """

    # 自定义输入参数格式
    assistant_input_format = {
        "messages": [{"role": "system", "content": system_message}]
    }

    result = await graph.ainvoke({"messages": [SystemMessage(content=system_message)]})

    # 异步调用图像分析子图
    # result = await graph.ainvoke(assistant_input_format)

    # 构建图像分析结果
    image_analysis_result = {
        "img_path": img_path,
        "analysis_mode": analysis_mode,
        "enhance_image": enhance_image,
        "analysis_result": result["messages"][-1].content,
        "analyzed_at": datetime.now(),
    }

    return {
        "messages": [
            ToolMessage(
                content=f"图像分析助手返回：{image_analysis_result['analysis_result']}",
                tool_call_id=tool_call_id,
            )
        ],
        "image_analysis": image_analysis_result,  # 保存分析结果
    }