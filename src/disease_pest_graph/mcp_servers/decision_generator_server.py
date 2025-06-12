import os
import json
import pandas as pd
from datetime import datetime
from fastmcp import FastMCP

# 初始化服务
mcp = FastMCP(name='decision_generator_server', instructions='决策生成助理的MCP服务器')

from datetime import datetime
import json

@mcp.tool()
async def pesticide_recommendation(
    pest_type: str,
    crop_stage: str,
    area_hectares: float,
    soil_moisture_percent: int,
    temperature_celsius: int
) -> str:
    """
    # 农药推荐工具
    根据病虫害类型、作物生长阶段和环境条件，推荐合适的农药及其施用方案。
    该工具结合农作物病虫害防治数据库和农药适配规则，返回推荐的农药名称、剂量、施用方法及注意事项。
    ## 参数:
        pest_type (str): 检测到的病虫害类型（如“稻瘟病”、“纹枯病”）。
        crop_stage (str): 作物当前生长阶段（如“分蘖期”、“抽穗期”）。
        area_hectares (float): 需要施药的农田面积（单位：公顷）。
        soil_moisture_percent (int): 当前土壤湿度百分比（0-100%）。
        temperature_celsius (int): 当前环境温度（摄氏度）。
    ## 返回:
        str: 包含农药推荐方案的 JSON 字符串。
            示例格式：
            {
                "timestamp": "2025-06-07T09:00:00",
                "pesticide_name": "井冈霉素",
                "dose_ml_per_hectare": 1500,
                "application_method": "无人机喷雾",
                "precautions": [
                    "避免在高温时段（35°C以上）施药",
                    "施药后24小时内禁止进入田间"
                ],
                "validity_period": "2025-06-07至2025-06-10"
            }
    """
    result = {
        "timestamp": datetime.now().isoformat(),
        "pesticide_name": "井冈霉素",
        "dose_ml_per_hectare": 1500,
        "application_method": "无人机喷雾",
        "precautions": [
            "避免在高温时段（35°C以上）施药",
            "施药后24小时内禁止进入田间"
        ],
        "validity_period": "2025-06-07至2025-06-10"
    }

    return json.dumps(result, indent=2, ensure_ascii=False)

from datetime import datetime, timedelta
import json

@mcp.tool()
async def spray_time_planner(
    weather_forecast: dict,
    crop_stage: str,
    current_time: str
) -> str:
    """
    # 施药时间规划工具
    根据天气预测、作物生长阶段和当前时间，规划最佳施药时间窗口。
    该工具综合考虑降雨概率、风速、作物敏感性等因素，推荐适合施药的时间段。
    ## 参数:
        weather_forecast (dict): 天气预测数据，格式示例如下：
            {
                "forecast_hours": 48,
                "precipitation_probability": {"12h": 5%, "24h": 15%, "36h": 30%},
                "wind_speed_m_s": {"12h": 1.2, "24h": 2.5, "36h": 3.8}
            }
        crop_stage (str): 作物当前生长阶段（如“分蘖期”、“抽穗期”）。
        current_time (str): 当前时间戳（ISO 8601 格式，如"2025-06-07T08:00:00"）。
    ## 返回:
        str: 包含推荐施药时间窗口的 JSON 字符串。
            示例格式：
            {
                "timestamp": "2025-06-07T08:00:00",
                "recommended_window": {
                    "start": "2025-06-07T09:00:00",
                    "end": "2025-06-07T11:00:00"
                },
                "reason": "降雨概率<10%，风速<2.5m/s，作物耐受度高"
            }
    """
    result = {
        "timestamp": current_time,
        "recommended_window": {
            "start": "2025-06-07T09:00:00",
            "end": "2025-06-07T11:00:00"
        },
        "reason": "降雨概率<10%，风速<2.5m/s，作物耐受度高"
    }

    return json.dumps(result, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    mcp.run(transport='streamable-http', host='127.0.0.1', port=20001, path='/disease_pest/decision_generator')