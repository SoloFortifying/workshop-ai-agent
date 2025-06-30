# Graphiti Knowledge Graph Deep Dive Workshop

This workshop demonstrates the power of Graphiti, a temporal knowledge graph solution that enables AI agents to maintain and query evolving knowledge over time. The workshop includes multiple demonstrations ranging from basic knowledge graph operations to advanced AI-powered code exploration.

## Overview

This workshop includes six main components:

1. **Quickstart Example (`demo_quickstart.py`)**: A comprehensive tutorial demonstrating Graphiti's core features using episodes.
2. **Triplet Demo (`demo_triplets.py`)**: A deterministic demonstration using manual triplet creation for complex AI ecosystem relationships.
3. **LLM Evolution Demo (`demo_llm_evolution.py`)**: A simulation showing how knowledge evolves over time, with three phases of LLM development that update the knowledge graph.
4. **Agent Interface (`agent.py`)**: A conversational agent powered by Pydantic AI that can search and query the Graphiti knowledge graph.
5. **Code Repository Parser (`parse_repo_into_neo4j.py`)**: Direct Neo4j extraction tool that creates code structure graphs without LLM processing.
6. **LLM Code Explorer (`llm_code_explorer.py`)**: AI-powered code exploration that uses OpenAI to intelligently navigate repositories.

## Prerequisites

- Python 3.10 or higher
- Neo4j 5.26 or higher (for storing the knowledge graph)
- OpenAI API key (for LLM inference and embedding)

## Installation

### 1. Set up a virtual environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up Neo4j

You have a couple easy options for setting up Neo4j:

#### Option A: Using Local-AI-Packaged (Simplified setup)
1. Clone the repository: `git clone https://github.com/coleam00/local-ai-packaged`
2. Follow the installation instructions to set up Neo4j through the package
3. Note the username and password you set in .env and the URI will be bolt://localhost:7687

#### Option B: Using Neo4j Desktop
1. Download and install [Neo4j Desktop](https://neo4j.com/download/)
2. Create a new project and add a local DBMS
3. Start the DBMS and set a password
4. Note the connection details (URI, username, password)

### 4. Configure environment variables

Create a `.env` file in the project root with the following variables:

```
# Neo4j Connection
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# OpenAI API
OPENAI_API_KEY=your_openai_api_key
MODEL_CHOICE=gpt-4.1-mini  # Or another OpenAI model
```

## Running the Demo

### 1. Run the Quickstart Example

To get familiar with Graphiti's core features using episodes:

```bash
python demo_quickstart.py
```

This will demonstrate:
- Adding episodes to the knowledge graph
- Performing basic searches
- Using center node search for context-aware results
- Utilizing search recipes for node retrieval

⚠️ **Note: This demo clears existing graph data at startup**

### 2. Run the Triplet Demo

To see deterministic knowledge graph creation using manual triplets:

```bash
python demo_triplets.py
```

This demonstrates:
- Creating complex AI ecosystem relationships
- Manual node and edge creation
- Multi-hop relationship queries
- Different search strategies with focal points
- Company-product-leader interconnections in the AI space

⚠️ **Note: This demo clears existing graph data at startup**

### 3. Experience the Power of Temporal Knowledge

To see how knowledge evolves over time, run the LLM evolution demo in one terminal:

```bash
python demo_llm_evolution.py
```

⚠️ **Note: This demo clears existing graph data at startup**

This interactive demo will:
1. Add information about current top LLMs (Gemini, Claude, GPT-4.1)
2. Update the knowledge graph when Claude 4 emerges as the best LLM
3. Update again when MLMs make traditional LLMs obsolete

The script will pause between phases, allowing you to interact with the agent to see how its knowledge changes.

### 4. Interact with the Agent

In a separate terminal, run the agent interface:

```bash
python agent.py
```

This will start a conversational interface where you can:
1. Ask questions about LLMs
2. See the agent retrieve information from the knowledge graph
3. Experience how the agent's responses change as the knowledge graph evolves

### 5. Code Repository Analysis

Extract code structure directly into Neo4j without LLM processing:

```bash
python parse_repo_into_neo4j.py
```

This tool:
- Clones GitHub repositories
- Parses Python files using AST
- Creates nodes for files, classes, methods, functions
- Establishes import relationships
- Provides lightning-fast structural analysis

### 6. AI-Powered Code Exploration

Use OpenAI to intelligently explore code repositories:

```bash
python llm_code_explorer.py
```

Or use the convenient function:
```python
import asyncio
from llm_code_explorer import ask_codebase

# Ask questions about your codebase
await ask_codebase("How do I create an OpenAI model instance?")
```

This demonstrates:
- Intelligent file selection based on user questions
- Deep code exploration using graph relationships
- LLM-synthesized answers with code examples
- Repository navigation guidance

## Demo Workflows

### Basic Knowledge Graph Workflow

1. Start with `python demo_quickstart.py` to understand episodes
2. Run `python demo_triplets.py` to see manual triplet creation
3. Compare the different approaches and their use cases

⚠️ **Important**: Each demo clears the graph data when it starts, so run them separately.

### Temporal Knowledge Evolution Workflow

1. In Terminal 1: Run `python demo_llm_evolution.py` and complete Phase 1
2. In Terminal 2: Run `python agent.py` and ask "Which is the best LLM?"
3. In Terminal 1: Continue to Phase 2 by typing "continue"
4. In Terminal 2: Ask the same question again to see the updated knowledge
5. In Terminal 1: Continue to Phase 3
6. In Terminal 2: Ask "Are LLMs still relevant?" to see the final evolution

⚠️ **Important**: The `demo_llm_evolution.py` script clears graph data at startup, so don't run other demos while using this workflow.

### Code Analysis Workflow

1. Run `python parse_repo_into_neo4j.py` to extract repository structure
2. Use `python llm_code_explorer.py` to ask questions about the code
3. Compare structural vs. semantic code understanding

These workflows demonstrate how Graphiti maintains temporal knowledge and how responses adapt to changing knowledge graphs.

## Key Features

- **Temporal Knowledge**: Graphiti tracks when facts become valid and invalid
- **Hybrid Search**: Combines semantic similarity and BM25 text retrieval
- **Context-Aware Queries**: Reranks results based on graph distance
- **Structured Data Support**: Works with both text and JSON episodes
- **Manual Triplet Creation**: Direct control over knowledge graph structure
- **Code Repository Analysis**: Extract and analyze code structure at scale
- **AI-Powered Exploration**: Intelligent navigation of complex codebases
- **Multi-Modal Integration**: Episodes, triplets, and direct Neo4j operations
- **Easy Integration**: Seamlessly works with Pydantic AI for agent development

## Use Cases Demonstrated

- **Knowledge Management**: Building and maintaining evolving knowledge bases
- **Code Analysis**: Understanding large codebases through graph relationships
- **AI Agents**: Creating context-aware conversational interfaces
- **Temporal Reasoning**: Tracking how information changes over time
- **Hybrid Search**: Combining multiple search and ranking strategies
- **Domain Modeling**: Representing complex real-world relationships

## Additional Resources

- [Graphiti Documentation](https://help.getzep.com/graphiti/graphiti/overview)
- [Pydantic AI Documentation](https://ai.pydantic.dev/)
- [Neo4j Documentation](https://neo4j.com/docs/)
