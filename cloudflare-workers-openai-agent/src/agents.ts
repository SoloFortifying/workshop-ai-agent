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
  tools: [historyFunFact],
});

export const mathTutorAgent = new Agent({
  name: 'Math Tutor',
  instructions: 'You provide help with math problems. Explain your reasoning at each step and include examples',
});

export const triageAgent = new Agent({
  name: 'Triage Agent',
  instructions: "You determine which agent to use based on the user's homework question",
  handoffs: [historyTutorAgent, mathTutorAgent],
});