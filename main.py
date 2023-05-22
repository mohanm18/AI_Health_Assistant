import openai


with open('hidden.txt') as file:
    openai.api_key = file.read()

 #function to make the requests   
def get_api_response(prompt: str) -> str | None:
    text: str | None = None

    try:
        response: dict = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[' Human:', ' AI:']
        )

        choices: dict = response.get('choices')[0]
        text = choices.get('text')
    #it prints an ERROR if things goes wrong
    except Exception as e:
        print('ERROR:', e)

    return text

#function created to append the messages, so that the history of conversation is maintained.
def update_list(message: str, pl: list[str]):
    pl.append(message)


#function created to get the prompt from the user and store it in an array
def create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt

#function created to get the response from the bot
def get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl) #array is being updated with the response of the assistant
        pos: int = bot_response.find('\nAI: ') #finding AI as response needs to be printed after that
        bot_response = bot_response[pos + 5:]  #index no. + 5 to provide formatted print
    else:
        bot_response = 'Something went wrong...'

    return bot_response


def main():
    prompt_list: list[str] = ['You are an exceptionally great, optimistic and sarcastic doctor who predicts the type of disease from the provided symptoms, provides description about the disease. And also provides remedies with the help of which those particular diseases can be cured.',
                              '\nHuman: Hi, I am feeling somewhat dizzy?',
                              '\nAI: Hello there, well we all are dizzy nowadays hahaha! Btw from how long are you feeling in such a way?']

    while True:
        user_input: str = input('You: ')  #takes input
        response: str = get_bot_response(user_input, prompt_list) #provides response provided by the assistant
        print(f'Doc.Jeremy: {response}')


if __name__ == '__main__':
    print("\n------------------ Doc. Jeremy At Your Service-----------------------")
    print("\nDoc.Jeremy: Hello there HomoSapien. Is there something I can help you with??")
    main()