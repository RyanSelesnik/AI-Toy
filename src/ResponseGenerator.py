from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
# import tensorflow as tf
class ResponseGenerator():

    def __init__(self, model_name, chat_history_ids="default",bot_input_ids="default"):
        self.processor = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.chat_history_ids=chat_history_ids
        self.bot_input_ids=bot_input_ids

    def encode(self, step, query):
        new_user_input_ids = self.processor.encode(query + self.processor.eos_token, return_tensors='pt')
        self.bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids
     
    def getResponse(self, step, query):
        ResponseGenerator.encode(self, step, query)
        self.chat_history_ids = self.model.generate(self.bot_input_ids, max_length=1000, pad_token_id=self.processor.eos_token_id, num_beams=5, early_stopping = True, temperature=0.7)
        print("DialoGPT: {}".format(self.processor.decode(self.chat_history_ids[:, self.bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))
        
def main():
    response_generator = ResponseGenerator("microsoft/DialoGPT-medium")
    step = 0
    while True:
        user_query = input(">> User: ")
        # response_generator.encode(step, input(">> User: "))
        response_generator.getResponse(step, user_query)
        step +=1

if __name__ == '__main__':
    main()