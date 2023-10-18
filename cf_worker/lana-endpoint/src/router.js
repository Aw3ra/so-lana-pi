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
	//Get the text from the audio file sent in the POST request
	const audio_text = await transcribe(request, env.OPENAI_API_KEY);
	//Get the messages from the database
	let messages = await get_messages("awera", env.SUPABASE_KEY, env.DB);
	//Add the audio text to the messages array
	messages.push(audio_text);  
	//Retrieve the assistant message from OpenAI and add it to the messages array
	let assistant_response = await chat(messages, env.OPENAI_API_KEY);
	// If the response is a dictionary, it is a command
	if (typeof assistant_response === "object") {
		// Do some more logic here, but for now just create another message
		assistant_response = "Command received.";
	}
	else {
		// If the response is not a dictionary, it is a message
		assistant_response = assistant_response.choices[0].message.content;
	}

	messages.push({role: "assistant", content: assistant_response});
	// Return the messages array as a JSON object
	return new Response(JSON.stringify(messages), { status: 200, headers: { 'Content-Type': 'application/json' } });
});

// 404 for everything else
router.all('*', () => new Response('Not Found.', { status: 404 }));

export default router;
