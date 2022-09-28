from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import argparse
class ResponseGenerator():

    def __init__(self, model_name, chat_history_ids="", bot_input_ids=""):
        self.processor = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.chat_history_ids=chat_history_ids
        self.bot_input_ids=bot_input_ids

    def encode(self, query):
        new_user_input_ids = self.processor.encode(query + self.processor.eos_token, return_tensors='pt')
        self.bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1) if type(self.chat_history_ids)!=str else new_user_input_ids
     
    def getResponse(self, query, args):
        ResponseGenerator.encode(self, query)
        self.chat_history_ids = self.model.generate(self.bot_input_ids, max_length=1000, pad_token_id=self.processor.eos_token_id, num_beams=args.bw, early_stopping=args.stopping, temperature=args.temp)
        response="DialoGPT: {}".format(self.processor.decode(self.chat_history_ids[:, self.bot_input_ids.shape[-1]:][0], skip_special_tokens=True))
        return response
        
def main(args):
    response_generator = ResponseGenerator("microsoft/DialoGPT-medium")
    while True:
        user_query = input(">> User: ")
        response=response_generator.getResponse(user_query, args)
        print(response)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Setting the arguments in DialoGPT decoder')
    parser.add_argument('--bw', help='Beam search width', type = int, default = 5)
    parser.add_argument('--stopping', help='Choose whether to terminate the algorithm upon encountering a complete hypothesis', type = bool, default = True)
    parser.add_argument('--temp', type = float, default = 0.7)
    args = parser.parse_args()

    main(args)