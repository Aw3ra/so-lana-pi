import { Router } from 'itty-router';
import { transcribe, chat } from './openai/response.js';
import { get_messages, add_message } from './supabase/database.js';
import { get_balance } from './commands/modules/crypto.js';
import { handle_function } from './commands/handler.js';

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
	//Get the text from the audio file sent in the POST request
	const audio_text = await transcribe(request, env.OPENAI_API_KEY);
	//Get the messages from the database
	let messages = await get_messages("awera", env.SUPABASE_KEY, env.DB);
	//Add the audio text to the messages array
	messages.push(audio_text);  
	//Retrieve the assistant message from OpenAI and add it to the messages array
	let assistant_response = await chat(messages, env.OPENAI_API_KEY);
	const finish_reason = assistant_response.choices[0].finish_reason;
	// If the response is a dictionary, it is a command
	let new_messages = [];
	if (finish_reason === "function_call") {
		// Handle the function, and return an array of messages
		const response = await handle_function(assistant_response, env);
		// For each message in the response, add it to the mnew messages array
		response.map((message) => {
			new_messages.push(message);
		});
	}
	else {
		// If the response is not a function call, add the response to the new messages array
		new_messages.push({role: "assistant", content: assistant_response.choices[0].message.content});
	}
	// For each of the new messages, do an promise.all await add_message
	await Promise.all(new_messages.map(async (message) => {
		await add_message(message, env.SUPABASE_KEY, env.DB);
	}));

	// Return the last message content in the array
	return new Response(JSON.stringify(new_messages[new_messages.length - 1].content), { status: 200, headers: { 'Content-Type': 'application/json' } });
});

// 404 for everything else
router.all('*', () => new Response('Not Found.', { status: 404 }));

export default router;


