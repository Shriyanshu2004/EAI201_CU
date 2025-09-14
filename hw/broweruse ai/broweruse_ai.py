from browser_use_sdk import BrowserUseSdk

CURRENT_DATE = "2025-08-15"

USERS = [
    {
        "full_name": "abcd",
        "city": "ODISHA",
        "request": "Comprehensive understanding of Deep Learning concepts",
    },
]

browser_sdk = BrowserUseSdk(api_key="your-api-key-here")

for user in USERS:
    response = browser_sdk.run(
        llm_model="o3",
        task=f"""
Your goal is to collect information about Deep Learning fundamentals.

Find top resources that explain this topic in depth.

  - Location: {user['city']}
  - Date of search: {CURRENT_DATE}
  - User Name: {user['full_name']}
  - Purpose: {user['request']}

List the top 6 websites that provide valuable insights and explain why they are useful.
""",
    )
    print(f"Results for {user['full_name']}:\n{response}\n")
