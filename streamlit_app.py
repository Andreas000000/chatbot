from openai import OpenAI
client = OpenAI(api_key=openai_api_key)

ASSISTANT_ID = "asst_NIVJXokSYcboqteCloJiJesL"

# ... (der Rest deines Codes bis zum Prompt bleibt gleich)

if prompt := st.chat_input("What is up?"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Neues: Assistant verwenden
    thread = client.beta.threads.create(
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID,
    )

    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        response = messages.data[0].content[0].text.value
    else:
        response = f"Assistant run failed with status: {run.status}"

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
