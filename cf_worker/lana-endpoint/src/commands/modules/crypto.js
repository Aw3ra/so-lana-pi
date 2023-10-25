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
        return `{INFORMATION} You have just looked up the users wallet and ther balance is ${sol} solanaL.`;
    }
    catch (err) {return new Response(err, { status: 420 });}
}