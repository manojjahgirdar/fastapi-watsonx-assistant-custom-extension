import json
from main import app, Depends, get_api_key, Query
from pydantic import BaseModel

''' 
    API CALL SUCCESS VALIDATOR MODELS (Output Validator)

    - This model describe what to expect in case of a successful response.
    - This model is requrired to generate an OpenAPI spec file with proper output definition.
'''

class PostValidatorSuccess(BaseModel):
    output: str = 'Your output will be a json object with a key named `output`.'

''' 
    API CALL ERROR VALIDATOR MODELS (Error Validator)
    
    - These models describe what output to expect in case of an error.
    - These models are required to generate an OpenAPI spec file with proper error handling definition.
'''

class PostValidatorError(BaseModel):
    detail: str = 'Validation Error Occurred'


class PostValidatorError2(BaseModel):
    detail: str = 'Invalid credentials'


''' 
    HANDLE RESPONSES 

    - Define how 2xx, 3xx, 4xx, 5xx responses look like.
    - The OpenAPI spec json will have these details.
'''

def handleResponse():
    return {
        200: {
            'model': PostValidatorSuccess,
            'description': 'A successful response will look something like this'
        },
        400: {
            'model': PostValidatorError2,
            'description': 'A response with invalid username/password will look something like this'
        },
        422: {
            'model': PostValidatorError,
            'description': 'A failed response will look something like this'
        }
    }

''' 
    API ROUTES 

    - Define the API routes
'''
api_url = "/api/generate"
api_details = "This is an API to generate text from Watsonx.ai"
api_tags = ["Watsonx.ai"]

@app.get(api_url, tags=api_tags, responses=handleResponse(), summary=api_details)
async def watsonxGenerate(api_key_valid: bool = Depends(get_api_key), question: str = Query(..., description="Question")):
    
    # -------------- Invoking Business Logic here to get output --------------
    from src.watsonx_generate import WatsonX
    obj = WatsonX()
    output = obj.generate(input_text=question)
    # -----------------------------------------------------------------------

    return {"output": output}