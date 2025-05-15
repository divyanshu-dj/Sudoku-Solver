from google import genai

client = genai.Client(api_key="AIzaSyCS6rGZAl3i9eN44Dsv-HccLss78sHLWoE")

PROMPT = """
You are given an image of a Sudoku puzzle.
Your task is to analyze the image and extract the Sudoku grid.

### Output Format (very important):
Return the Sudoku puzzle as a valid 9x9 Python list of lists. Each row should contain exactly 9 integers. Use `0` for any empty cell.

Example:
[
  [5, 3, 0, 0, 7, 0, 0, 0, 0],
  [6, 0, 0, 1, 9, 5, 0, 0, 0],
  [0, 9, 8, 0, 0, 0, 0, 6, 0],
  ...
  [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

### Instructions:
- Read the digits in the cells from the image.
- Leave a cell as 0 if it is blank or unclear.
- Do not include extra commentary.
- Only return a valid 9x9 Python array as shown above.
"""

structured_output_schema = {
    "type": "object",
    "properties": {
        "grid": {
            "type": "array",
            "items": {
                "type": "array",
                "items": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 9
                },
                "minItems": 9,
                "maxItems": 9
            },
            "minItems": 9,
            "maxItems": 9
        }
    },
    "required": ["grid"]
}

def llm_predict(img):
    # Upload the image to Google GenAI
    my_file = client.files.upload(file=img)

    # Generate content using the model
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[my_file, PROMPT],
        structured_output_schema=structured_output_schema,
    )

    # Parse the response
    result = response.json()
    return result["grid"]

