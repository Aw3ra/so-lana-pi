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
            message.role = message.from;
            message.content = message.content;
            delete message.message;
            delete message.from_user;
            delete message.for_user;
            delete message.created_at;
            delete message.id;
            delete message.device;
            delete message.from;
        });
        return messages;
    }
    catch (err) {return new Response(err, { status: 420 });}

}