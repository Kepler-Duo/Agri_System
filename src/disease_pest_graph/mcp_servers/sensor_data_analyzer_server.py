import os
import json
import pandas as pd
from datetime import datetime
from fastmcp import FastMCP

# 初始化服务
mcp = FastMCP(name='sensor_data_analyzer_server', instructions='传感器数据分析助理的MCP服务器')

@mcp.tool()
async def soil_condition_analysis(data: str, data_format: str = "csv") -> str:
    """
    # 土壤条件分析函数
    分析土壤传感器数据并评估其对病虫害的影响。
    该函数解析输入的土壤数据（湿度、养分含量等），计算土壤健康评分，并评估病虫害风险等级。
    ## 参数:
        data (str): 土壤传感器数据字符串。支持格式：
            - CSV: moisture,nitrogen\n32,1.2
            - Database format: "moisture=32&nitrogen=1.2"
        data_format (str, optional): 数据格式，可选 "csv" 或 "database"。默认为 "csv"。
    ## 返回:
        str: 包含土壤健康状况、健康评分和病虫害风险等级的 JSON 字符串。
            示例格式：
            {
                "timestamp": "2023-10-05T14:30:00",
                "soil_health": {
                    "moisture": 32,
                    "nutrient_level": 1.2,
                    "health_score": 0.75
                },
                "disease_risk_impact": "中风险"
            }
    """
    if data_format == "csv":
        df = pd.read_csv(data)
        soil_data = df.to_dict(orient="records")[0]
    else:  # database format
        soil_data = {
            "moisture": float(data.split("=")[1].split("&")[0]),
            "nitrogen": float(data.split("&")[1].split("=")[1])
        }

    health_score = (soil_data.get("moisture", 32) / 40) * 0.6 + (soil_data.get("nitrogen", 1.2) / 2.0) * 0.4

    result = {
        "timestamp": datetime.now().isoformat(),
        "soil_health": {
            "moisture": soil_data.get("moisture", 32),
            "nutrient_level": soil_data.get("nitrogen", 1.2),
            "health_score": round(health_score, 2)
        },
        "disease_risk_impact": "低风险" if health_score > 0.7 else "中风险"
    }

    return json.dumps(result, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    mcp.run(transport='streamable-http', host='127.0.0.1', port=20003, path='/disease_pest/sensor_data_analyzer')