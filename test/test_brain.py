from core.brain import ask_ai

while True:
    q = input("You: ")

    if q == "exit":
        break

    print("EVI:", ask_ai(q))