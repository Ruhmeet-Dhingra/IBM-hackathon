from chat import chat_response

question = input("Ask ROV: ")

response = chat_response(question)

print("\nROV:\n")
print(response)