# Cloudflare Workers TypeScript API Deployment Guide

This guide demonstrates how to hyperscale AI agents using Cloudflare Workers and the OpenAI Agent SDK. Cloudflare Workers support Python but it is in beta, so we are using OpenAI's Agent SDK since they have a TypeScript version! 

Cloudflare Workers run your code at 300+ locations globally, so your AI agents are extremely responsive regardless of where your users are located.

The code above (in this folder) represents the complete example of this integration. However, this guide will walk you through creating everything from scratch, starting with a simple API and then adding OpenAI agent functionality.

## Prerequisites
- Node.js installed on your machine
- A Cloudflare account (free tier works)
- OpenAI API Key

## Step 1: Install Wrangler CLI
```bash
npm install -g wrangler
```

## Step 2: Authenticate with Cloudflare
```bash
wrangler login
```
This opens your browser to authenticate with your Cloudflare account.

## Step 3: Create a new Worker project
```bash
mkdir cloudflare-agent-api
cd cloudflare-agent-api
wrangler init
```
When prompted:
- Choose "Hello World" 
- Select the Worker template (first option listed)
- Select "TypeScript" for the language
- Choose "Yes" to use git

## Step 4: Update your TypeScript API endpoint
Replace the contents of your `src/index.ts` file with:

```typescript
/**
 * Simple API endpoint for Cloudflare Workers
 */

interface ApiResponse {
  message: string;
  timestamp: string;
  method: string;
  path: string;
  userAgent?: string;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    
    // Simple test endpoint
    if (url.pathname === '/api/test' && request.method === 'GET') {
      const response: ApiResponse = {
        message: 'Hello from Cloudflare Workers with TypeScript!',
        timestamp: new Date().toISOString(),
        method: request.method,
        path: url.pathname,
        userAgent: request.headers.get('User-Agent') || undefined
      };

      return new Response(JSON.stringify(response, null, 2), {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        }
      });
    }

    // Health check endpoint
    if (url.pathname === '/health' && request.method === 'GET') {
      return new Response(JSON.stringify({
        status: 'healthy',
        timestamp: new Date().toISOString()
      }), {
        headers: {
          'Content-Type': 'application/json'
        }
      });
    }

    // Handle OPTIONS for CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        }
      });
    }
    
    // 404 for all other routes
    return new Response(JSON.stringify({
      error: 'Not Found',
      availableEndpoints: [
        'GET /api/test',
        'GET /health'
      ]
    }), { 
      status: 404,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }
} satisfies ExportedHandler<Env>;
```

## Step 5: Test locally
```bash
npm run dev
```
Your API will be available at:
- `http://localhost:8787/api/test` - Main test endpoint
- `http://localhost:8787/health` - Health check

## Step 6: Test your endpoints locally

### Test the GET endpoint:
```bash
curl http://localhost:8787/api/test
```

### Test the health endpoint:
```bash
curl http://localhost:8787/health
```

## Step 7: Deploy to Cloudflare
```bash
npm run deploy
```

## Step 8: Test your deployed API
After deployment, your API will be available at a URL like:
`https://my-api.your-subdomain.workers.dev`

Test the deployed endpoints:
```bash
# Test endpoint
curl https://my-api.your-subdomain.workers.dev/api/test

# Health check
curl https://my-api.your-subdomain.workers.dev/health
```

## Step 9: Add OpenAI Agents Integration

Now let's add OpenAI agents to create a more powerful API.

### Install OpenAI Agents
```bash
npm install @openai/agents
```

### Update wrangler.jsonc for Node.js compatibility
Add the Node.js compatibility flag to your `wrangler.jsonc`:

```json
{
  "name": "my-api",
  "main": "src/index.ts",
  "compatibility_date": "2024-06-27",
  "compatibility_flags": ["nodejs_compat"]
}
```

### Create Agents File
Create a new file `src/agents.ts`:

```typescript
import { Agent, tool } from '@openai/agents';
import { z } from 'zod';

const historyFunFact = tool({
  name: 'history_fun_fact',
  description: 'Give a fun fact about a historical event',
  parameters: z.object({}),
  execute: async () => {
    return 'Sharks are older than trees.';
  },
});

export const historyTutorAgent = new Agent({
  name: 'History Tutor',
  instructions: 'You provide assistance with historical queries. Explain important events and context clearly.',
  model: 'gpt-4.1-mini',
  tools: [historyFunFact],
});

export const mathTutorAgent = new Agent({
  name: 'Math Tutor',
  instructions: 'You provide help with math problems. Explain your reasoning at each step and include examples',
  model: 'gpt-4.1-mini',
});

export const triageAgent = new Agent({
  name: 'Triage Agent',
  instructions: "You determine which agent to use based on the user's homework question",
  model: 'gpt-4.1-mini',
  handoffs: [historyTutorAgent, mathTutorAgent],
});
```

### Add OpenAI API Key Secret
```bash
wrangler secret put OPENAI_API_KEY
```

You'll be prompted to enter your OpenAI API key. This is encrypted and never stored in your code.

### Update TypeScript Types
Update your type definitions to include the OpenAI API key. Add this interface to your `src/index.ts`:

```typescript
interface Env {
  // Secrets (from wrangler secret put)
  OPENAI_API_KEY: string;
}
```

### For Local Development
Create a `.dev.vars` file in your project root:

```
OPENAI_API_KEY=sk-your-local-openai-api-key
```

Add `.dev.vars` to your `.gitignore` file:
```
.dev.vars
node_modules/
dist/
```

### Replace index.ts with OpenAI Integration
Replace the entire contents of your `src/index.ts` file with:

```typescript
/**
 * Simple API endpoint for Cloudflare Workers with OpenAI Agents
 */

import { run, setDefaultOpenAIKey } from '@openai/agents';
import { triageAgent } from './agents';

interface ApiResponse {
	message: string;
	timestamp: string;
	method: string;
	path: string;
	userAgent?: string;
  }

interface AgentRequest {
	message: string;
	streaming?: boolean;
  }

interface AgentResponse {
	output: string;
	agent: string;
	timestamp: string;
  }

interface Env {
  // Secrets (from wrangler secret put)
  OPENAI_API_KEY: string;
}
  
  export default {
	async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
	  const url = new URL(request.url);
	  
	  // Simple test endpoint
	  if (url.pathname === '/api/test' && request.method === 'GET') {
		const response: ApiResponse = {
		  message: 'Hello from Cloudflare Workers with TypeScript!',
		  timestamp: new Date().toISOString(),
		  method: request.method,
		  path: url.pathname,
		  userAgent: request.headers.get('User-Agent') || undefined
		};
  
		return new Response(JSON.stringify(response, null, 2), {
		  headers: {
			'Content-Type': 'application/json',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
			'Access-Control-Allow-Headers': 'Content-Type, Authorization'
		  }
		});
	  }
  
	  // Health check endpoint
	  if (url.pathname === '/health' && request.method === 'GET') {
		return new Response(JSON.stringify({
		  status: 'healthy',
		  timestamp: new Date().toISOString()
		}), {
		  headers: {
			'Content-Type': 'application/json'
		  }
		});
	  }

	  // Handle POST request to /api/agent
	  if (url.pathname === '/api/agent' && request.method === 'POST') {
		try {
		  let body: AgentRequest;
		  try {
			body = await request.json();
		  } catch (jsonError) {
			return new Response(JSON.stringify({
			  error: 'Invalid JSON in request body'
			}), {
			  status: 400,
			  headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*'
			  }
			});
		  }
		  
		  const { message, streaming = false } = body;
		  
		  if (!message) {
			return new Response(JSON.stringify({
			  error: 'Message is required'
			}), {
			  status: 400,
			  headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*'
			  }
			});
		  }

		  // Check if API key is configured
		  if (!env.OPENAI_API_KEY) {
			return new Response(JSON.stringify({
			  error: 'OpenAI API key not configured'
			}), {
			  status: 500,
			  headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*'
			  }
			});
		  }

		  // Set the API key for the OpenAI SDK
		  setDefaultOpenAIKey(env.OPENAI_API_KEY);

		  if (streaming) {
			// Handle streaming response
			const encoder = new TextEncoder();
			const streamResult = await run(triageAgent, message, { stream: true });
			
			const readable = new ReadableStream({
			  async start(controller) {
				try {
				  for await (const event of streamResult) {
					if (event.type === 'run_item_stream_event') {
					  const item = event.item;
					  if ('content' in item && typeof item.content === 'string') {
						const data = JSON.stringify({
						  type: 'text',
						  content: item.content,
						  timestamp: new Date().toISOString()
						});
						controller.enqueue(encoder.encode(`data: ${data}\n\n`));
					  }
					} else if (event.type === 'agent_updated_stream_event') {
					  const data = JSON.stringify({
						type: 'handoff',
						agent: event.agent.name,
						timestamp: new Date().toISOString()
					  });
					  controller.enqueue(encoder.encode(`data: ${data}\n\n`));
					}
				  }
				  controller.enqueue(encoder.encode('data: [DONE]\n\n'));
				  controller.close();
				} catch (error) {
				  controller.error(error);
				}
			  }
			});

			return new Response(readable, {
			  headers: {
				'Content-Type': 'text/event-stream',
				'Cache-Control': 'no-cache',
				'Connection': 'keep-alive',
				'Access-Control-Allow-Origin': '*'
			  }
			});
		  } else {
			// Handle non-streaming response
			const result = await run(triageAgent, message);
			
			const response: AgentResponse = {
			  output: result.finalOutput || '',
			  agent: triageAgent.name,
			  timestamp: new Date().toISOString()
			};

			return new Response(JSON.stringify(response, null, 2), {
			  headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*'
			  }
			});
		  }
		} catch (error) {
		  console.error('Agent error:', error);
		  return new Response(JSON.stringify({
			error: 'Failed to process agent request',
			details: error instanceof Error ? error.message : 'Unknown error'
		  }), {
			status: 500,
			headers: {
			  'Content-Type': 'application/json',
			  'Access-Control-Allow-Origin': '*'
			}
		  });
		}
	  }
  
	  // Handle OPTIONS for CORS preflight
	  if (request.method === 'OPTIONS') {
		return new Response(null, {
		  headers: {
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
			'Access-Control-Allow-Headers': 'Content-Type, Authorization'
		  }
		});
	  }
	  
	  // 404 for all other routes
	  return new Response(JSON.stringify({
		error: 'Not Found',
		availableEndpoints: [
		  'GET /api/test',
		  'GET /health',
		  'POST /api/agent'
		]
	  }), { 
		status: 404,
		headers: {
		  'Content-Type': 'application/json'
		}
	  });
	}
  } satisfies ExportedHandler<Env>;
```

## Step 10: Test locally with OpenAI integration
```bash
npm run dev
```

### Test the basic endpoints:
```bash
# Test endpoint
curl http://localhost:8787/api/test

# Health check
curl http://localhost:8787/health
```

### Test the new agent endpoint:
```bash
# Non-streaming request
curl -X POST http://localhost:8787/api/agent \
  -H "Content-Type: application/json" \
  -d '{"message": "What is 2 + 2?"}'

# Streaming request
curl -X POST http://localhost:8787/api/agent \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about the American Revolution", "streaming": true}'
```

## Step 11: Deploy with OpenAI integration
```bash
npm run deploy
```

**Note:** Secrets persist across deployments - you only need to set them once (or when values change).

## Step 12: Test your deployed OpenAI API
Test the deployed endpoints:

```bash
# Basic endpoints
curl https://my-api.your-subdomain.workers.dev/api/test
curl https://my-api.your-subdomain.workers.dev/health

# Agent endpoints
curl -X POST https://my-api.your-subdomain.workers.dev/api/agent \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the square root of 144?"}'

curl -X POST https://my-api.your-subdomain.workers.dev/api/agent \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about World War II", "streaming": true}'
```

## Project Structure
Your final project should look like this:
```
my-api/
├── src/
│   ├── index.ts
│   └── agents.ts
├── wrangler.jsonc
├── package.json
├── .dev.vars (don't commit)
├── .gitignore
└── node_modules/
```

## Next Steps
- Customize your agents for specific use cases
- Add more sophisticated tools and functions
- Implement authentication if required
- Add error handling and logging
- Set up custom domains in Cloudflare dashboard
- Add KV storage or D1 database bindings if needed

Your TypeScript API with OpenAI Agents is now deployed and running on Cloudflare's global edge network!