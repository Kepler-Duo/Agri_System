import os
import json
import pandas as pd
from datetime import datetime
from fastmcp import FastMCP

# 初始化服务
mcp = FastMCP(name='common_server', instructions='病虫害智能体公用服务的MCP服务器')


@mcp.tool()
async def weather_risk_analysis(data: str, data_format: str = "json") -> str:
    """
    # 天气风险分析函数
    根据历史及预测天气数据评估病虫害发生风险。
    该函数解析输入的天气数据（温度、湿度、降雨量等），通过规则引擎计算病虫害风险等级。
    ## 参数:
        data (str): 天气数据字符串。支持格式：
            - JSON: {"temperature": 32, "humidity": 75, "rainfall": 10}
            - CSV: temperature,humidity,rainfall\n32,75,10
        data_format (str, optional): 数据格式，可选 "json" 或 "csv"。默认为 "json"。
    ## 返回:
        str: 包含风险等级、分析依据和时间戳的 JSON 字符串。
            示例格式：
            {
                "timestamp": "2023-10-05T14:30:00",
                "risk_level": "高风险",
                "analysis_basis": {
                    "temperature": 32,
                    "humidity": 75,
                    "rainfall": 10
                }
            }
    """
    if data_format == "json":
        weather_data = json.loads(data)
    else:  # csv
        df = pd.read_csv(data)
        weather_data = df.to_dict(orient="records")[0]

    risk_level = "低风险"
    if weather_data.get("temperature", 25) > 30 and weather_data.get("humidity", 60) > 70:
        risk_level = "高风险"
    elif weather_data.get("rainfall", 0) > 50:
        risk_level = "中风险"

    result = {
        "timestamp": datetime.now().isoformat(),
        "risk_level": risk_level,
        "analysis_basis": {
            "temperature": weather_data.get("temperature", 25),
            "humidity": weather_data.get("humidity", 60),
            "rainfall": weather_data.get("rainfall", 0)
        }
    }

    return json.dumps(result, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    mcp.run(transport='streamable-http', host='127.0.0.1', port=20000, path='/disease_pest/common')