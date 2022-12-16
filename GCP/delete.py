from datetime import datetime, timedelta
import requests

userExists = requests.get(f'https://kinideas-profile-vdzflryflq-ew.a.run.app/subscribedUsers/gZkd8CJAxESJpJFmXRLnU0IFkhE3')
if userExists.status_code == 200:
    susbscriptionType = userExists.json()['subscription_type']
    lastUpdate = userExists.json()['updated_at']
    expireDate = lastUpdate + timedelta(days = 30)
    now = str(datetime.now())[:len(expireDate)]
    if now <= expireDate:
        print("Not expired")