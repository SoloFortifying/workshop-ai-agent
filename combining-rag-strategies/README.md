# Dynamous Workshop - Combining RAG Strategies

This n8n workflow implements a powerful Retrieval-Augmented Generation (RAG) system that integrates three key strategies: Query Expansion, Agentic RAG, and Contextual Retrieval. Together, these approaches create a more accurate and intelligent document retrieval and response generation system.

I would also love to build this same AI Agent in Python for a future workshop! Just wanted to start with n8n since it is much easier to visualize and build out step by step.

## Key Components

### 1. Query Expansion
- Dedicated AI agent expands user queries to be more complete and specific
- Enhanced queries improve downstream document retrieval quality
- Agent outputs only questions, which feed into the main RAG pipeline

### 2. Agentic RAG
- AI agent intelligently selects and uses multiple retrieval tools
- Can perform iterative searches, analyzing and refining based on initial results
- Tools include vector similarity search, document metadata lookup, and full document extraction
- Enables more sophisticated knowledge traversal and connection-making

### 3. Contextual Retrieval
- Each document chunk is enhanced with contextual information before embedding
- "Generate Contextual Text" node creates context that situates each chunk within the larger document
- Preserves critical relationships and context that would otherwise be lost in traditional chunking
- Significantly improves retrieval accuracy by maintaining document coherence

## Technical Implementation
- Automatic document processing from Google Drive
- Supabase with pgvector for vector storage and retrieval
- OpenAI for the LLMs, taking advantage of automatic prompt caching for GPT models to make the contextual retrieval way less expensive.

## Performance Benefits
- More coherent responses that understand document relationships
- Reduced hallucinations through better contextual understanding
- Faster and more relevant answers with less query refinement

## Ideal Use Cases
- Complex information retrieval across multiple documents
- Specialized domains requiring deep contextual understanding
- Research and analysis connecting related concepts

## Why Combine these Strategies?

This integrated approach demonstrates that combining multiple RAG strategies creates a system more powerful than the sum of its parts, significantly advancing the state-of-the-art in knowledge retrieval and generation.