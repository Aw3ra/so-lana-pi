export const lana_functions=[
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
    },

    {
        "name": "check_solana_details",
        "description": "Check the current details of the solana blockchain",
        "parameters": {
            "type": "object",
            "properties": {
                "fact_name":{
                    "type": "string",
                    "description": "The type of fact to check",
                    "enum": [
                        "daily_fees", "daily_rewards", "daily_active_users"
                    ]
                }
            }
        },
    }
  ]