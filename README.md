# TON Transactions Viewer

Welcome to the TON Transactions Viewer script! This tool allows you to check and display transaction details on the TON (The Open Network) blockchain.

## Features

- **Check TON Wallet Balance**: Retrieve and display the balance of a given TON wallet.
- **Fetch Recent Transactions**: List the recent transactions for a specific TON wallet.
- **Convert TON to USD**: Display the value of transactions and balances in USD.
- **Save Transactions**: Save transaction details to a text file for later reference.
- **Visit GitHub**: Open the GitHub repository for this project.

## Prerequisites

To run this script, you need to have the following:

- Python 3.6 or later
- `pip` (Python package installer)
- API Key from TON API

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/sayh3x/TON-Transactions-Viewer.git
    cd TON-Transactions-Viewer
    ```

2. **Install required Python packages**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:

    Create a `.env` file in the root directory of the project and add your TON API key:

    ```env
    TON_API_KEY=your_ton_api_key_here
    ```

## Getting TON API Key

1. **Sign up for an account** on [TON API](https://tonapi.io/).
2. **Generate an API Key** from the dashboard after logging in.
3. **Add the API Key** to the `.env` file as described above.

## Usage

1. **Run the script**:

    ```bash
    python ton_transactions_Viewer.py
    ```

2. **Follow the prompts** to enter a TON wallet address and perform various actions such as checking balance, viewing recent transactions, saving transaction details, etc.

## Example Commands

- **Check Balance**: Enter a TON wallet address when prompted.
- **View Recent Transactions**: Enter the wallet address and the script will list the recent transactions.
- **Save Transactions**: After viewing transactions, enter "save" to save the details to a file.
- **Exit the Script**: Enter "exit" to close the script.

## Contributing

We welcome contributions to this project. Feel free to open issues or submit pull requests.

---

Developed by 

## Additional Instructions

Make sure to replace `https://github.com/sayh3x/TON-Transactions-Viewer.git` with the actual URL of your GitHub repository.
‍