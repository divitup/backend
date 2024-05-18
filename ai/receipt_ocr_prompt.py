from dataclasses import dataclass


@dataclass
class VisionReceiptExtractionPrompt:
    template: str = """
       You are an expert at information extraction from images of receipts.

       Given this of a receipt, extract the following information into a json string. The keys with their descriptions are as follows:
       {
            "vendor_name": "The name of the vendor from which the items were purchased",
            "vendor_address": "The address of the vendor from which the items were purchased",
            "items_purchased": [
                {
                    "item_name": "The name of the item",
                    "item_cost": "The cost of the item"
                }
            ],
            "datetime": "The date and time that the receipt was issued. This must be formatted like 'MM/DD/YY HH:MM'",
            "subtotal": "The total cost before tax",
            "tax_rate": "The tax rate",
            "total_after_tax": "The total cost after tax"
       }

       Do not guess. If some information is missing or not clear enough to extract, just return "N/A" in the relevant field.
       If you determine that the image is not of a receipt, just set all the fields in the formatting instructions to "N/A". 
       
       You must obey the output format under all circumstances. Please follow the formatting instructions exactly.
       Do not return any additional comments or explanation.
       """