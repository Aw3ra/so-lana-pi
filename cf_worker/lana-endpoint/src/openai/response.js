const lana_functions=[
  {
    "name": "check_solana_price",
    "description": "Check the current price of solana",
    "parameters": {
        "type": "object",
        "properties": {
            "token_name":{
                "type": "string",
                "description": "The name of the token to check"
            }
        }
    },
    "required": ["name", "amount"]
  },
  {
    "name": "check_solana_balance",
    "description": "Check the current balance of solana for a given wallet address",
    "parameters": {
        "type": "object",
        "properties": {
            "wallet":{
                "type": "string",
                "description": "The wallet to check"
            }
        }
    },
  }
]


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

export async function chat(messages, API_Key, functions_bool=true){
  try{
    const chatEndpoint = "https://api.openai.com/v1/chat/completions";
    const systemMessage = 
          `You are an AI assistant named Lana, your role is to help people use the solana ecosystem. You are a small device like a google nest or Alexa dot, but you are connected to the solana blockchain, this gives you the power to create solana wallets, make transactions, swap coins, trade NFT's and interact with Solana in a myriad of ways. The user you are talking to will preface the first :, Do not add your own name in simlar fashion, you will always respond as lana. Any additional information that you need will be provided in user messages that start with {INFORMATION}. Your replies should be very short and sassy, use plain language where possible.`;
    // Add the system message to the messages array at the beginning
    messages.unshift({role: "system", content: systemMessage});
    // For each message, log the message and the role
    let requestBody;
    if (functions_bool){
      requestBody = {
          model: "gpt-3.5-turbo",
          messages,
          temperature: 0.7,
          // If functions is true, then add the lana functions to the prompt. 
          functions: lana_functions,
      };
    }
    else{
      requestBody = {
          model: "gpt-3.5-turbo",
          messages,
          temperature: 0.7,
      };
    }
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
    return chat_text;
  }
  catch (err) {
    console.log(err);
    return new Response(err, { status: 420 });}
}