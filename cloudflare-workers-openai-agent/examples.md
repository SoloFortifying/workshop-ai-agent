# OpenAI Agents API Examples

## Basic Usage (Non-streaming)

```bash
# Ask a history question
curl -X POST http://localhost:8787/api/agent \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the capital of France?"
  }'

# Ask a math question
curl -X POST http://localhost:8787/api/agent \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is 25 * 4?"
  }'
```

## Streaming Usage

```bash
# Stream the response
curl -X POST http://localhost:8787/api/agent \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain the French Revolution",
    "streaming": true
  }'
```

## JavaScript Client Example

```javascript
// Non-streaming request
async function askAgent(message) {
  const response = await fetch('http://localhost:8787/api/agent', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message })
  });
  
  const data = await response.json();
  console.log('Agent:', data.agent);
  console.log('Response:', data.output);
}

// Streaming request
async function streamAgent(message) {
  const response = await fetch('http://localhost:8787/api/agent', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message, streaming: true })
  });
  
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    const chunk = decoder.decode(value);
    const lines = chunk.split('\n').filter(line => line.trim() !== '');
    
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6);
        if (data === '[DONE]') {
          console.log('Stream ended');
        } else {
          const event = JSON.parse(data);
          if (event.type === 'text') {
            process.stdout.write(event.content);
          } else if (event.type === 'handoff') {
            console.log(`\n[Handed off to ${event.agent}]`);
          }
        }
      }
    }
  }
}
```

## Running the Development Server

```bash
# Start the Cloudflare Worker development server
npm run dev

# The API will be available at http://localhost:8787
```

## Environment Setup

Make sure your `.dev.vars` file contains:
```
OPENAI_API_KEY=your-openai-api-key
```

For production deployment, set the environment variable:
```bash
wrangler secret put OPENAI_API_KEY
```