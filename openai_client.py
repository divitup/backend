from inits.general import openai_client

def receipt_ocr(image_url):
    '''

    :param image_url: S3 URL of the image
    :return: Receipt OCR result
    '''
    prompt = '''
    Please extract the information from the receipt image, and output the information in the following json format:
    
    '''


response = openai_client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What’s in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                    },
                },
            ],
        }
    ],
    max_tokens=300,
)

print(response.choices[0])