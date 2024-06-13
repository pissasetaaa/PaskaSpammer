import requests
import time
import threading

# Function to create webhooks
def create_webhooks(bot_token, channel_id, num_webhooks):
    headers = {
        'Authorization': f'Bot {bot_token}',
        'Content-Type': 'application/json'
    }
    webhook_urls = []
    for i in range(num_webhooks):
        data = {'name': f'PASKASPAMMER{i+1}'}
        response = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/webhooks', headers=headers, json=data)
        webhook = response.json()
        webhook_urls.append(f'https://discord.com/api/webhooks/{webhook["id"]}/{webhook["token"]}')
        print(f'Created webhook {i+1}')
    return webhook_urls

# Function to send messages
def send_messages(webhook_urls, message, interval):
    def send_message(webhook_url):
        payload = {'content': message}
        response = requests.post(webhook_url, json=payload)
        print(f'Sent: {response.status_code} using webhook {webhook_url}')
    
    while True:
        threads = []
        for webhook_url in webhook_urls:
            thread = threading.Thread(target=send_message, args=(webhook_url,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        if interval > 0:
            time.sleep(interval)

print(""" 
                      __                                                       
    ____  ____ ______/ /______ __________  ____ _____ ___  ____ ___  ___  _____
   / __ \\/ __ `/ ___/ //_/ __ `/ ___/ __ \\/ __ `/ __ `__ \\/ __ `__ \\/ _ \\/ ___/
  / /_/ / /_/ (__  ) ,< / /_/ (__  ) /_/ / /_/ / / / / / / / / / / /  __/ /    
 / .___/\\__,_/____/_/|_|\\__,_/____/ .___/\\__,_/_/ /_/ /_/_/ /_/ /_/\\___/_/     
/_/                              /_/                                           
""") 

def menu():
    print("Welcome to the Discord Webhook Spammer")
    bot_token = input("Enter your bot token: ")
    channel_id = input("Enter the channel ID: ")
    num_webhooks = int(input("Enter the number of webhooks to create: "))
    message = input("Enter the message to spam: ")
    interval = float(input("Enter the interval between messages (in seconds, can be 0): ")) / 10  # Ten times faster

    print("\nCreating webhooks...")
    webhook_urls = create_webhooks(bot_token, channel_id, num_webhooks)
    print(f"Created {len(webhook_urls)} webhooks successfully!")

    print("\nStarting to send messages...")
    send_messages(webhook_urls, message, interval)

# Run the menu
menu()
