# code
import random
responses = [
       "Yes, definitely.",
       " Chances are slim.",
       "Unclear at the moment .",
       "Cannot predict now.",
       "Very doubtful.",
       " Absolutely not.",
       "Outlook not so good.",
       "Highly likely."]
# code
while True:
       question = input("Ask the magical 8 Ball a question (type 'exit' to quit): ")
       if question.lower() == 'exit':
           print("Goodbye!")
           break
       else:
           print("Magic 8 Ball says:", random.choice(responses))

