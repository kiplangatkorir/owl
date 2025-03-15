# ScrumGPT: AI-Powered Scrum Master Assistant

## Overview
ScrumGPT is an intelligent Scrum Master assistant built using OWL's multi-agent collaboration framework. It helps teams manage their agile processes by facilitating Scrum events, tracking progress, and providing insights for continuous improvement.

## Features
- Sprint Planning Assistant
  - User story refinement
  - Sprint backlog organization
  - Capacity planning
- Daily Scrum Facilitator
  - Progress tracking
  - Impediment identification
  - Team collaboration insights
- Sprint Review Helper
  - Sprint goal achievement analysis
  - Demo preparation assistance
  - Stakeholder feedback collection
- Sprint Retrospective Guide
  - Team feedback analysis
  - Action item tracking
  - Continuous improvement suggestions
- Agile Metrics Dashboard
  - Burndown chart generation
  - Velocity tracking
  - Team health monitoring

## Requirements
camel-ai[all]==0.2.30
matplotlib>=3.7.1
pandas>=2.0.0
python-dotenv>=1.0.0
plotly>=5.18.0  # For interactive charts
dash>=2.14.0  # For metrics dashboard

## Setup

### 1. Install Ollama
First, install Ollama by following the instructions at [Ollama's website](https://ollama.ai/download).

### 2. Pull Required Models
```bash
# Pull the Qwen 72B model
ollama pull qwen2.5:72b
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Optional: Configure Tool Integrations
For JIRA integration (optional):
```
JIRA_API_TOKEN=your_token_here
```

## Usage

1. Start Ollama Server:
```bash
ollama serve
```

2. Run the assistant for different Scrum events:

Sprint Planning:
```bash
python scrumgpt.py --event sprint_planning --team alpha --sprint 23
```

Daily Scrum:
```bash
python scrumgpt.py --event daily_scrum --team alpha --sprint 23
```

Sprint Review:
```bash
python scrumgpt.py --event sprint_review --team alpha --sprint 23
```

Retrospective:
```bash
python scrumgpt.py --event retrospective --team alpha --sprint 23
```

## Example Commands
```bash
# Run Sprint Planning
python scrumgpt.py --event sprint_planning --team alpha --sprint 23

# Run Daily Scrum
python scrumgpt.py --event daily_scrum --team alpha --sprint 23

# Run Sprint Review
python scrumgpt.py --event sprint_review --team alpha --sprint 23

# Run Retrospective
python scrumgpt.py --event retrospective --team alpha --sprint 23
```

## How it Works
ScrumGPT uses OWL's:
- BrowserToolkit for accessing agile management tools
- DocumentProcessingToolkit for analyzing team documents
- FileWriteToolkit for generating reports
- CodeExecutionToolkit for metrics calculation
- MCPToolkit for structured interactions

## Model Configuration
The assistant uses the Qwen 72B model through Ollama with different configurations:
- User Agent: Higher temperature (0.7) for more creative responses
- Assistant Agent: Lower temperature (0.2) for more focused and consistent responses
- Document Processing: Balanced temperature (0.3) for analysis tasks

## Integration Options
- JIRA Software
- Azure DevOps
- Trello
- GitHub Projects

## Contributing
Feel free to contribute by:
1. Adding new Scrum event handlers
2. Improving metrics calculations
3. Adding integrations with other tools
4. Enhancing the AI's facilitation capabilities
