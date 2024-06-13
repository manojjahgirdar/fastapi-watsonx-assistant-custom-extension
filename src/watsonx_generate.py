from ibm_watson_machine_learning.foundation_models import Model
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
import os

class WatsonX:
    def __init__(self) -> None:
        self.ibm_cloud_api_key = os.getenv('IBM_CLOUD_API_KEY')
        self.project_id = os.getenv('WX_PROJECT_ID')
        self.wx_url = os.getenv('WX_ENDPOINT')

    def get_credentials(self):
        return {
            "url" : self.wx_url,
            "apikey" : self.ibm_cloud_api_key
        }
    
    def generate(self, input_text):

        model_id = "ibm/granite-13b-chat-v2"

        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 100,
            "min_new_tokens": 1,
            "repetition_penalty": 1
        }

        prompt = PromptTemplate(
			input_variables=["input_text"], 
			template="""
<|Instruction|>
Act as a support agent. Evaluate the given question and try to answer them. Be positive, your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.
If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
Keep your answers short and concise.

<|Questions|>
Question: {input_text} 
Helpful Answer: 
""",
)
        prompt_formatted_str: str = prompt.format(input_text=input_text)

        llm = Model(
                model_id=model_id, 
                params=parameters, 
                credentials=self.get_credentials(),
                project_id=self.project_id
        )
        
        response = llm.generate_text(prompt=prompt_formatted_str)

        return response