import { get_balance } from "./modules/crypto";

export async function handle_function(called_function, env){
    const function_name = called_function.choices[0].message.function_call.name
    if (called_function === "check_solana_balance") {
        return await get_balance("9DtsixQAmaHZ1UPRqoGFNocezYYWBXFjU9pHtSCrRYzc", env.HELIUS_KEY);
    }
    else {
        return "I'm sorry, I don't know that function.";
    }
}