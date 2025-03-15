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
```
camel-ai[all]==0.2.30
matplotlib>=3.7.1
pandas>=2.0.0
python-dotenv>=1.0.0
jira>=3.5.1  # Optional: For JIRA integration
```

## Usage
1. Set up your environment:
```bash
pip install -r requirements.txt
```

2. Configure your settings in `.env`:
```
OPENAI_API_KEY=your_key_here
JIRA_API_TOKEN=your_token_here  # Optional
```

3. Run the assistant:
```python
python scrumgpt.py --event "sprint_planning" --team "alpha" --sprint "23"
```

## Example Commands
- Sprint Planning: `python scrumgpt.py --event sprint_planning --team alpha --sprint 23`
- Daily Scrum: `python scrumgpt.py --event daily_scrum --team alpha --sprint 23`
- Sprint Review: `python scrumgpt.py --event sprint_review --team alpha --sprint 23`
- Retrospective: `python scrumgpt.py --event retrospective --team alpha --sprint 23`

## How it Works
ScrumGPT uses OWL's:
- BrowserToolkit for accessing agile management tools
- DocumentProcessingToolkit for analyzing team documents
- FileWriteToolkit for generating reports
- CodeExecutionToolkit for metrics calculation
- MCPToolkit for structured interactions

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
