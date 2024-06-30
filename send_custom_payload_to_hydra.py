import os
import hmac
import hashlib
import requests

def read_payload_from_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()


def generate_signature(payload, secret_token):
    # Encode payload and secret_token as bytes
    payload_bytes = payload.encode('utf-8')
    secret_token_bytes = secret_token.encode('utf-8')
    
    # Create HMAC SHA256 signature
    hmac_obj = hmac.new(secret_token_bytes, msg=payload_bytes, digestmod=hashlib.sha256)
    signature = "sha256=" + hmac_obj.hexdigest()
    return signature


def send_post_request(url, payload, signature):
    headers = {
        'Content-Type': 'application/json',
        'X-GitHub-Event': 'custom',
        'X-Hub-Signature-256': signature
    }
    
    print("Sending POST Request....")
    response = requests.post(url, headers=headers, data=payload)
    return response


def main():
    try:
        url = "https://api.enterprise.redhat.com/hydra/umb-bridge/v1/publish"
        payload = read_payload_from_file('payload.json')
        secret_token = os.getenv('SECRET_TOKEN')  # Retrieve secret token from environment variable
        if secret_token is None:
            raise ValueError("Secret token not found in environment variables.")
        
        signature = generate_signature(payload, secret_token)
        print("Generated Signature:", signature)
        
        response = send_post_request(url, payload, signature)
        if response:
            print("Request Successful!")
        else:
            print("Request Failed!")

        print("Response Status Code:", response.status_code)
        print("Response Body:", response.text)
            
    except Exception as e:
        print("Error:", e)


if __name__ == '__main__':
    main()
