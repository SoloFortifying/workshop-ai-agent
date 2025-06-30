# Interactive Agentic Applications Workshop - Vercel AI SDK Demo

This project demo is part of the Dynamous Community workshop on building interactive agentic applications! It demonstrates how to use the Vercel AI SDK to create a chat interface with an AI agent that can generate dynamic frontend components to display tool calling information in real time.

This is one of several examples in the workshop that showcase different approaches to building interactive AI applications:

- **This demo**: Vercel AI SDK with Claude 4 and tool usage
- **[CopilotKit with AG-UI](https://github.com/ag-ui-protocol/ag-ui/tree/cd6eb4860a7fc6e340f69fcac6f6126591db734d/dojo)**: A demonstration of the Agent-User Interaction Protocol
- **[Data Streaming Protocol Example](https://github.com/vercel-labs/ai-sdk-preview-python-streaming)**: Example using Vercel AI SDK with a Python backend

The other demos are not included in this repository - you can follow the links above to explore those projects and follow their respective README files to get started.

NOTE that the dojo/ folder was removed recently from the AG-UI repo for some reason. The link above takes you to a slightly older commit so be sure to download/clone the repo from there.

These examples highlight various approaches to building interactive, agentic applications with modern AI frameworks.

## About This Agentic Application

This app was built using the [Vercel AI SDK Claude 4 Guide](https://ai-sdk.dev/docs/guides/claude-4) as a starting point, but has been enhanced with a custom weather tool implementation and a significantly improved UI. This is still mostly for demo purposes, certainly check out Module 5 of the AI Agent Mastery course to dive into building a complete agentic application!

This app demonstrates:

1. **Vercel AI SDK Integration**: Using the AI SDK to create a streaming chat interface
2. **Tool Usage**: Implementation of a weather tool that Claude can invoke during conversation
3. **Streaming UI**: Real-time streaming of AI responses with a beautiful tool invocation visualization
4. **Reasoning Visibility**: Optional display of Claude's reasoning process

The main components include:

- `app/page.tsx`: The main chat interface with message display and input handling
- `app/weather.tsx`: A component for displaying weather information
- `app/api/chat/route.ts`: The API route that handles Claude 4 integration
- `lib/tools/get-weather.ts`: Implementation of the weather tool using the Open-Meteo API

## Getting Started

### Prerequisites

- Node.js installed on your machine
- An Anthropic API key (for Claude 4 access)

### Setup

1. Clone this repository
2. Install dependencies:

```bash
npm install
```

3. Create a `.env` file based on the provided `.env.example`:

```bash
cp .env.example .env
```

4. Add your Anthropic API key to the `.env` file:

```
ANTHROPIC_API_KEY=your_api_key_here
```

5. Start the development server:

```bash
npm run dev
```

6. Open [http://localhost:3000](http://localhost:3000) in your browser to see the application

## Learn More

- [Vercel AI SDK Documentation](https://ai-sdk.dev/docs) - Learn about the Vercel AI SDK features and API
- [AG-UI Protocol](https://docs.ag-ui.com/introduction) - The Agent-User Interaction Protocol for connecting AI agents to frontend applications
- [Data Streaming Protocol](https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol#data-stream-protocol) - Documentation for the data streaming protocol used in Vercel AI SDK

## Additional Resources

- [CopilotKit](https://www.copilotkit.ai/) - Framework for building AI copilots
- [CopilotKit Demo with AG-UI](https://github.com/ag-ui-protocol/ag-ui/tree/cd6eb4860a7fc6e340f69fcac6f6126591db734d/dojo) - Example implementation
- [Data Streaming Protocol example with Python backend](https://github.com/vercel-labs/ai-sdk-preview-python-streaming) - Example using Python backend
