from langchain_core.runnables import Runnable
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from configuration import Configuration
from src.disease_pest_graph.prompt import disease_pest_prompt
from src.disease_pest_graph.state import DiseasePestState
from src.graph_common.assistant import AgriAssistant
from src.disease_pest_graph.disease_pest_assistants.decision_generator_invoke import (
    InvokeDecisionGeneratorAssistant, consult_decision_generator
)
from src.disease_pest_graph.disease_pest_assistants.images_analyzer_invoke import (
    InvokeImagesAnalyzerAssistant, consult_images_analyzer
)
from src.disease_pest_graph.disease_pest_assistants.sensor_data_analyzer_invoke import (
    InvokeSensorDataAnalyzerAssistant, consult_sensor_data_analyzer
)


class DiseasePestGraph:
    def __init__(self, assistants=None, tools=None):
        self.assistants = assistants or [
            InvokeDecisionGeneratorAssistant,
            InvokeImagesAnalyzerAssistant,
            InvokeSensorDataAnalyzerAssistant
        ]
        self.tools = tools or []
        self.graph = self.build_graph()

    def build_runnable(self) -> Runnable:
        llm = Configuration.new_llm()
        # 绑定子助理工具到病虫害助手
        if self.tools or self.assistants:
            return disease_pest_prompt | llm.bind_tools(self.assistants + self.tools, parallel_tool_calls=False)
        return disease_pest_prompt | llm

    def route(self, state: DiseasePestState):
        """根据工具调用路由到相应的子助理"""
        messages = state.get("messages", [])
        if not messages:
            return END

        message = messages[-1]
        if not hasattr(message, 'tool_calls') or not message.tool_calls:
            return END

        tools_by_name = {tool.__name__: tool for tool in self.assistants}

        return [
            tools_by_name[call["name"]].model_fields["assistant"].default
            for call in message.tool_calls
        ]

    def build_graph(self) -> CompiledStateGraph:
        graph = StateGraph(DiseasePestState)

        # Adding nodes
        graph.add_node("disease_pest_assistant", AgriAssistant(self.build_runnable()))


        graph.add_node("sensor_data_analyzer", consult_sensor_data_analyzer)
        graph.add_node("images_analyzer", consult_images_analyzer)
        graph.add_node("decision_generator", consult_decision_generator)

        # Adding edges
        graph.add_edge(START, "disease_pest_assistant")

        # 添加条件边，支持路由到子助理
        graph.add_conditional_edges(
            "disease_pest_assistant",
            self.route,
            ["sensor_data_analyzer", "images_analyzer", "decision_generator", END]
        )

        graph.add_edge("sensor_data_analyzer", "disease_pest_assistant")
        graph.add_edge("images_analyzer", "disease_pest_assistant")
        graph.add_edge("decision_generator", "disease_pest_assistant")

        return graph.compile()