# Carbon Footprint Chatbot

The Carbon Footprint Chatbot is a Python-based chatbot that provides information and answers questions about reducing carbon footprints. It uses a keyword matching algorithm to analyze user input and generate appropriate responses.

## Features

- **Keyword Matching**: The chatbot utilizes a keyword matching algorithm to identify relevant keywords in user input and generate appropriate responses.

## Installation

1. Clone the repository:

    ```git clone https://github.com/DDuran19/CarbonFootprintChatBotAssistant```
2. Install the required dependencies:

    ```pip install pandas numpy```

## Usage

1. Import the necessary modules:

    ```
    import pandas as pd
    import numpy as np
    import re
    ```
2. Load the JSON data:
    ```
    RESPONSE_DATA = pd.read_json("data.json", orient='records')
    ```
3. Use the get_response() function to get the chatbot's response based on user input:
    ```
    response = get_response(user_input)
    ```
4. Run the chatbot:
    ```
    while True:
        user_input = input("You: ")
        print("Bot:", get_response(user_input))
    ```
## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.

## License
This project is licensed under the [MIT License](/LICENSE).

