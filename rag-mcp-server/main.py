from sentence_transformers import CrossEncoder
from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from supabase import create_client, Client
from collections.abc import AsyncIterator
from typing import List, Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI
from pathlib import Path
import numpy as np
import asyncio
import logging
import signal
import sys
import os

# Load environment variables from the project root .env file
project_root = Path(__file__).resolve().parent
dotenv_path = project_root / '.env'
load_dotenv(dotenv_path, override=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Changed to DEBUG for more verbose logging
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log', mode='w'),
        logging.StreamHandler(sys.stdout)  # Explicitly use stdout
    ]
)
# Ensure all loggers are verbose
logging.getLogger().setLevel(logging.INFO)


logger = logging.getLogger('reranking_mcp')  # Use a more specific logger name

@dataclass
class RerankerContext:
    """Context for the Reranker MCP server."""
    model: CrossEncoder
    supabase: Client
    openai_client: OpenAI

@asynccontextmanager
async def reranker_lifespan(server: FastMCP) -> AsyncIterator[RerankerContext]:
    """Manages the Reranker model lifecycle.
    
    Args:
        server: The FastMCP server instance
        
    Yields:
        RerankerContext: The context containing the Reranker model, Supabase client, and OpenAI client
    """
    # Load the cross-encoder model
    model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    
    # Get Supabase URL and key from environment variables
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    supabase = create_client(supabase_url, supabase_key)

    # Create the OpenAI client for embeddings
    openai_api_key = os.getenv('OPENAI_API_KEY')    
    openai_client = OpenAI(api_key=openai_api_key)    

    try:
        yield RerankerContext(model=model, supabase=supabase, openai_client=openai_client)
    finally:
        # No cleanup needed in this case, just showing this is where you would do that for things like DB connections!
        pass

# Initialize FastMCP server with the Reranker model as context
mcp = FastMCP(
    "mcp-rag-with-reranker",
    description="MCP server for RAG with document reranking using cross-encoder models",
    lifespan=reranker_lifespan,
    host=os.getenv("HOST", "0.0.0.0"),
    port=os.getenv("PORT", "8050")
)

@mcp.tool()
async def search_and_rerank(ctx: Context, query: str, collection_name: str = "documents_reranking", match_count: int = 15, top_k: int = 15) -> str:
    """Search documents from Supabase and rerank them based on relevance to the query.

    This tool performs a two-step process:
    1. Retrieves relevant documents from Supabase using vector similarity search
    2. Reranks the retrieved documents using a cross-encoder model

    Args:
        ctx: The MCP server context containing the Supabase client, OpenAI client, and Reranker model
        query: The search query
        collection_name: Name of the Supabase collection to search in (default: "documents_reranking")
        match_count: Number of documents to retrieve from vector search 
        top_k: Number of top documents to return after reranking
    """
    try:
        logger.info(f"Processing search and rerank request - Query: {query}, Collection: {collection_name}, Match count: {match_count}, Top-k: {top_k}")
        
        # Get Supabase client and model from context
        supabase = ctx.request_context.lifespan_context.supabase
        model = ctx.request_context.lifespan_context.model
        openai_client = ctx.request_context.lifespan_context.openai_client
        
        try:
            # Generate query embedding using OpenAI
            response = openai_client.embeddings.create(
                input=query,
                model="text-embedding-3-small"
            )
            query_embedding = response.data[0].embedding
            
        except Exception as e:
            logger.error(f"Failed to generate embedding: {str(e)}")
            raise
        
        # Perform vector similarity search
        try:
            # Perform the vector search
            result = supabase.rpc(
                'match_documents_reranking',
                {
                    'query_embedding': query_embedding,
                    'match_count': match_count
                }
            ).execute()
                        
            if not result.data:
                logger.warning(f"No documents found in collection {collection_name}")
                return "No matching documents found"
                
            documents = [item['text'] for item in result.data]
            logger.info(f"Retrieved {len(documents)} documents from Supabase")
            
            # Pair each doc with the query for reranking
            pairs = [[query, doc] for doc in documents]
            
            # Predict relevance scores
            scores = model.predict(pairs)
            
            # Combine and sort results
            scored = [
                {"text": doc, "score": float(score)}
                for doc, score in zip(documents, scores)
            ]
            scored_sorted = sorted(scored, key=lambda x: x["score"], reverse=True)
            
            logger.info(f"Successfully reranked documents. Top score: {scored_sorted[0]['score'] if scored_sorted else 'N/A'}")
            return str(scored_sorted[:top_k])
            
        except Exception as e:
            logger.error(f"Error during Supabase search: {str(e)}")
            return f"Error searching documents: {str(e)}"
            
    except Exception as e:
        logger.error(f"Error during search and rerank: {str(e)}")
        return f"Error processing request: {str(e)}"

async def main():
    try:
        transport = os.getenv("TRANSPORT", "sse")
        if transport == 'sse':
            # Run the MCP server with sse transport
            await mcp.run_sse_async()
        else:
            # Run the MCP server with stdio transport
            await mcp.run_stdio_async()

    except KeyboardInterrupt:
        logger.info('Received keyboard interrupt, initiating shutdown...')
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        for task in tasks:
            task.cancel()
        logger.info(f'Cancelling {len(tasks)} outstanding tasks')
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info('Shutdown complete')
    except Exception as e:
        logger.error(f'Error running server: {str(e)}')
        raise

if __name__ == "__main__":
    asyncio.run(main())