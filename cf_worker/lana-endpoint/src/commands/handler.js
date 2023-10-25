import { get_balance, get_solana_facts } from "./modules/crypto";

export async function handle_function(called_function, env){
    const function_name = called_function.choices[0].message.function_call.name
    if (function_name === "check_solana_balance") {
        return await get_balance("9DtsixQAmaHZ1UPRqoGFNocezYYWBXFjU9pHtSCrRYzc", env.HELIUS_KEY);
    }
    else if (function_name === "check_solana_details") {
        const fact_type = JSON.parse(called_function.choices[0].message.function_call.arguments).fact_name;
        console.log(fact_type);
        const fact_results = get_solana_facts(JSON.parse(called_function.choices[0].message.function_call.arguments).fact_name);
        return fact_results;
    }
    else {
        return "I'm sorry, I don't know that function.";
    }
}