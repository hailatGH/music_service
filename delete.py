from datetime import datetime
import requests

userExists = requests.get(f'https://kinideas-profile-vdzflryflq-ew.a.run.app/subscribedUsers/gZkd8CJAxESJpJFmXRLnU0IFkhE3')
userData = userExists.json()['subscription_expiry_date'].replace("T", " ").replace("Z", "")
now = str(datetime.now())[:len(userData)]
print(userData)
print(now)
# print(datetime.today())
if userData > now:
    print(True)
else:
    print(False)