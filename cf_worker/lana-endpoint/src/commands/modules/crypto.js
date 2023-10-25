export async function get_balance(wallet, HELIUS_KEY){
    try{
        const helius_url = `https://api.helius.xyz/v0/addresses/${wallet}/balances?api-key=${HELIUS_KEY}`;
        const response = await fetch(helius_url);
        const balance = await response.json();
        // Conver the balance from lamports to SOL
        let sol =  balance.nativeBalance / 1000000000;
        // Round to 2 decimal places
        sol = Math.round(sol * 100) / 100;
        // Return an informative message about the balance
        return `{INFORMATION} You have just looked up the users wallet and ther balance is ${sol} solana.`;
    }
    catch (err) {return `{INFORMATION} There was an error: ${err}`;}
}

export async function get_solana_facts(fact_type){
    try{
        if (fact_type === "daily_active_users"){
            // User http request to hit this api: https://api.solana.fm/v0/stats/active-users
            let response = await (await fetch("https://api.solana.fm/v0/stats/active-users")).json();
            return `{INFORMATION} The current number of active users on solana is ${response.result.activeUsers}.` 
        }
        else if (fact_type === "daily_fees"){
            let response = await (await fetch("https://api.solana.fm/v0/stats/tx-fees?date=25-10-2023")).json();
            let fees = response.result.totalTxFees / 1000000000;
            fees = Math.round(fees * 100) / 100;
            // Divide this amount by the rouhg cost of a transaction
            return `{INFORMATION} The collective amount of sol spent on transactions by everyone today is: ${fees}.`
        }
    }
    catch (err) {return `{INFORMATION} There was an error: ${err}`};
}