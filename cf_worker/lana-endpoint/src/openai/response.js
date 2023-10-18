export async function transcribe(request, API_Key)
    {
        try{
            const audioEndpoint = "https://api.openai.com/v1/audio/translations";
            const rawAudioData = await request.arrayBuffer();
            if (!rawAudioData) {
              return new Response("Audio data missing", { status: 69 });
            }
            const formData = new FormData();
            const blob = new Blob([rawAudioData], { type: "audio/wav" });
            formData.append("file", blob, "audio.wav");
            formData.append("model", "whisper-1");
            const openaiHeaders = {
              "Authorization": `Bearer ${API_Key}`
            };
            const openaiInit = {
              method: "POST",
              body: formData,
              headers: openaiHeaders
            };
            const response = await fetch(audioEndpoint, openaiInit);
            const audio_text = JSON.parse(await response.text()).text;
            return {role: "user", content: audio_text};
        }
        catch (err) {return new Response(err, { status: 420 });}
    }

export async function chat(messages, API_Key){
  try{
    const chatEndpoint = "https://api.openai.com/v1/chat/completions";
    const systemMessage = "You are an AI assistant named Lana, you are extremely sassy and reply with short responses";
    // Add the system message to the messages array at the beginning
    messages.unshift({role: "system", content: systemMessage});
    // For each message, log the message and the role
    const requestBody = {
        model: "gpt-3.5-turbo",
        messages,
        temperature: 0.7
    };
    const openaiHeaders = {
      "Authorization": `Bearer ${API_Key}`,
      "Content-Type": "application/json"
    };
    const openaiInit = {
      method: "POST",
      body: JSON.stringify(requestBody),
      headers: openaiHeaders
    };
    const response = await fetch(chatEndpoint, openaiInit);
    const chat_text = await response.json();
    return chat_text.choices[0].message.content;
  }
  catch (err) {
    console.log(err);
    return new Response(err, { status: 420 });}
}