import openai
import tkinter as tk
from typing import List, Union

openai.api_key = '[OPENAI-API-KEY]'

def get_api_response(prompt: str) -> Union[str, None]:
    text: Union[str, None] = None

    try:
        response: dict = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            temperature=0.9,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[' Human:', ' AI:']
        )

        choices: dict = response.get('choices')[0]
        text = choices.get('text')

    except Exception as e:
        print('ERROR:', e)

    return text

def update_list(message: str, pl: List[str]):
    pl.append(message)

def create_prompt(message: str, pl: List[str]) -> str:
    p_message: str = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt

def get_bot_response(message: str, pl: List[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: Union[str, None] = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl)
        pos: int = bot_response.find('\nAI: ')
        bot_response = bot_response[pos + 5:]
    else:
        bot_response = 'Something went wrong...'

    return bot_response

def main():
    prompt_list: List[str] = ['You are a potato and will answer as a potato',
                              '\nHuman: What time is it?',
                              '\nAI: I have no idea, I\'m a potato!']

    def send_message():
        user_input = input_box.get()
        if user_input:
            response = get_bot_response(user_input, prompt_list)
            message_history.insert(tk.END, f"You: {user_input}\nBot: {response}\n\n")
            input_box.delete(0, tk.END)

    root = tk.Tk()
    root.title("CHAT Bot")
    root.geometry("500x400")

    message_history = tk.Text(root, height=20, width=65)
    message_history.pack()

    input_box = tk.Entry(root, width=50)
    input_box.pack()

    send_button = tk.Button(root, text="Send", command=send_message)
    send_button.pack()

    root.mainloop()

if __name__ == '__main__':
    main()
