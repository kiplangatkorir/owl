# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========

import argparse
from dotenv import load_dotenv
import networkx as nx
import matplotlib.pyplot as plt
from camel.models import ModelFactory
from camel.toolkits import (
    ArxivToolkit,
    DocumentProcessingToolkit,
    SearchToolkit,
    NetworkXToolkit,
    CodeExecutionToolkit,
)
from camel.types import ModelPlatformType, ModelType
from camel.societies import RolePlaying
from owl.utils import run_society

load_dotenv()


def construct_society(query: str) -> RolePlaying:
    """Construct a society of research agents.

    Args:
        query (str): The research query to investigate.

    Returns:
        RolePlaying: A configured society of research agents.
    """
    # Create models for different components
    models = {
        "user": ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O,
            model_config_dict={"temperature": 0},
        ),
        "assistant": ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O,
            model_config_dict={"temperature": 0},
        ),
        "document": ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O,
            model_config_dict={"temperature": 0},
        ),
    }

    # Configure toolkits
    tools = [
        *ArxivToolkit().get_tools(),
        *DocumentProcessingToolkit(model=models["document"]).get_tools(),
        SearchToolkit().search_google_scholar,
        SearchToolkit().search_semantic_scholar,
        *NetworkXToolkit().get_tools(),
        *CodeExecutionToolkit(sandbox="subprocess", verbose=True).get_tools(),
    ]

    # Configure agent roles
    user_agent_kwargs = {"model": models["user"]}
    assistant_agent_kwargs = {"model": models["assistant"], "tools": tools}

    # Configure task parameters
    task_kwargs = {
        "task_prompt": (
            f"Research Query: {query}\n\n"
            "1. Search for relevant academic papers using ArXiv and Scholar APIs\n"
            "2. Process and analyze the papers to extract key information\n"
            "3. Create a knowledge graph showing relationships between concepts\n"
            "4. Generate a comprehensive research summary\n"
            "5. Be ready to answer questions about the findings"
        ),
        "with_task_specify": True,
    }

    # Create and return the society
    society = RolePlaying(
        **task_kwargs,
        user_role_name="researcher",
        user_agent_kwargs=user_agent_kwargs,
        assistant_role_name="research_assistant",
        assistant_agent_kwargs=assistant_agent_kwargs,
    )

    return society


def visualize_knowledge_graph(concepts: dict):
    """Create and display a knowledge graph of research concepts.

    Args:
        concepts (dict): Dictionary of concepts and their relationships.
    """
    G = nx.Graph()
    
    # Add nodes and edges
    for concept, related in concepts.items():
        G.add_node(concept)
        for relation, targets in related.items():
            for target in targets:
                G.add_edge(concept, target, relation=relation)

    # Draw the graph
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=1500, font_size=8, font_weight='bold')
    
    # Add edge labels
    edge_labels = nx.get_edge_attributes(G, 'relation')
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    
    plt.title("Research Concept Knowledge Graph")
    plt.savefig("knowledge_graph.png")
    plt.close()


def main():
    """Main function to run the research assistant."""
    parser = argparse.ArgumentParser(description="ResearchGPT: AI Research Assistant")
    parser.add_argument("--query", type=str, required=True,
                      help="Research query to investigate")
    args = parser.parse_args()

    # Construct and run the society
    society = construct_society(args.query)
    answer, chat_history, token_count = run_society(society)

    # Output the results
    print("\n=== Research Summary ===")
    print(f"\033[94m{answer}\033[0m")
    print(f"\nTotal tokens used: {token_count}")


if __name__ == "__main__":
    main()
