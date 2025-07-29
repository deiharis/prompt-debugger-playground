import streamlit as st
import requests
import tiktoken


st.set_page_config(page_title="Prompt Debugger Playground")
st.title("🧠 Prompt Debugger Playground")

api_key = st.text_input("🔑 Enter your OpenRouter API Key", type="password")

model = st.selectbox(
    "Choose a Model",
    ["mistral", "gpt-3.5-turbo", "deepseek-chat"]
)

prompt = st.text_area("Enter your Prompt Here", height=200)

if st.button("Run Prompt"):
    if not api_key or not prompt:
        st.warning("Please enter your API key and prompt.")
    else:
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "http://localhost", 
            "Content-Type": "application/json"
        }
        
        model_map = {
            "mistral": "mistralai/mistral-7b-instruct",
            "gpt-3.5-turbo": "openai/gpt-3.5-turbo",
            "deepseek-chat": "deepseek-ai/deepseek-chat"
        }

        data = {
            "model": model_map[model],
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        with st.spinner("Querying model..."):
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                res_json = response.json()
                reply = res_json["choices"][0]["message"]["content"]
                st.subheader("🤖 Model Response:")
                st.write(reply)

                enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
                tokens = enc.encode(prompt)
                token_count = len(tokens)
                st.info(f"🔢 Token Count: {token_count}")

                token_price = {
                    "gpt-3.5-turbo": 0.0015 / 1000,
                    "mistral": 0.0002 / 1000,
                    "deepseek-chat": 0.0001 / 1000
                }
                cost = token_count * token_price[model]
                st.success(f"💸 Estimated Cost: ${cost:.6f}")
            else:
                st.error(f"API Error: {response.status_code}")
                st.json(response.json())
