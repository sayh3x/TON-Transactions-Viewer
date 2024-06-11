# import library
from dotenv import load_dotenv
from colorama import Fore
import pyfiglet as pyg
import time, os, requests, logging, webbrowser, sys, shutil

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set TON_API_KEY using environment variable or default value
TON_API_KEY = os.getenv('TON_API_KEY')

VERSION = "1.0.1"
GITHUB_URL = "https://github.com/sayh3x/TON-Transactions-Viewer"

received_transactions = []
wallet_address = ""
ton_to_usd_rate = 0
is_checking_transactions = False

# Function for Clear Terminal 
def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def log_and_animate(message, duration=3, interval=0.5, level='INFO', mote='.'):
    log_message = f'{time.strftime("%Y-%m-%d %H:%M:%S")} - {level} - {message}'
    print(log_message, end='', flush=True)

    end_time = time.time() + duration
    while time.time() < end_time:
        for dots in range(4):
            sys.stdout.write(f'\r{log_message}{mote * dots}{" " * (3 - dots)}')
            sys.stdout.flush()
            time.sleep(interval)
    sys.stdout.write(f'\r{log_message}{mote * 3}\n')
    sys.stdout.flush()

# Check Target TON Balance
def check_ton_balance(address, retries=3, delay=5):
    api_url = f"https://tonapi.io/v1/account/getInfo?account={address}"

    for attempt in range(retries):
        try:
            response = requests.get(api_url)
            data = response.json()

            if 'balance' in data:
                balance = int(data["balance"]) / 1e9  # Convert to TON
                return balance
            else:
                logging.error("Error getting balance: %s", data.get("message", "Unknown error"))
                return 0
        except Exception as e:
            if attempt < retries - 1:
                logging.error(f"Error checking balance, retrying in {delay} seconds: {str(e)}")
                time.sleep(delay)
            else:
                logging.error("Error checking balance: %s", str(e))
                return 0

# Get Wallet Transactions
def get_wallet_received_transactions(wallet_address):
    url = f"https://tonapi.io/v1/account/getTransactions?account={wallet_address}&limit=50&sort=-timestamp"
    
    try:
        response = requests.get(url)
        data = response.json()

        if 'transactions' in data:
            transactions = data["transactions"]
            received_transactions = [{"value": tx["value"], "to": tx["to"], "tx_hash": tx["hash"], "from": tx["from"], "timestamp": tx["utime"]} for tx in transactions if tx["to"] == wallet_address]
            return received_transactions
        else:
            logging.error("Error: %s", data.get("message", "Unknown error"))
            return None
    except Exception as e:
        logging.error("An error occurred: %s", e)
        return None

# Get TON price with api.coingecko.com api
def get_ton_price():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=toncoin&vs_currencies=usd")
        data = response.json()
        ton_price = data["toncoin"]["usd"]
        return ton_price
    except Exception as e:
        logging.error("Error fetching TON price: %s", str(e))
        return None

# Convert TON to USD with api
def convert_to_usd(ton_amount, ton_to_usd_rate):
    return ton_amount * ton_to_usd_rate

# Add title for terminal
def set_terminal_title(title):
    os.system(f"echo -n \"\\033]0;{title}\\007\"")

# View output in terminal 
def display_transactions(transactions, ton_to_usd_rate):
    for tx in transactions:
        value_in_ton = int(tx["value"]) / 1e9  # Convert from nanoton to TON
        usd_value = convert_to_usd(value_in_ton, ton_to_usd_rate)
        lower_sender_address = tx["from"]
        len_address = len(lower_sender_address)
        mid_point = len_address // 2

        balance = check_ton_balance(address=lower_sender_address)
        balance_in_usd = convert_to_usd(balance, ton_to_usd_rate)

        set_terminal_title(f"Sender Address: {lower_sender_address}")

        print()
        for i in range(len_address):
            if i == mid_point:
                print(f"'{lower_sender_address}'", end='')
            else:
                print('-', end='')
        print('\n')
        print(f"Send Value: {value_in_ton} TON")
        print(f"TON Balance: {balance}")
        print(f"Convert TON to USD: {balance_in_usd}\n")

        print("-" * (len_address * 2))
        print()

# Function for fast save Transactions file
def save_transactions(transactions, ton_to_usd_rate, privios):
    log_and_animate(f'Save transactions in {privios}.txt ', level='Waiting', mote='#')
    if not os.path.exists('ton_log'):
        os.makedirs('ton_log')
                
    with open(os.path.join('ton_log', f'{privios}.txt'), 'w') as file:
        for tx in transactions:
            value_in_ton = int(tx["value"]) / 1e9  # Convert from nanoton to TON
            usd_value = convert_to_usd(value_in_ton, ton_to_usd_rate)
            file.write(f"Transaction Hash: {tx['tx_hash']}\n")
            file.write(f"Value: {value_in_ton} TON\n")
            file.write(f"Value in USD: {usd_value}\n")
            file.write(f"From: {tx['from']}\n")
            file.write(f"To: {tx['to']}\n")
            file.write(f"Timestamp: {tx['timestamp']}\n")
            file.write("\n")

# Check Main Wallet Transaction
def check_wallet(text_input='Enter TON Wallet (enter 0 to visit GitHub): ', privios=None):
    global received_transactions, wallet_address, ton_to_usd_rate, is_checking_transactions

    print(Fore.GREEN)
    try:
        wallet_address = input(text_input); print(Fore.RESET)
        # Open Github repository 
        if wallet_address == '0':
            clear()
            log_and_animate("Opening GitHub repository ", level='Waiting', mote='*', duration=1)
            webbrowser.open(GITHUB_URL)
            check_wallet(text_input='Enter TON Wallet for exit (Enter 00): ')
        # Delet Transactions save folder
        elif wallet_address == 'del' or wallet_address == 'rem':
            log_and_animate('Removing ', level='Waiting', mote=';D')
            dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ton_log')
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                main(sayh3x=f"Folder {dir_path} has been removed.")
            else:
                main(sayh3x="i Can't find 'ton_log' folder")
        # Exit in Script 
        elif wallet_address == 'exit' or wallet_address == '00':
            clear()
            log_and_animate(Fore.YELLOW + "Bye ;", level='Exit', mote=')')
            sys.exit()
        # Save Transactions in file
        elif wallet_address == 'save':
            if received_transactions:
                save_transactions(received_transactions, ton_to_usd_rate, privios=privios)
                main(sayh3x=f"Save in path {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ton_log')}")
            else:
                main(sayh3x='Please Enter address wallet\r\nand after enter wallet enter "save".')

        log_and_animate('Checking wallet transactions')
        is_checking_transactions = True

        received_transactions = get_wallet_received_transactions(wallet_address)
        if received_transactions:
            logging.info("Received Transactions:")
            ton_to_usd_rate = get_ton_price() or 0
            display_transactions(received_transactions, ton_to_usd_rate)
            generate_logo(text_info=f'{Fore.GREEN}Completed enter "save" {Fore.RED}!!!{Fore.RESET}')
            check_wallet(privios=wallet_address)
        else:
            log_and_animate("No transactions found or 'Check Api Key'", level='Problem', mote='!')
    
    except KeyboardInterrupt:
        generate_logo(text_info='For Exit Enter "exit" or File"save"')
        check_wallet(text_input='Enter TON Wallet: ', privios=wallet_address)
    finally:
        is_checking_transactions = False

# Add Logo in terminal 
def generate_logo(text_info=''):
    clear()
    logo = pyg.figlet_format('TON Viewer', font='slant')
    print(Fore.BLUE + logo + Fore.RESET)
    
    if len(text_info) > 0:
        print(Fore.RED+f'\n{text_info}\n')

    print(Fore.RED + "𝘋𝘦𝘷𝘦𝘭𝘰𝘱𝘦𝘥 𝘣𝘺 𝙃3𝙓" + Fore.RESET)
    print(Fore.YELLOW + "Version: " + VERSION + Fore.RESET)

# Main Function
def main(sayh3x=''):
    generate_logo(text_info=sayh3x)
    check_wallet()

# Run
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess stopped by user (Ctrl+C)")
        sys.exit()
