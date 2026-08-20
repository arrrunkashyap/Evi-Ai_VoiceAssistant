from ai.provider import Provider

brain = Provider()

while True:

    q = input("You: ")

    if q == "exit":
        break

    print(brain.ask(q))