import pandas as pd
# from nsepython import nse_optionchain_scrapper
from models import Token
from smartapi import SmartConnect
from config import *

# def get_next_expiry():
#     payload = nse_optionchain_scrapper("BANKNIFTY", )
#     df = pd.DataFrame({'Date': payload['records']['expiryDates']})
#     expiry = df['Date'].iloc[0]
#     expiry = expiry.split('-')
#     expiry = expiry[0]+expiry[1].upper() +str(2)+expiry[2][-1]
#     return expiry

def get_token(expiry):
    # expiry = get_next_expiry()
    import requests
    BASE_URL = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
    data = requests.get(BASE_URL)
    df = data.json()
    strike = 20000
    EXPIRY = expiry
    symbol = []
    token = []

    for item in range(300):
        symbolce = 'BANKNIFTY' + EXPIRY + str(strike) + 'CE'
        symbolpe = 'BANKNIFTY' + EXPIRY + str(strike) + 'PE'
        for items in df:
            for key, value in items.items():
                if value == symbolce:
                    tokenc = items['token']
                    symbol.append(symbolce)
                    token.append(tokenc)
                if value == symbolpe:
                    tokenp = items['token']
                    symbol.append(symbolpe)
                    token.append(tokenp)

        strike += 100
    print(symbol)
    df1 = pd.DataFrame(symbol, columns=['Symbol'])
    df2 = pd.DataFrame(token, columns=['Token'])
    df1 = df1.join(df2)
    return df1

def find_token(tradingsymbol,df):
    token = ''
    for num in range(len(df)):
        if df['Symbol'][num] == tradingsymbol:
            token = df['Token'][num]
    return token

def add_symbol(expiry):
    symbol = []

    df = get_token(expiry)
    for item in range(len(df)):
        tradingsymbol = df['Symbol'][item]
        token = df['Token'][item]
        tsymbols = [tradingsymbol,token,expiry]
        symbol.append(tsymbols)
    return symbol

def add_symbol_to_database(expiry):
    symbol = add_symbol(expiry)
    tokens = []
    for item in symbol:
        token = Token(symbol=item[0],tokens = item[1],expiry=item[2])
        db.session.add(token)
        db.session.commit()

def order():
    API_KEY = '1LfHsCtr'
    obj=SmartConnect(api_key=API_KEY,)
                    #optional
                    #access_token = "your access token",
                    #refresh_token = "your refresh_token")
    print(obj)
    USERID= ''
    PASSWORD = ''
    data = obj.generateSession(USERID,PASSWORD)

    refreshToken= data['data']['refreshToken']

    feedToken=obj.getfeedToken()

    userProfile= obj.getProfile(refreshToken)
    return obj

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    expiry = '15JUL21'
    add_symbol_to_database(expiry)


