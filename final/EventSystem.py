import random
import ollama


class EventSystem:
    def __int__(self, state):
        self.gainOrLoseMoney = GainOrLoseMoney(state)


class GainOrLoseMoney:
    def __init__(self, state):
        self.input = ["Generate a simple, short sentence. This sentence is a positive event in adventure game, which "
                      "allows player to gain a little money. You need not to mention how many coins. DO not be polite to me, just provide the result",
                      "Generate a simple, short sentence. This sentence is a bad event in adventure game, which let "
                      "player lose a little money. You need not to mention how many coins. DO not be polite to me, just provide the result"]
        self.state = state

    def execute(self):
        input_index = random.randint(0, len(self.input)-1)
        input_selected = self.input[input_index]
        amount = 0

        if input_index == 0:
            amount = random.randint(4, 10)
            amount_text = " Gained {} coins!".format(amount)
        else:
            amount = -random.randint(2, 13)
            amount_text = " Lost {} coins!".format(amount)

        response = ""
        for part in ollama.generate('llama2', input_selected, stream=True):
            response += part['response']

        self.state.coins += amount

        response = response.replace("\"", '')
        print(response+amount_text, sep='')
        return response+amount_text


if __name__ == '__main__':
    gainOrLoseMoney = GainOrLoseMoney()
    gainOrLoseMoney.execute()