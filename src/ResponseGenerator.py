from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class ResponseGenerator():

    def __init__(self, model_name, chat_history_ids="default",bot_input_ids="default"):
        self.processor = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.chat_history_ids=chat_history_ids
        self.bot_input_ids=bot_input_ids

    def encoder(self, step):
        new_user_input_ids = self.processor.encode(input(">> User:") + self.processor.eos_token, return_tensors='pt')
        self.bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

    def decoder(self):
        self.chat_history_ids = self.model.generate(self.bot_input_ids, max_length=1000, pad_token_id=self.processor.eos_token_id, temperature=0.7)

    def print(self):
        print("DialoGPT: {}".format(self.processor.decode(self.chat_history_ids[:, self.bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))


def main():
    response_generator = ResponseGenerator("microsoft/DialoGPT-medium")
    for step in range(10):
        response_generator.encoder(step)
        response_generator.decoder()
        response_generator.print()


if __name__ == '__main__':
    main()

# tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
# model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# # Let's chat for 5 lines
# for step in range(10):
#     # encode the new user input, add the eos_token and return a tensor in Pytorch
#     new_user_input_ids = tokenizer.encode(input(">> User:") + tokenizer.eos_token, return_tensors='pt')

#     # append the new user input tokens to the chat history
#     bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

#     # generated a response while limiting the total chat history to 1000 tokens, 
#     chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id, temperature=0.7)

#     # pretty print last ouput tokens from bot
#     print("DialoGPT: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))

