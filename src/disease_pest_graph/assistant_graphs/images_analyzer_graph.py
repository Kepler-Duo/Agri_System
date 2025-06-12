from langchain_core.runnables import Runnable
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from configuration import Configuration
from src.disease_pest_graph.prompt import images_analyzer_prompt
from src.disease_pest_graph.state import DiseasePestState
from src.graph_common.assistant import AgriAssistant
from src.disease_pest_graph.mcp_servers import mcp_tools
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage


# class ImagesAnalyzerGraph:
#     def __init__(self, tools=None):
#         self.tools = tools or mcp_tools['images_analyzer_mcp_tools'] + mcp_tools['common_mcp_tools']
#         self.graph = self.build_graph()

#     def build_runnable(self) -> Runnable:
#         llm = Configuration.new_llm()
#         if self.tools:
#             return images_analyzer_prompt | llm.bind_tools(self.tools)
#         return images_analyzer_prompt | llm

#     def build_graph(self) -> CompiledStateGraph:
#         graph = StateGraph(DiseasePestState)

#         # Adding nodes
#         graph.add_node("images_analyzer", AgriAssistant(self.build_runnable()))

#         # Adding edges
#         graph.add_edge(START, "images_analyzer")
#         graph.add_edge("images_analyzer", END)

#         return graph.compile()


class ImagesAnalyzerGraph:
    def __init__(self, tools=None):
        self.tools = tools or mcp_tools["images_analyzer_mcp_tools"] + mcp_tools["common_mcp_tools"]
        self.graph = self.build_graph()

    def build_runnable(self):
        llm = Configuration.new_llm()
        return images_analyzer_prompt | llm.bind_tools(self.tools, parallel_tool_calls=False)

    def build_graph(self) -> CompiledStateGraph:
        graph = StateGraph(DiseasePestState)

        # 添加节点
        graph.add_node("images_analyzer", AgriAssistant(self.build_runnable()))
        graph.add_node("tool_node", ToolNode(self.tools))  # 简洁添加工具处理节点

        # 图结构
        graph.add_edge(START, "images_analyzer")
        graph.add_conditional_edges("images_analyzer", self._route_tool_or_end)
        graph.add_edge("tool_node", "images_analyzer")
        graph.add_edge("images_analyzer", END)  # 如果无工具调用则直接结束

        return graph.compile()

    def _route_tool_or_end(self, state: dict) -> str:
        """
        如果 AIMessage 含有工具调用，则进入 tool_node，否则结束。
        """
        last_msg = next((m for m in reversed(state["messages"]) if isinstance(m, AIMessage)), None)
        if last_msg and getattr(last_msg, "tool_calls", None):
            return "tool_node"
        return END