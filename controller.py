from flask import render_template,request,redirect,url_for,session,Response
from config import app
from views import *
from models import Token
import time,threading
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

@app.route('/' , methods = ['GET'])
def home():
    return render_template('base.html')

@app.route('/straddle', methods = ['GET'])
def straddle():
    obj = order()

    ltp = obj.ltpData(exchange='NSE', tradingsymbol='BANKNIFTY', symboltoken='26009')
    ltp = ltp['data']['ltp']
    ltp = round(ltp / 100) * 100
    print(ltp)
    expiry = '15JUL21'
    ce = 'BANKNIFTY' + expiry + str(ltp) + 'CE'
    pe = 'BANKNIFTY' + expiry + str(ltp) + 'PE'
    t1 = Token.query.filter_by(symbol=ce).first()
    t2 = Token.query.filter_by(symbol=pe).first()

    tokence = t1.tokens
    tokenpe = t2.tokens
    ltpce = obj.ltpData(exchange='NFO', tradingsymbol=ce, symboltoken=tokence)
    ltpce = ltpce['data']['ltp']
    ltppe = obj.ltpData(exchange='NFO', tradingsymbol=pe, symboltoken=tokenpe)
    ltppe = ltppe['data']['ltp']
    session['ltpce'] = ltpce
    session['CE'] = ce
    session['PE'] = pe
    session['ltpce'] = ltppe
    straddlelist = [{'symbol': ce, 'ltp':ltpce,'profit': 0,'token':tokence},
                    {'symbol': pe, 'ltp':ltppe,'profit': 0,'token':tokenpe}]
    # session['obj'] = obj
    return render_template('home.html',  straddlelist = straddlelist ,CE = ce,PE = pe)


def straddle_list():
    ce = session['CE']
    print(ce)
    pe = session['PE']
    obj = order()
    ltpce = session['ltpce']

    ltppe = session['ltpce']
    t1 = Token.query.filter_by(symbol= ce).first()
    t2 = Token.query.filter_by(symbol=pe).first()
    tokence = t1.tokens
    tokenpe = t2.tokens

    letce = obj.ltpData(exchange='NFO', tradingsymbol=ce, symboltoken=tokence)
    letce = letce['data']['ltp']
    letpe = obj.ltpData(exchange='NFO', tradingsymbol=pe, symboltoken=tokenpe)
    letpe = letpe['data']['ltp']
    profitce = (letce-ltpce)*25
    profitpe = (letpe - ltpce)*25
    straddlelist = [{'symbol': ce, 'ltp': ltpce, 'profit': profitce, 'token': tokence},
                    {'symbol': pe, 'ltp': ltppe, 'profit': profitpe, 'token': tokenpe}]

    return straddlelist




@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()

def update_load():
    with app.app_context():
        while True:
            time.sleep(5)
            straddlelist = straddle_list()
            turbo.can_stream(turbo.update(render_template('home.html',straddlelist=straddlelist), target = 'load'))

# if __name__ == '__main__':


    # before_first_request()
    # ltpce = obj.ltpData(exchange='NFO', tradingsymbol=ce, symboltoken=tokence)
    # ltpce = ltpce['data']['ltp']
    # ltppe = obj.ltpData(exchange='NFO', tradingsymbol=pe, symboltoken=tokenpe)
    # ltppe = ltppe['data']['ltp']
    # print(ltpce)
    # print(ltpce)