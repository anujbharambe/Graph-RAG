from Agent1 import run_graphrag_agent

def main():
    print("=== GraphRAG Assistant ===")
    query = input("Enter your query:\n> ")
    response = run_graphrag_agent(query)
    print("\n=== Answer ===\n", response)

if __name__ == "__main__":
    main()
