import requests

class SendMessage:
    def __init__(self):
        self.triggers = {
            "sms": "text_nathan",
            "email": "email_nathan",
        }
        self.IFTTT_KEY = "cA6SJcKRjiMKvcbQWazyQO"
        self.IFTTT_URL = "https://maker.ifttt.com/trigger/"

    def send_message(self, msg: str, trigger: str=False):
        if not trigger:
            trigger = self.triggers["email"]

        api_endpoint = f"{self.IFTTT_URL}{trigger}/with/key/{self.IFTTT_KEY}"
        # message syntax: {value1} on {Occurred At}
        parameters = {"value1": msg}
        
        print(msg)
        try:
            text_response = requests.get(url=api_endpoint, params=parameters)
            text_response.raise_for_status()
        except Exception as e:
            print(e)
        else:
            print(text_response.status_code)
        

if __name__ == "__main__":
    # test sms message
    sms = SendMessage()

    sms.send_message("Test text message")
    
    
