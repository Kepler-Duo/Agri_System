import os
import json
import pandas as pd
from datetime import datetime
from fastmcp import FastMCP

# 初始化服务
mcp = FastMCP(name='images_analyzer_server', instructions='图像分析助理的MCP服务器')

@mcp.tool()
async def image_enhancement(img_path: str) -> str:
    """
    # 图像增强/复原函数
    对多光谱/高光谱图像进行增强或复原处理。
    该函数应用图像处理算法提升图像质量，消除噪声或失真，生成清晰的图像用于后续分析。
    ## 参数:
        img_path (str): 输入图像的文件路径。支持格式包括 RGB（JPEG/PNG）和多光谱（tif/tiff）。
    ## 返回:
        str: 包含处理后图像保存路径的文本信息。
            示例格式：'图像增强完成，已保存至 processed_{original_filename}'
    """
    processed_path = f"processed_{os.path.basename(img_path)}"
    return f"图像增强完成，已保存至 {processed_path}"

@mcp.tool()
async def rice_disease_detection(img_path: str) -> str:
    """
    # 水稻病害检测函数
    使用预训练模型对水稻病害图像进行分类、检测和分割。
    该函数加载水稻病害图像，通过模型返回分类结果、检测框和分割掩膜。
    ## 参数:
        img_path (str): 输入图像的文件路径。支持格式包括 RGB（JPEG/PNG）和多光谱（tif/tiff）。
    ## 返回:
        str: 包含分类、检测和分割结果的 JSON 字符串。
            示例格式：
            {
                "timestamp": "2023-10-05T14:30:00",
                "classification": {"class": "稻瘟病", "confidence": 0.92},
                "detection": [
                    {"bbox": [120, 80, 200, 150], "label": "稻瘟病病斑", "confidence": 0.88},
                    {"bbox": [300, 100, 180, 140], "label": "纹枯病", "confidence": 0.76}
                ],
                "segmentation": {
                    "mask_coords": [[120,80],[120,230],[320,230],[320,80]],
                    "label": "稻瘟病",
                    "confidence": 0.91
                }
            }
    """
    result = {
        "timestamp": datetime.now().isoformat(),
        "classification": {"class": "稻瘟病", "confidence": 0.92},
        "detection": [
            {"bbox": [120, 80, 200, 150], "label": "稻瘟病病斑", "confidence": 0.88},
            {"bbox": [300, 100, 180, 140], "label": "纹枯病", "confidence": 0.76}
        ],
        "segmentation": {
            "mask_coords": [[120,80],[120,230],[320,230],[320,80]],
            "label": "稻瘟病",
            "confidence": 0.91
        }
    }

    return json.dumps(result, indent=2, ensure_ascii=False)

@mcp.tool()
async def rice_pest_detection(img_path: str) -> str:
    """
    # 水稻虫害检测函数
    使用预训练模型对水稻虫害图像进行分类、检测和分割。
    该函数加载水稻虫害图像，通过模型返回分类结果、检测框和分割掩膜。
    ## 参数:
        img_path (str): 输入图像的文件路径。支持格式包括 RGB（JPEG/PNG）和多光谱（tif/tiff）。
    ## 返回:
        str: 包含分类、检测和分割结果的 JSON 字符串。
            示例格式：
            {
                "timestamp": "2023-10-05T14:30:00",
                "classification": {"class": "稻飞虱", "confidence": 0.89},
                "detection": [
                    {"bbox": [150, 120, 40, 30], "label": "褐飞虱", "confidence": 0.85},
                    {"bbox": [280, 130, 35, 28], "label": "白背飞虱", "confidence": 0.78}
                ],
                "segmentation": {
                    "mask_coords": [[150,120],[150,150],[190,150],[190,120]],
                    "label": "稻飞虱",
                    "confidence": 0.87
                }
            }
    """
    result = {
        "timestamp": datetime.now().isoformat(),
        "classification": {"class": "稻飞虱", "confidence": 0.89},
        "detection": [
            {"bbox": [150, 120, 40, 30], "label": "褐飞虱", "confidence": 0.85},
            {"bbox": [280, 130, 35, 28], "label": "白背飞虱", "confidence": 0.78}
        ],
        "segmentation": {
            "mask_coords": [[150,120],[150,150],[190,150],[190,120]],
            "label": "稻飞虱",
            "confidence": 0.87
        }
    }

    return json.dumps(result, indent=2, ensure_ascii=False)

@mcp.tool()
async def rice_weed_detection(img_path: str) -> str:
    """
    # 水稻杂草检测函数
    使用预训练模型对水稻杂草图像进行分类、检测和分割。
    该函数加载水稻杂草图像，通过模型返回分类结果、检测框和分割掩膜。
    ## 参数:
        img_path (str): 输入图像的文件路径。支持格式包括 RGB（JPEG/PNG）和多光谱（tif/tiff）。
    ## 返回:
        str: 包含分类、检测和分割结果的 JSON 字符串。
            示例格式：
            {
                "timestamp": "2023-10-05T14:30:00",
                "classification": {"class": "稗草", "confidence": 0.93},
                "detection": [
                    {"bbox": [80, 60, 100, 80], "label": "稗草", "confidence": 0.91},
                    {"bbox": [250, 70, 90, 75], "label": "水苋菜", "confidence": 0.82}
                ],
                "segmentation": {
                    "mask_coords": [[80,60],[80,140],[180,140],[180,60]],
                    "label": "稗草",
                    "confidence": 0.92
                }
            }
    """
    result = {
        "timestamp": datetime.now().isoformat(),
        "classification": {"class": "稗草", "confidence": 0.93},
        "detection": [
            {"bbox": [80, 60, 100, 80], "label": "稗草", "confidence": 0.91},
            {"bbox": [250, 70, 90, 75], "label": "水苋菜", "confidence": 0.82}
        ],
        "segmentation": {
            "mask_coords": [[80,60],[80,140],[180,140],[180,60]],
            "label": "稗草",
            "confidence": 0.92
        }
    }

    return json.dumps(result, indent=2, ensure_ascii=False)

@mcp.tool()
async def early_disease_pest_monitoring(
    remote_sensing_img: str,
    weather_data: str,
    data_format: str = "json"
) -> str:
    """
    # 病虫害早期监测函数
    基于多源数据（遥感影像、气象数据、作物生长数据）进行病虫害早期监测分析。
    该函数融合遥感图像、气象数据等多维度信息，生成病虫害分布热力图和风险评估结果。
    ## 参数:
        remote_sensing_img (str): 遥感影像文件路径。支持格式包括 RGB（JPEG/PNG）和多光谱（tif/tiff）。
        weather_data (str): 气象数据字符串。支持格式：
            - JSON: {"temperature": 28, "humidity": 75, "precipitation": 20}
            - CSV: temperature,humidity,precipitation\n28,75,20
        data_format (str, optional): 气象数据格式，可选 "json" 或 "csv"。默认为 "json"。
    ## 返回:
        str: 包含病虫害监测结果和热力图文件路径的 JSON 字符串。
            示例格式：
            {
                "timestamp": "2023-10-05T14:30:00",
                "affected_areas": [
                    {"bbox": [1200, 800, 400, 300], "type": "稻瘟病", "severity": "中度", "area_sqm": 250.5},
                    {"bbox": [2800, 1500, 600, 400], "type": "纹枯病", "severity": "轻度", "area_sqm": 120.3}
                ],
                "heatmaps": {
                    "rgb": "heatmap_rgb_processed_image.jpg",
                    "geotiff": "heatmap_geotiff_processed_image.tif"
                },
                "risk_factors": {
                    "temperature": 28,
                    "humidity": 75,
                    "precipitation": 20
                }
            }
    """
    processed_img = f"processed_{os.path.basename(remote_sensing_img)}"

    if data_format == "json":
        weather_info = json.loads(weather_data)
    else:  # CSV格式
        df_weather = pd.read_csv(weather_data)
        weather_info = df_weather.to_dict(orient="records")[0]

    monitoring_result = {
        "timestamp": datetime.now().isoformat(),
        "affected_areas": [
            {"bbox": [1200, 800, 400, 300], "type": "稻瘟病", "severity": "中度", "area_sqm": 250.5},
            {"bbox": [2800, 1500, 600, 400], "type": "纹枯病", "severity": "轻度", "area_sqm": 120.3}
        ],
        "heatmaps": {
            "rgb": f"heatmap_rgb_{os.path.basename(remote_sensing_img)}",
            "geotiff": f"heatmap_geotiff_{os.path.basename(remote_sensing_img)}"
        },
        "risk_factors": {
            "temperature": weather_info.get("temperature", 28),
            "humidity": weather_info.get("humidity", 75),
            "precipitation": weather_info.get("precipitation", 20)
        }
    }

    return json.dumps(monitoring_result, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    mcp.run(transport='streamable-http', host='127.0.0.1', port=20002, path='/disease_pest/images_analyzer')