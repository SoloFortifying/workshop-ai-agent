# RAG MCP Server with Search and Reranking

This MCP server provides complete RAG (Retrieval-Augmented Generation) capabilities with both vector search and document reranking using Supabase and cross-encoder models. It accepts a query, retrieves relevant documents from Supabase, and reranks them based on their relevance to the query. This is particularly useful to ensure that AI agents leveraging RAG understand which chunks are most worth paying attention to.

## Overview

The server combines two key RAG components in a single solution:

1. **Vector Search**: Uses OpenAI embeddings and Supabase vector storage to find relevant documents
2. **Document Reranking**: Uses the `cross-encoder/ms-marco-MiniLM-L-6-v2` model to rerank retrieved documents by relevance

It exposes a single tool that takes a query, performs vector search in Supabase, and returns the documents reranked by their relevance to the query.

## Prerequisites

- Python 3.12+
- OpenAI API key
- Supabase project

## Installation

1. Clone the repository

2. Set up a virtual environment:

   **Windows**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS/Linux**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Build Docker image (optional, can use Python directly):
   ```bash
   docker build -t rag-reranking-mcp-server .
   ```

## Available Tools

### search_and_rerank

Searches for documents in Supabase and reranks them based on their relevance to a query.

Parameters:
- `query`: The search query
- `collection_name`: Name of the Supabase collection to search in (default: "documents_reranking")
- `match_count`: Number of documents to retrieve from vector search (default: 15)
- `top_k`: Number of top documents to return after reranking (default: 15)

Returns:
A list of the top-k documents with their relevance scores, sorted by score in descending order.

## Environment Variables

Create a `.env` file with the following variables:

```env
HOST=0.0.0.0
PORT=8050
TRANSPORT=sse

# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_role_key

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
```

Note if hosting Supabase yourself: For Docker, use `http://host.docker.internal:8000` as the Supabase URL. For local development, use your actual Supabase URL.

## Running the Server

### Using Python

```bash
python main.py
```

The server will start on the default port (8050) or the port specified in your .env file.

### Using Docker

```bash
docker run --rm -i -p 8050:8050 --env-file=.env rag-reranking-mcp-server
```

## Integration with MCP Clients

### SSE Configuration

Once you have the server running with SSE transport (default), you can connect to it using this configuration:

```json
{
  "mcpServers": {
    "rag-search-reranking": {
      "transport": "sse",
      "url": "http://localhost:8050/sse"
    }
  }
}
```

> **Note for Windsurf users**: Use `serverUrl` instead of `url` in your configuration:
> ```json
> {
>   "mcpServers": {
>     "rag-search-reranking": {
>       "transport": "sse",
>       "serverUrl": "http://localhost:8050/sse"
>     }
>   }
> }
> ```
>
> **Note for Docker users**: Use `host.docker.internal` instead of `localhost` if your client is running in a different container.

### Stdio Configuration

To use the server with stdio transport, add this configuration to your MCP client:

```json
{
  "mcpServers": {
    "rag-search-reranking": {
      "command": "python",
      "args": ["path/to/rag-mcp-server/main.py"],
      "env": {
        "TRANSPORT": "stdio",
        "OPENAI_API_KEY": "your_openai_api_key",
        "SUPABASE_URL": "your_supabase_url",
        "SUPABASE_KEY": "your_supabase_key"
      }
    }
  }
}
```