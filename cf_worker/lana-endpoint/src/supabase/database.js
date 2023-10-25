export async function get_messages(user, SUPABASE_KEY, database){
    // Using fetch, get all the messages from the database for the user
    try{
        const supabase_url = `https://${database}.supabase.co/rest/v1/messages?for_user=eq.${user}`;
        const supabase_headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": `Bearer ${SUPABASE_KEY}`
        };
        const supabase_init = {
            method: "GET",
            headers: supabase_headers
        };
        const response = await fetch(supabase_url, supabase_init);
        const messages = await response.json();
        // Convert the array of messages into a date-sorted array of messages in the form: {"role": "user", "content": "message"}
        // 1. Sort the array by date
        messages.sort((a, b) => (a.created_at > b.created_at) ? 1 : -1);
        // 2. Convert the array into the form: {"role": "user", "content": "message"}
        messages.map((message) => {
            message.role = message.role;
            message.content = message.content;
            delete message.message;
            delete message.from_user;
            delete message.for_user;
            delete message.created_at;
            delete message.id;
            delete message.device;
        });
        return messages;
    }
    catch (err) {return new Response(err, { status: 420 });}
}

export async function add_message(message, SUPABASE_KEY, database){
    // Using fetch, add the message to the database
    try{
        const supabase_url = `https://${database}.supabase.co/rest/v1/messages`;
        const new_message = {
            "created_at": new Date().toISOString(),
            "device": "00001",
            "content": message.content,
            "for_user": "awera",
            "role": message.role,
        };
        const supabase_headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": `Bearer ${SUPABASE_KEY}`,
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        };
        const supabase_init = {
            method: "POST",
            headers: supabase_headers,
            body: JSON.stringify(new_message)
        };
        const response = await fetch(supabase_url, supabase_init);
        if (!response.ok) {
            throw new Error(`Supabase responded with status: ${response.status}`);
        }
    }
    catch (err) {
        console.error("Error in add_message:", err);
        return new Response(err.toString(), { status: 420 });
    }
}