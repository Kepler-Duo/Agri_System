from langchain_core.messages import ToolMessage
from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field
from datetime import datetime

from src.disease_pest_graph.assistant_graphs.sensor_data_analyzer_graph import SensorDataAnalyzerGraph
from src.disease_pest_graph.state import DiseasePestState

class InvokeSensorDataAnalyzerAssistant(BaseModel):
    """
    调用传感器数据分析助理，分析土壤湿度、温度等环境数据。
    """
    sensor_data: dict = Field(
        description="传感器数据，包含土壤湿度、温度、pH值，空气湿度等"
    )

    analysis_type: str = Field(
        description="分析类型：environment_risk（环境风险评估）、optimal_conditions（最适条件分析）等"
    )

    assistant: str = Field(default="sensor_data_analyzer", description="传感器数据分析助理节点名")

    class Config:
        json_schema_extra = {
            "示例": {
                "sensor_data": {
                    "soil_moisture": 45.2,
                    "temperature": 28.5,
                    "humidity": 75.8,
                    "ph": 6.8
                },
                "analysis_type": "environment_risk"
            }
        }

graph = SensorDataAnalyzerGraph().graph
async def consult_sensor_data_analyzer(state: DiseasePestState):
    """处理传感器数据分析"""
    tool_call_id = None
    sensor_data = None
    analysis_type = None

    for tool_call in state["messages"][-1].tool_calls:
        if tool_call["name"] == InvokeSensorDataAnalyzerAssistant.__name__:
            tool_call_id = tool_call["id"]
            sensor_data = tool_call["args"]["sensor_data"]
            analysis_type = tool_call["args"]["analysis_type"]

    # 构建传感器数据分析的输入消息
    system_message = f"""
    请对以下传感器数据进行分析：
    
    传感器数据：{sensor_data}
    分析类型：{analysis_type}
    
    根据分析类型执行相应的任务：
    - environment_risk：评估当前环境条件下的病虫害风险
    - optimal_conditions：分析最适宜的作物生长条件
    
    请提供详细的分析结果，包括：
    1. 环境参数评估（土壤湿度、温度、湿度、pH值等）
    2. 病虫害风险等级评估
    3. 环境因子对作物生长的影响分析
    4. 异常数据识别和警告
    5. 预测性分析（未来风险趋势）
    
    数据详情：
    - 土壤湿度: {sensor_data.get('soil_moisture', 'N/A')}%
    - 温度: {sensor_data.get('temperature', 'N/A')}°C
    - 空气湿度: {sensor_data.get('humidity', 'N/A')}%
    - pH值: {sensor_data.get('ph', 'N/A')}
    - 其他参数: {dict((k, v) for k, v in sensor_data.items() if k not in ['soil_moisture', 'temperature', 'humidity', 'ph'])}
    """

    # 自定义输入参数格式
    assistant_input_format = {
        "messages": [{"role": "system", "content": system_message}]
    }

    # 异步调用传感器数据分析子图
    result = await graph.ainvoke({"messages": [SystemMessage(content=system_message)]})

    # 构建传感器数据分析结果
    analysis_result = {
        "sensor_data": sensor_data,
        "analysis_type": analysis_type,
        "analysis_result": result['messages'][-1].content,
        "analyzed_at": datetime.now(),
    }

    return {
        "messages": [
            ToolMessage(
                content=f"传感器数据分析助手返回：{analysis_result['analysis_result']}",
                tool_call_id=tool_call_id,
            )
        ],
        "sensor_analysis": analysis_result  # 保存分析结果供其他节点使用
    }