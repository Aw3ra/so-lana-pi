import { Router } from 'itty-router';
import { transcribe, chat } from './openai/response.js';
import { get_messages } from './supabase/database.js';

// now let's create a router (note the lack of "new")
const router = Router();

// GET collection index
router.get('/api/todos', () => new Response('Todos Index!'));

// GET item
router.get('/api/todos/:id', ({ params }) => new Response(`Todo #${params.id}`));

router.get('/api/lanaactive', () => new Response('Lana is Live!'));

// POST to the collection (we'll use async here)
router.post('/api/lanaresponse', async (request, env) => {
    if (request.method !== "POST") {
		return new Response("Please POST an audio file.", { status: 420 });
	  }
	  console.log(env);
	  const audio_text = await transcribe(request, env.OPENAI_API_KEY);
	  let messages = await get_messages("awera", env.SUPABASE_KEY, env.DB);
	  messages.push(audio_text);  
	  messages.push({role: "assistant", content: await chat(messages, env.OPENAI_API_KEY)});
	  // Return the messages array as a JSON object
	  return new Response(JSON.stringify(messages), { status: 200, headers: { 'Content-Type': 'application/json' } });
});

// 404 for everything else
router.all('*', () => new Response('Not Found.', { status: 404 }));

export default router;
