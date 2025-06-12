"""定义调用病虫害防治子图助手所需的类和方法"""

from langchain_core.messages import ToolMessage
from pydantic import BaseModel, Field

from src.disease_pest_graph.graph import DiseasePestGraph
from src.primary_graph.state import CenterState


class InvokeDiseaseAndPestAssistant(BaseModel):
    """
    咨询专门处理病虫害管理的助理。
    """

    img_path: str = Field(description="图像存储的地址")

    sensor_data: str = Field(description="json格式的传感器环境信息")

    request: str = Field(description="用户想要了解的病害或虫害的种类以及防治办法")

    assistant: str = Field(
        default="disease_pest_assistant", description="对应的assistant节点的名字"
    )

    class Config:
        json_schema_extra = {
            "示例": {
                "img_path": "agent/wwc/graph2.png",
                "sensor_data": {"humid": 3, "temperature": 20},
                "request": "我想知道这个作物发生什么了,怎么防治?。",
            }
        }


graph = DiseasePestGraph().graph


async def consult_disease_pest_assistant(state: CenterState):
    # 多重工具调用下获取调用ID和调用参数
    tool_call_id = None
    img_path = None
    sensor_data = None
    tool_request = None

    for tool_call in state["messages"][-1].tool_calls:
        if tool_call["name"] == InvokeDiseaseAndPestAssistant.__name__:
            tool_call_id = tool_call["id"]
            img_path = tool_call["args"]["img_path"]
            sensor_data = tool_call["args"]["sensor_data"]
            tool_request = tool_call["args"]["request"]

    system_message = f'''
    需求：{tool_request},
    图像路径：{img_path},
    传感器数据：{sensor_data}
    '''

    # 自定义输入参数
    assistant_input_format = {
        "messages": [{"role": "system", "content": system_message}],
        "img_path": img_path,
        "sensor_data": sensor_data,
    }

    # 异步调用子图
    result = await graph.ainvoke(assistant_input_format)

    return {
        "messages": [
            ToolMessage(
                content=f"病害防治助手'disease_pest_assistant'返回消息:{result['messages'][-1].content}",
                tool_call_id=tool_call_id,
            )
        ]
    }