from src.config import Config
from src.agents import HealthTipAgent, TechnicalAgent, GeneralSupportAgent, OrchestratorAgent

def main():
    # 1. Ensure config is valid (e.g. API key exists)
    try:
        Config.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        return

    # 1. Initialize our specialized agents
    health_tip_agent = HealthTipAgent()
    technical_agent = TechnicalAgent()
    general_agent = GeneralSupportAgent()
    
    # 2. Initialize the orchestrator
    orchestrator = OrchestratorAgent(
        agents=[health_tip_agent, technical_agent, general_agent],
        default_agent=general_agent
    )
    
    print("=" * 55)
    print("Welcome to the Multi-Agent Customer Support Router!")
    print("Type your query below. Type 'exit' or 'quit' to stop.")
    print("=" * 55)
    print("\n")
    
    chat_history = []
    last_agent = None
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
                
            if not user_input:
                continue
                
            # Handle the request
            result = orchestrator.handle_request(user_input, chat_history)
            
            # Context switch message
            if last_agent != result['agent_name']:
                print(f"\n[System] Switched context to {result['agent_name']}")
                last_agent = result['agent_name']
            
            # Print the final response
            print(f"\n[{result['agent_name']}] {result['response']}\n")
            
            # Append to history
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": result['response']})
            
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
