import os

from langchain.chains import TransformChain
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.runnables import chain
from langchain_core.output_parsers import JsonOutputParser
import base64
from langchain.callbacks import get_openai_callback

from ai.receipt_model import ReceiptInformation
from ai.receipt_ocr_prompt import VisionReceiptExtractionPrompt


class VisionReceiptExtractionChain:

    def __init__(self, llm):
        self.llm = llm
        self.chain = self.set_up_chain()

    @staticmethod
    def load_image(path: dict) -> dict:
        """Load image and encode it as base64."""

        def encode_image(path):
            with open(path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")

        image_base64 = encode_image(path["image_path"])
        return {"image": image_base64}

    def set_up_chain(self):
        extraction_model = self.llm
        prompt = VisionReceiptExtractionPrompt()
        parser = JsonOutputParser(pydantic_object=ReceiptInformation)

        load_image_chain = TransformChain(
            input_variables=["image_path"],
            output_variables=["image"],
            transform=self.load_image,
        )

        # build custom chain that includes an image
        @chain
        def receipt_model_chain(inputs: dict) -> dict:
            """Invoke model"""
            msg = extraction_model.invoke(
                [
                    HumanMessage(
                        content=[
                            {"type": "text", "text": prompt.template},
                            {"type": "text", "text": parser.get_format_instructions()},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": inputs["image_url"],
                                },
                            },
                        ]
                    )
                ]
            )
            return msg.content

        # return load_image_chain | receipt_model_chain | JsonOutputParser()
        return receipt_model_chain | JsonOutputParser()

    def run_and_count_tokens(self, input_dict: dict):
        with get_openai_callback() as cb:
            result = self.chain.invoke(input_dict)

        return result, cb


if __name__ == "__main__":
    model = ChatOpenAI(
        api_key=os.getenv("OPENAI_API"),
        temperature=0,
        model="gpt-4o",
        max_tokens=1024
    )

    extractor = VisionReceiptExtractionChain(model)

    res, cb = extractor.run_and_count_tokens(
        {"image_url": "https://divup-images.s3.amazonaws.com/recript1.jpg"}
    )
    print("Result:")
    print(res)
    print("Callback:")
    print(cb)
