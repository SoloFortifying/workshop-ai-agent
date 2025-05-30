import { anthropic, AnthropicProviderOptions } from '@ai-sdk/anthropic';
import { getWeather } from '@/lib/tools/get-weather';
import { streamText, generateText } from 'ai';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: anthropic('claude-4-sonnet-20250514'),
    messages,
    maxSteps: 5,
    headers: {
      'anthropic-beta': 'interleaved-thinking-2025-05-14',
    },
    tools: {
      getWeather
    },
    providerOptions: {
      anthropic: {
        thinking: { type: 'enabled', budgetTokens: 15000 },
      } satisfies AnthropicProviderOptions,
    },
  });

  return result.toDataStreamResponse({
    // sendReasoning: true,
  });
}