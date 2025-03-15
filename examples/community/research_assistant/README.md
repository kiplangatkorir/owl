# ResearchGPT: Intelligent Research Assistant

## Overview
ResearchGPT is an intelligent research assistant built using OWL's multi-agent collaboration framework. It helps researchers streamline their literature review process by combining document processing, academic search, and content summarization capabilities.

## Features
- Academic paper search across multiple sources (ArXiv, Google Scholar, Semantic Scholar)
- PDF and document processing for research papers
- Automated summarization and key point extraction
- Visual representation of research findings
- Interactive Q&A about processed papers
- Citation management and export

## Requirements
```
camel-ai[all]==0.2.30
matplotlib>=3.7.1
networkx>=3.1
pandas>=2.0.0
```

## Usage
1. Set up your API keys in the `.env` file:
```
OPENAI_API_KEY=your_key_here
GOOGLE_SCHOLAR_API_KEY=your_key_here
```

2. Run the assistant:
```python
python research_assistant.py --query "quantum computing applications"
```

## Example Output
The assistant will:
1. Search for relevant papers
2. Generate summaries and extract key points
3. Create a knowledge graph of concepts
4. Provide an interactive Q&A session about the findings

## How it Works
ResearchGPT uses OWL's:
- ArxivToolkit for paper search
- DocumentProcessingToolkit for PDF analysis
- SearchToolkit for web searches
- NetworkXToolkit for knowledge graph visualization
- CodeExecutionToolkit for data processing

## Contributing
Feel free to suggest improvements or report issues!
