from agent.agent_builder import build_agent
from config import PART_PATH

def main():
    agent = build_agent()

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"Please add dimensions to the drawing "
                           f"for part file {PART_PATH}"
            }
        ]
    })

    print("Results : ")
    

    final_message = result["messages"][-1]
    print(final_message.content)

if __name__ == "__main__":
    main()