"use strict";
(() => {
  addEventListener("fetch", (event) => {
    event.respondWith(handleRequest(event.request));
  });
  async function handleRequest(request) {
    if (request.method !== "POST") {
      return new Response("Please POST an audio file.", { status: 420 });
    }
    const openaiEndpoint = "https://api.openai.com/v1/audio/translations";
    const rawAudioData = await request.arrayBuffer();
    if (!rawAudioData) {
      return new Response("Audio data missing", { status: 69 });
    }
    const formData = new FormData();
    const blob = new Blob([rawAudioData], { type: "audio/wav" });
    formData.append("file", blob, "audio.wav");
    formData.append("model", "whisper-1");
    const openaiHeaders = {
      "Authorization": "Bearer token"
    };
    const openaiInit = {
      method: "POST",
      body: formData,
      headers: openaiHeaders
    };
    const response = await fetch(openaiEndpoint, openaiInit);
    return new Response(await response.text(), { status: response.status });
  }
})();