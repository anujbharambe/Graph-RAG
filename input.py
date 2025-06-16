from Agent1 import run_graphrag_agent

def main():
    print("=== GraphRAG Assistant ===")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        query = input("You: ")
        if query.strip().lower() in {"exit", "quit"}:
            print("\nConversation saved to logging.txt. Goodbye!")
            break

        response = run_graphrag_agent(query)
        print(f"\nAI: {response}\n")

if __name__ == "__main__":
    main()
