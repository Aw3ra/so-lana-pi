export async function get_messages(user, SUPABASE_KEY, database){
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
        messages.sort((a, b) => (a.created_at > b.created_at) ? 1 : -1);
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
export async function upload_messages(message, user, SUPABASE_KEY, database){
    try{
        const supabase_url = `https://${database}.supabase.co/rest/v1/messages`;
        const supabase_headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": `Bearer ${SUPABASE_KEY}`,
            "Content-Type": "application/json"
        };
        const supabase_init = {
            method: "POST",
            headers: supabase_headers,
            body: JSON.stringify({
                "from_user": user,
                "for_user": user,
                "content": message,
                "device": "00001"
            })
        };
        const response = await fetch(supabase_url, supabase_init);
        const messages = await response.json();
        return messages;
    }
    catch (err) {return new Response(err, { status: 420 });}
}