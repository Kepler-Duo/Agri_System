from langchain_core.messages import ToolMessage
from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field
from datetime import datetime

from src.disease_pest_graph.assistant_graphs.decision_generator_graph import DecisionGeneratorGraph
from src.disease_pest_graph.state import DiseasePestState

class InvokeDecisionGeneratorAssistant(BaseModel):
    """
    调用决策生成助理，生成具体的防治策略和执行方案。
    """
    disease_info: dict = Field(
        description="病虫害信息，必要字段"
    )

    # environment_data: dict = Field(
    #     description="环境数据分析结果，必要字段"
    # )

    # crop_info: dict = Field(
    #     description="作物信息，包含品种、生长阶段、所属地块编号等"
    # )

    decision_type: str = Field(
        description="决策类型：treatment_plan（治疗方案）、prevention_strategy（预防策略）、emergency_response（紧急响应）"
    )

    assistant: str = Field(default="decision_generator", description="决策生成助理节点名")

    class Config:
        json_schema_extra = {
            "示例": {
                "disease_info": {
                    "type": "叶斑病"
                },
                "decision_type": "treatment_plan"
            }
        }

graph = DecisionGeneratorGraph().graph
async def consult_decision_generator(state: DiseasePestState):
    """生成防治决策"""
    tool_call_id = None
    disease_info = None
    environment_data = None
    crop_info = None
    decision_type = None
    for tool_call in state["messages"][-1].tool_calls:
        if tool_call["name"] == InvokeDecisionGeneratorAssistant.__name__:
            tool_call_id = tool_call["id"]
            disease_info = state.get("image_analysis") or tool_call["args"]["disease_info"]
            # environment_data = tool_call["args"]["environment_data"]
            # crop_info = tool_call["args"]["crop_info"]
            decision_type = tool_call["args"]["decision_type"]

    # 综合之前的分析结果生成决策
    sensor_data = state.get("sensor_analysis", {})
    image_data = state.get("image_analysis", {})

    # 环境数据：{environment_data}
    # 作物信息：{crop_info}

    # 构建系统消息
    system_message = f"""
    请根据以下信息生成具体的防治决策方案：
    
    病虫害信息：{disease_info}
    传感器分析结果：{sensor_data}
    图像分析结果：{image_data}
    决策类型：{decision_type}
    
    请生成详细的防治方案，包括：
    1. 具体的防治措施
    2. 推荐的农药或生物防治方法
    3. 施用时间和频次
    4. 预期效果和注意事项
    5. 监测建议
    """

    # 自定义输入参数格式
    assistant_input_format = {
        "messages": [{"role": "system", "content": system_message}]
    }

    # 异步调用决策生成子图
    result = await graph.ainvoke({"messages": [SystemMessage(content=system_message)]})

    # 构建治疗方案结果
    treatment_plan = {
        "decision_type": decision_type,
        "disease_info": disease_info,
        "crop_info": crop_info,
        "treatment_measures": result['messages'][-1].content,
        "generated_at": datetime.now(), 
        "context_data": {
            "sensor_analysis": sensor_data,
            "image_analysis": image_data,
            "environment_data": environment_data
        }
    }

    return {
        "messages": [
            ToolMessage(
                content=f"决策生成助手返回治疗方案：{treatment_plan['treatment_measures']}",
                tool_call_id=tool_call_id,
            )
        ],
        "treatment_decision": treatment_plan
    }