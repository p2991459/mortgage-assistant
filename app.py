import time
from flask import Flask, request, jsonify, render_template
import json
import os
from sql_agent import mrkl
app = Flask(__name__)
from prompt_similarity import get_best_match
from openai_playground import general_query
@app.route('/', methods=['GET', 'POST'])
def index():
    #TODO: Dump the previous conversation to responses.jsonl and delete the json file
    #DONE: Delete last conversation json file to prevent overriding
    filename = 'last_conversation.json'
    if os.path.exists(filename):  # Check if file exists in current directory
        os.remove(filename)  # Delete the file
        print(f"{filename} has been deleted successfully!")
    else:
        print(f"{filename} does not exist in the current directory.")
    return render_template('index.html')

@app.route('/gpt_response', methods=['GET', 'POST'])
def gpt_response():
    if request.method == 'POST':
        request_data = request.json
        user_input = request_data["text"]
        cache_prompts = json.loads(open("cache_prompts.json").read())
        if user_input in cache_prompts:
            time.sleep(3)
            return str(cache_prompts[user_input])
        elif user_input not in cache_prompts:
            default_prompt_cache = json.loads(open("general_prompt_cache.json").read())
            best_match = get_best_match(user_input, list(default_prompt_cache.keys()))
            print(f"This is the best match from the prompt cache: {best_match}")
            if best_match is not None:
                time.sleep(3)
                return str(default_prompt_cache[best_match])
            else:
                # TODO: It is the temp method to store the cache, it reduce the bot efficiency.
                # output_from_normal_chain = gpt.submit_request(user_input)['choices'][0]['text']
                # print(f"This is output from normal chain:  {output_from_normal_chain}")
                # if output_from_normal_chain == "RESULTS FROM DB":
                db_chain_output = str(mrkl.run(user_input))
                print(f"This is the output from db_chain: {db_chain_output}")
                if (db_chain_output == "Syntax error")  or (db_chain_output == "It is general question.") or (db_chain_output == "It is general question") or (db_chain_output == "It is a general question. Please provide more details."):
                    try:
                        history_chat = json.loads(open("last_conversation.json").read())
                        print(f"This is history chat: {history_chat}")
                        prompt = ""
                        for conversation in history_chat:
                            if conversation["from"] == "bot":
                                print(conversation["from"])
                                prompt+=f'\nAI: {conversation["text"]}'
                            else:
                                prompt += f'\nHuman: {conversation["text"]}'
                        prompt += f'\nHuman: {user_input}'
                        print(prompt)
                        return general_query(prompt)
                    except FileNotFoundError as e:
                        print("File not found so executing except block")
                        output = general_query(user_input)
                        cache_prompts[user_input] = output
                        open("cache_prompts.json", "w").write(json.dumps(cache_prompts))
                        return output
                elif((db_chain_output == "Got empty result")):
                    output = "There is no data that matches your requirements. We can put you in contact with a qualified and regulate mortgage advisor, who will guide you through the next steps to apply for the mortgage.Alternatively you can apply now for a mortgage, via the application form in this website.In both circumstances, we will discuss with you all the best options available to you."
                    return output
                else:
                    cache_prompts[user_input] = db_chain_output
                    open("cache_prompts.json", "w").write(json.dumps(cache_prompts))
                    return db_chain_output
                # else:
                #     cache_prompts[user_input] = str(output_from_normal_chain)
                #     open("cache_prompts.json", "w").write(json.dumps(cache_prompts))
                #     return str(output_from_normal_chain)

        else:
            final_output = str(mrkl.run(user_input))
            cache_prompts[user_input] = final_output
            open("cache_prompts.json", "w").write(json.dumps(cache_prompts))
            return final_output



@app.route('/conversation', methods=['GET', 'POST'])
def conversation():
    '''This will take conversation id and conversations and dump them to last_conversation to update the responses.jsonl to improve the chatbot efficiency'''
    data = request.json
    id = data["id"]
    messages = data["messages"]
    try:
        conv_id = (open("last_conversation_id.txt").read())
    except FileNotFoundError as e:
        open("last_conversation_id.txt","w").write(str(id))
        conv_id = (open("last_conversation_id.txt").read())
    if conv_id == id:
        open("last_conversation.json","w").write(messages)
    else:
        open("last_conversation_id.txt","w").write(str(id))
        open("last_conversation.json", "w").write(messages)
    return "ok"

@app.route('/get_conversation_id', methods=['GET'])
def get_conversation_id():
    '''This will read the conversation ID from a file and return it as a response.'''
    conv_id = open("last_conversation_id.txt").read()
    return conv_id
if __name__ == '__main__':
    app.run(debug=True)