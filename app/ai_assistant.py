from langchain_openai import ChatOpenAI
from langchain.agents import load_tools, initialize_agent, AgentType
from flask import current_app

def get_ai_assistant_response(user_input):
    try:
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            openai_api_key=current_app.config['OPENAI_API_KEY']
        )

        # Check if Google API keys are available
        google_api_key = current_app.config.get('GOOGLE_API_KEY')
        google_cse_id = current_app.config.get('GOOGLE_CSE_ID')

        tools = []
        if google_api_key and google_cse_id:
            import os
            os.environ["GOOGLE_API_KEY"] = google_api_key
            os.environ["GOOGLE_CSE_ID"] = google_cse_id
            tools = load_tools(["google_search"], llm=llm)

        if not tools:
            # Fallback to basic LLM if no tools are configured or available
            from langchain.schema import HumanMessage, SystemMessage
            messages = [
                SystemMessage(content="You are a helpful assistant for the CARE platform, dedicated to global well-being and education for children. You help users with project activities, health information, and educational resources."),
                HumanMessage(content=user_input)
            ]
            response = llm.invoke(messages)
            return response.content

        agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True
        )

        prompt = f"The user is asking about: {user_input}. You are a helpful assistant for the CARE platform, dedicated to global well-being and education for children. Help the user with their inquiry."
        response = agent.run(prompt)
        return response
    except Exception as e:
        return f"I'm sorry, I encountered an error: {str(e)}"
