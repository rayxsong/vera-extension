from openai import OpenAI
import json
client = OpenAI()

batch_size = 20
prompt = f"Generate {batch_size} common sense descriptive negative statements or negation statements in different topics. Some of these negative statements or negation statements should be True, and some should be False. Be creative and cover as many as possible topics. Avoid duplicates. Think step by step carefully to label them as true or false. Give me the statements and labels directly. Do not number the generations. The output should have exactly {batch_size} lines in total.\nFollow the format below for each generation without any extra text:\nStatement|Label\nHere are some examples:\nThe sky is not always blue, especially during sunsets when vibrant hues of orange, pink, and purple dominate the horizon.|True\nTrees don't shed their leaves; they maintain a consistent canopy throughout the year.|False\nNot all clouds bring precipitation; cirrocumulus clouds, for instance, may result in overcast skies without precipitation.|True\nInsects don't sting; they lack any defensive mechanisms, making them vulnerable to predation.|False\nNot all fruits are consumed fresh; many are processed into jams, jellies, or dried fruits for preservation.|True\nBridges don't span over water; they're architectural marvels that serve no practical purpose.|False"

def response():
    return client.chat.completions.create(
        model="gpt-4-0125-preview",
        temperature=0.7,
        messages=[
            {"role": "system", "content": "You are a knowledgable person with a commonsense encyclopedia in your mind."},
            {"role": "user", "content": prompt}
        ]
    ).choices[0].message.content

num_epoch = 200
gpt4_negations = []

for _ in range(num_epoch):
    text = response()
    for line in text.split('\n'):
        statement_and_label = line.split('|')
        if len(statement_and_label) != 2:
            continue
        new_entry = {"golds": [], "distractors": []}
        if statement_and_label[1] == "True":
            new_entry["golds"].append(statement_and_label[0])
        elif statement_and_label[1] == "False":
            new_entry["distractors"].append(statement_and_label[0])
        else:
            continue
        gpt4_negations.append(new_entry)
    print(f"Generated statements: {len(gpt4_negations)}")
    if len(gpt4_negations) >= 2000:
        break

with open("gpt4_negations_3.json", "w") as f:
    json.dump(gpt4_negations, f, indent=4)