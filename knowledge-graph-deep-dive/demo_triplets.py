"""
Copyright 2025, Zep Software, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import asyncio
import logging
import os
import uuid
from datetime import datetime, timezone
from logging import INFO

from dotenv import load_dotenv

from graphiti_core import Graphiti
from graphiti_core.edges import EntityEdge
from graphiti_core.nodes import EntityNode
from graphiti_core.utils.maintenance.graph_data_operations import clear_data

#################################################
# CONFIGURATION
#################################################
# Set up logging and environment variables for
# connecting to Neo4j database
#################################################

# Configure logging
logging.basicConfig(
    level=INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)

load_dotenv()

# Neo4j connection parameters
# Make sure Neo4j Desktop is running with a local DBMS started
neo4j_uri = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
neo4j_user = os.environ.get('NEO4J_USER', 'neo4j')
neo4j_password = os.environ.get('NEO4J_PASSWORD', 'password')

if not neo4j_uri or not neo4j_user or not neo4j_password:
    raise ValueError('NEO4J_URI, NEO4J_USER, and NEO4J_PASSWORD must be set')


async def main():
    #################################################
    # INITIALIZATION
    #################################################
    # Connect to Neo4j and set up Graphiti indices
    # This is required before using other Graphiti
    # functionality
    #################################################

    # Initialize Graphiti with Neo4j connection
    graphiti = Graphiti(neo4j_uri, neo4j_user, neo4j_password)

    try:
        # Initialize the graph database with graphiti's indices. This only needs to be done once.
        await graphiti.build_indices_and_constraints()

        # Clear existing data
        print("Clearing existing graph data...")
        await clear_data(graphiti.driver)
        print("Graph data cleared successfully.")        

        #################################################
        # CREATING TRIPLETS
        #################################################
        # Instead of using episodes, we'll manually create
        # triplets (node-edge-node relationships) for a
        # more deterministic demonstration
        #################################################

        print("Creating complex knowledge graph triplets...")

        # Create UUIDs for all entities
        claude_uuid = str(uuid.uuid4())
        anthropic_uuid = str(uuid.uuid4())
        gpt4_uuid = str(uuid.uuid4())
        openai_uuid = str(uuid.uuid4())
        gemini_uuid = str(uuid.uuid4())
        google_uuid = str(uuid.uuid4())
        dario_uuid = str(uuid.uuid4())
        sam_uuid = str(uuid.uuid4())
        sundar_uuid = str(uuid.uuid4())
        llama_uuid = str(uuid.uuid4())
        meta_uuid = str(uuid.uuid4())
        mark_uuid = str(uuid.uuid4())
        constitutional_ai_uuid = str(uuid.uuid4())
        transformer_uuid = str(uuid.uuid4())
        attention_uuid = str(uuid.uuid4())

        # Create AI Assistant nodes
        claude_node = EntityNode(
            uuid=claude_uuid,
            name="Claude",
            summary="Constitutional AI assistant developed by Anthropic with advanced reasoning capabilities",
            group_id="ai_demo"
        )

        gpt4_node = EntityNode(
            uuid=gpt4_uuid,
            name="GPT-4",
            summary="Large multimodal language model developed by OpenAI with 175B+ parameters",
            group_id="ai_demo"
        )

        gemini_node = EntityNode(
            uuid=gemini_uuid,
            name="Gemini",
            summary="Google's family of multimodal large language models designed to be flexible and efficient",
            group_id="ai_demo"
        )

        llama_node = EntityNode(
            uuid=llama_uuid,
            name="LLaMA",
            summary="Meta's Large Language Model trained on diverse text data with open-source variants",
            group_id="ai_demo"
        )

        # Create Company nodes
        anthropic_node = EntityNode(
            uuid=anthropic_uuid,
            name="Anthropic",
            summary="AI safety company founded in 2021 focused on developing safe, beneficial AI systems",
            group_id="ai_demo"
        )

        openai_node = EntityNode(
            uuid=openai_uuid,
            name="OpenAI",
            summary="AI research company founded in 2015 focused on ensuring AGI benefits all of humanity",
            group_id="ai_demo"
        )

        google_node = EntityNode(
            uuid=google_uuid,
            name="Google",
            summary="Technology company with advanced AI research division Google DeepMind",
            group_id="ai_demo"
        )

        meta_node = EntityNode(
            uuid=meta_uuid,
            name="Meta",
            summary="Social media and technology company with significant AI research investments",
            group_id="ai_demo"
        )

        # Create Person nodes
        dario_node = EntityNode(
            uuid=dario_uuid,
            name="Dario Amodei",
            summary="CEO and co-founder of Anthropic, formerly VP of Research at OpenAI",
            group_id="ai_demo"
        )

        sam_node = EntityNode(
            uuid=sam_uuid,
            name="Sam Altman",
            summary="CEO of OpenAI, entrepreneur and investor in AI technology",
            group_id="ai_demo"
        )

        sundar_node = EntityNode(
            uuid=sundar_uuid,
            name="Sundar Pichai",
            summary="CEO of Google and Alphabet, oversees Google's AI initiatives",
            group_id="ai_demo"
        )

        mark_node = EntityNode(
            uuid=mark_uuid,
            name="Mark Zuckerberg",
            summary="CEO and founder of Meta, driving the company's AI and metaverse strategy",
            group_id="ai_demo"
        )

        # Create Technology/Concept nodes
        constitutional_ai_node = EntityNode(
            uuid=constitutional_ai_uuid,
            name="Constitutional AI",
            summary="AI training methodology that uses a set of principles to guide model behavior",
            group_id="ai_demo"
        )

        transformer_node = EntityNode(
            uuid=transformer_uuid,
            name="Transformer Architecture",
            summary="Neural network architecture that revolutionized natural language processing",
            group_id="ai_demo"
        )

        attention_node = EntityNode(
            uuid=attention_uuid,
            name="Attention Mechanism",
            summary="Key component of transformer models that allows focusing on relevant parts of input",
            group_id="ai_demo"
        )

        # Create comprehensive edge relationships
        edges = [
            # Company-Product relationships
            EntityEdge(group_id="ai_demo", source_node_uuid=claude_uuid, target_node_uuid=anthropic_uuid,
                      created_at=datetime.now(timezone.utc), name="DEVELOPED_BY", fact="Claude is developed by Anthropic"),
            EntityEdge(group_id="ai_demo", source_node_uuid=gpt4_uuid, target_node_uuid=openai_uuid,
                      created_at=datetime.now(timezone.utc), name="DEVELOPED_BY", fact="GPT-4 is developed by OpenAI"),
            EntityEdge(group_id="ai_demo", source_node_uuid=gemini_uuid, target_node_uuid=google_uuid,
                      created_at=datetime.now(timezone.utc), name="DEVELOPED_BY", fact="Gemini is developed by Google"),
            EntityEdge(group_id="ai_demo", source_node_uuid=llama_uuid, target_node_uuid=meta_uuid,
                      created_at=datetime.now(timezone.utc), name="DEVELOPED_BY", fact="LLaMA is developed by Meta"),
            
            # Leadership relationships
            EntityEdge(group_id="ai_demo", source_node_uuid=dario_uuid, target_node_uuid=anthropic_uuid,
                      created_at=datetime.now(timezone.utc), name="CEO_OF", fact="Dario Amodei is the CEO of Anthropic"),
            EntityEdge(group_id="ai_demo", source_node_uuid=sam_uuid, target_node_uuid=openai_uuid,
                      created_at=datetime.now(timezone.utc), name="CEO_OF", fact="Sam Altman is the CEO of OpenAI"),
            EntityEdge(group_id="ai_demo", source_node_uuid=sundar_uuid, target_node_uuid=google_uuid,
                      created_at=datetime.now(timezone.utc), name="CEO_OF", fact="Sundar Pichai is the CEO of Google"),
            EntityEdge(group_id="ai_demo", source_node_uuid=mark_uuid, target_node_uuid=meta_uuid,
                      created_at=datetime.now(timezone.utc), name="CEO_OF", fact="Mark Zuckerberg is the CEO of Meta"),
            
            # Technology relationships
            EntityEdge(group_id="ai_demo", source_node_uuid=claude_uuid, target_node_uuid=constitutional_ai_uuid,
                      created_at=datetime.now(timezone.utc), name="USES_TECHNOLOGY", fact="Claude uses Constitutional AI methodology"),
            EntityEdge(group_id="ai_demo", source_node_uuid=gpt4_uuid, target_node_uuid=transformer_uuid,
                      created_at=datetime.now(timezone.utc), name="BASED_ON", fact="GPT-4 is based on Transformer architecture"),
            EntityEdge(group_id="ai_demo", source_node_uuid=gemini_uuid, target_node_uuid=transformer_uuid,
                      created_at=datetime.now(timezone.utc), name="BASED_ON", fact="Gemini is based on Transformer architecture"),
            EntityEdge(group_id="ai_demo", source_node_uuid=llama_uuid, target_node_uuid=transformer_uuid,
                      created_at=datetime.now(timezone.utc), name="BASED_ON", fact="LLaMA is based on Transformer architecture"),
            EntityEdge(group_id="ai_demo", source_node_uuid=transformer_uuid, target_node_uuid=attention_uuid,
                      created_at=datetime.now(timezone.utc), name="UTILIZES", fact="Transformer architecture utilizes attention mechanisms"),
            
            # Professional relationships
            EntityEdge(group_id="ai_demo", source_node_uuid=dario_uuid, target_node_uuid=openai_uuid,
                      created_at=datetime.now(timezone.utc), name="FORMER_VP_AT", fact="Dario Amodei was formerly VP of Research at OpenAI"),
            
            # Competitive relationships
            EntityEdge(group_id="ai_demo", source_node_uuid=claude_uuid, target_node_uuid=gpt4_uuid,
                      created_at=datetime.now(timezone.utc), name="COMPETES_WITH", fact="Claude competes with GPT-4 in the AI assistant market"),
            EntityEdge(group_id="ai_demo", source_node_uuid=gemini_uuid, target_node_uuid=gpt4_uuid,
                      created_at=datetime.now(timezone.utc), name="COMPETES_WITH", fact="Gemini competes with GPT-4 in the AI market"),
            
            # Innovation relationships
            EntityEdge(group_id="ai_demo", source_node_uuid=anthropic_uuid, target_node_uuid=constitutional_ai_uuid,
                      created_at=datetime.now(timezone.utc), name="PIONEERED", fact="Anthropic pioneered Constitutional AI methodology"),
        ]

        # Add all triplets to the graph
        triplets = [
            (claude_node, edges[0], anthropic_node),
            (gpt4_node, edges[1], openai_node),
            (gemini_node, edges[2], google_node),
            (llama_node, edges[3], meta_node),
            (dario_node, edges[4], anthropic_node),
            (sam_node, edges[5], openai_node),
            (sundar_node, edges[6], google_node),
            (mark_node, edges[7], meta_node),
            (claude_node, edges[8], constitutional_ai_node),
            (gpt4_node, edges[9], transformer_node),
            (gemini_node, edges[10], transformer_node),
            (llama_node, edges[11], transformer_node),
            (transformer_node, edges[12], attention_node),
            (dario_node, edges[13], openai_node),
            (claude_node, edges[14], gpt4_node),
            (gemini_node, edges[15], gpt4_node),
            (anthropic_node, edges[16], constitutional_ai_node),
        ]

        for i, (source, edge, target) in enumerate(triplets):
            print(f"Adding triplet {i+1}/17: {source.name} -> {target.name}")
            await graphiti.add_triplet(source, edge, target)

        #################################################
        # BASIC SEARCH
        #################################################
        # Search for information using the same queries
        # as the episode-based example
        #################################################

        # Perform multiple search queries to demonstrate the complex graph
        search_queries = [
            'Which AI assistant is from Anthropic?',
            'Who is the CEO of OpenAI?',
            'What technology does Claude use?',
            'Which models are based on Transformer architecture?',
            'Who used to work at OpenAI?'
        ]

        for query in search_queries:
            print(f"\nSearching for: '{query}'")
            results = await graphiti.search(query)

            print(f'\nSearch Results for "{query}":')
            for i, result in enumerate(results[:3]):  # Limit to top 3 results
                print(f'{i+1}. UUID: {result.uuid}')
                print(f'   Fact: {result.fact}')
                if hasattr(result, 'valid_at') and result.valid_at:
                    print(f'   Valid from: {result.valid_at}')
                if hasattr(result, 'invalid_at') and result.invalid_at:
                    print(f'   Valid until: {result.invalid_at}')
                print('   ---')

        #################################################
        # CENTER NODE SEARCH
        #################################################
        # For more contextually relevant results, you can
        # use a center node to rerank search results based
        # on their graph distance to a specific node
        #################################################

        # Demonstrate center node search with different focal points
        center_queries = [
            ('AI competition analysis', 'Who competes with whom in AI?', claude_uuid, 'Claude'),
            ('OpenAI connections', 'What connections does OpenAI have?', openai_uuid, 'OpenAI'),
            ('Transformer technology', 'What uses Transformer architecture?', transformer_uuid, 'Transformer Architecture'),
            ('Leadership analysis', 'Who leads AI companies?', dario_uuid, 'Dario Amodei')
        ]

        for description, query, center_uuid, center_name in center_queries:
            print(f'\n=== {description.upper()} ===')
            print(f'Query: "{query}"')
            print(f'Center Node: {center_name} ({center_uuid})')
            
            reranked_results = await graphiti.search(query, center_node_uuid=center_uuid)
            
            print(f'\nResults (reranked by distance from {center_name}):')
            for i, result in enumerate(reranked_results[:4]):  # Top 4 results
                print(f'{i+1}. {result.fact}')
            print()

        # Demonstrate multi-hop relationship queries
        print('\n=== MULTI-HOP RELATIONSHIP ANALYSIS ===')
        multi_hop_queries = [
            'How is Dario Amodei connected to Constitutional AI?',
            'What is the relationship between Meta and Transformer architecture?',
            'How are Google and attention mechanisms related?'
        ]
        
        for query in multi_hop_queries:
            print(f'\nQuery: "{query}"')
            results = await graphiti.search(query)
            for i, result in enumerate(results[:3]):
                print(f'{i+1}. {result.fact}')

    finally:
        #################################################
        # CLEANUP
        #################################################
        # Always close the connection to Neo4j when
        # finished to properly release resources
        #################################################

        # Close the connection
        await graphiti.close()
        print('\nConnection closed')


if __name__ == '__main__':
    asyncio.run(main())