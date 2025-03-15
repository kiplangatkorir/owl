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
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple

from dotenv import load_dotenv
import matplotlib.pyplot as plt
import pandas as pd

from camel.models import ModelFactory
from camel.toolkits import (
    BrowserToolkit,
    DocumentProcessingToolkit,
    FileWriteToolkit,
    CodeExecutionToolkit,
    MCPToolkit,
)
from camel.types import ModelPlatformType, ModelType
from camel.societies import RolePlaying
from owl.utils import run_society

load_dotenv()

class ScrumEvent:
    """Base class for Scrum events."""
    def __init__(self, team: str, sprint: int):
        self.team = team
        self.sprint = sprint
        self.output_dir = f"outputs/{team}/sprint_{sprint}"
        os.makedirs(self.output_dir, exist_ok=True)

    def get_prompt(self) -> str:
        """Get the event-specific prompt."""
        raise NotImplementedError

class SprintPlanning(ScrumEvent):
    """Sprint Planning event handler."""
    def get_prompt(self) -> str:
        return (
            f"Team: {self.team}, Sprint: {self.sprint}\n\n"
            "As a Scrum Master, facilitate the Sprint Planning meeting:\n"
            "1. Review and refine the top priority items from the product backlog\n"
            "2. Help the team determine their capacity for this sprint\n"
            "3. Assist in breaking down user stories into tasks\n"
            "4. Track sprint commitments and ensure they align with the team's capacity\n"
            "5. Document the sprint goal and sprint backlog\n"
            "6. Identify potential risks or impediments\n"
        )

class DailyScrum(ScrumEvent):
    """Daily Scrum event handler."""
    def get_prompt(self) -> str:
        return (
            f"Team: {self.team}, Sprint: {self.sprint}\n\n"
            "As a Scrum Master, facilitate the Daily Scrum:\n"
            "1. Help team members share their updates effectively\n"
            "2. Track progress towards the sprint goal\n"
            "3. Identify any impediments or blockers\n"
            "4. Note any items requiring follow-up discussions\n"
            "5. Update the sprint burndown chart\n"
            "6. Ensure the meeting stays focused and time-boxed\n"
        )

class SprintReview(ScrumEvent):
    """Sprint Review event handler."""
    def get_prompt(self) -> str:
        return (
            f"Team: {self.team}, Sprint: {self.sprint}\n\n"
            "As a Scrum Master, facilitate the Sprint Review:\n"
            "1. Help the team demonstrate completed work\n"
            "2. Track stakeholder feedback and suggestions\n"
            "3. Analyze sprint goal achievement\n"
            "4. Document lessons learned and improvement areas\n"
            "5. Update product backlog based on feedback\n"
            "6. Prepare sprint metrics and charts\n"
        )

class Retrospective(ScrumEvent):
    """Sprint Retrospective event handler."""
    def get_prompt(self) -> str:
        return (
            f"Team: {self.team}, Sprint: {self.sprint}\n\n"
            "As a Scrum Master, facilitate the Sprint Retrospective:\n"
            "1. Guide the team in reflecting on their process\n"
            "2. Help identify what went well\n"
            "3. Help identify areas for improvement\n"
            "4. Track action items from previous retrospectives\n"
            "5. Create concrete action items for the next sprint\n"
            "6. Document team health metrics and trends\n"
        )

def construct_society(event: ScrumEvent) -> RolePlaying:
    """Construct a society of Scrum agents.

    Args:
        event: The Scrum event to handle.

    Returns:
        RolePlaying: A configured society of Scrum agents.
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
        *BrowserToolkit(headless=True).get_tools(),  # For accessing agile tools
        *DocumentProcessingToolkit(model=models["document"]).get_tools(),
        *FileWriteToolkit(output_dir=event.output_dir).get_tools(),
        *CodeExecutionToolkit(sandbox="subprocess", verbose=True).get_tools(),
        *MCPToolkit().get_tools(),  # For structured interactions
    ]

    # Configure agent roles
    user_agent_kwargs = {
        "model": models["user"],
        "role_name": "Scrum_Master",
        "role_description": (
            "An experienced Scrum Master who facilitates Scrum events, "
            "removes impediments, and helps the team improve their process."
        ),
    }
    assistant_agent_kwargs = {
        "model": models["assistant"],
        "role_name": "Agile_Coach",
        "role_description": (
            "An AI assistant with deep knowledge of Scrum and agile practices, "
            "helping the Scrum Master facilitate events and improve team performance."
        ),
        "tools": tools,
    }

    # Configure task parameters
    task_kwargs = {
        "task_prompt": event.get_prompt(),
        "with_task_specify": True,
    }

    # Create and return the society
    society = RolePlaying(
        **task_kwargs,
        user_role_name="scrum_master",
        user_agent_kwargs=user_agent_kwargs,
        assistant_role_name="agile_coach",
        assistant_agent_kwargs=assistant_agent_kwargs,
    )

    return society

def generate_burndown_chart(team: str, sprint: int, data: pd.DataFrame):
    """Generate a sprint burndown chart.

    Args:
        team: Team name
        sprint: Sprint number
        data: DataFrame with daily progress data
    """
    plt.figure(figsize=(10, 6))
    plt.plot(data['Date'], data['Remaining'], marker='o', label='Actual')
    plt.plot(data['Date'], data['Ideal'], linestyle='--', label='Ideal')
    
    plt.title(f'Sprint {sprint} Burndown Chart - Team {team}')
    plt.xlabel('Date')
    plt.ylabel('Story Points Remaining')
    plt.grid(True)
    plt.legend()
    
    output_path = f"outputs/{team}/sprint_{sprint}/burndown_chart.png"
    plt.savefig(output_path)
    plt.close()

def main():
    """Main function to run the Scrum Master assistant."""
    parser = argparse.ArgumentParser(description="ScrumGPT: AI Scrum Master Assistant")
    parser.add_argument("--event", type=str, required=True,
                      choices=['sprint_planning', 'daily_scrum', 'sprint_review', 'retrospective'],
                      help="Scrum event to facilitate")
    parser.add_argument("--team", type=str, required=True,
                      help="Team name")
    parser.add_argument("--sprint", type=int, required=True,
                      help="Sprint number")
    args = parser.parse_args()

    # Create event handler
    event_handlers = {
        'sprint_planning': SprintPlanning,
        'daily_scrum': DailyScrum,
        'sprint_review': SprintReview,
        'retrospective': Retrospective,
    }
    
    event = event_handlers[args.event](args.team, args.sprint)

    # Construct and run the society
    society = construct_society(event)
    answer, chat_history, token_count = run_society(society)

    # Save the output
    output = {
        'event': args.event,
        'team': args.team,
        'sprint': args.sprint,
        'timestamp': datetime.now().isoformat(),
        'summary': answer,
        'chat_history': chat_history,
    }
    
    output_file = os.path.join(event.output_dir, f"{args.event}_summary.json")
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    # Output the results
    print(f"\n=== {args.event.replace('_', ' ').title()} Summary ===")
    print(f"\033[94m{answer}\033[0m")
    print(f"\nOutput saved to: {output_file}")
    print(f"Total tokens used: {token_count}")


if __name__ == "__main__":
    main()
