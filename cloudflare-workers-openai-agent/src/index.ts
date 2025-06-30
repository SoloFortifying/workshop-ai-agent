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
			  output: result.finalOutput || ''
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