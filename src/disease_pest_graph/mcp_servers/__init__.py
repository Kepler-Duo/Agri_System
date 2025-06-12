import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient


# 初始化客户端
_client = MultiServerMCPClient(
    {
        "common_server": {
            "url": "http://127.0.0.1:20000/disease_pest/common",
            "transport": "streamable_http",
        },
        "decision_generator_server": {
            "url": "http://127.0.0.1:20001/disease_pest/decision_generator",
            "transport": "streamable_http",
        },
        "images_analyzer_server": {
            "url": "http://127.0.0.1:20002/disease_pest/images_analyzer",
            "transport": "streamable_http",
        },
        "sensor_data_analyzer_server": {
            "url": "http://127.0.0.1:20003/disease_pest/sensor_data_analyzer",
            "transport": "streamable_http",
        },
    }
)

loaded = False
mcp_tools = {
    "common_mcp_tools": [],
    "decision_generator_mcp_tools": [],
    "images_analyzer_mcp_tools": [],
    "sensor_data_analyzer_mcp_tools": [],
}


async def load_mcp_tools():
    global loaded, mcp_tools
    mcp_tools["common_mcp_tools"] = await _client.get_tools(server_name="common_server")
    mcp_tools["decision_generator_mcp_tools"] = await _client.get_tools(
        server_name="decision_generator_server"
    )
    mcp_tools["images_analyzer_mcp_tools"] = await _client.get_tools(
        server_name="images_analyzer_server"
    )
    mcp_tools["sensor_data_analyzer_mcp_tools"] = await _client.get_tools(
        server_name="sensor_data_analyzer_server"
    )
    loaded = True

if loaded == False:
    asyncio.run(load_mcp_tools())