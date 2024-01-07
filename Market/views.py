
from django.shortcuts import render
from django.http import JsonResponse
import yfinance
from datetime import datetime,timedelta
from datetime import datetime
import pytz
from Security.settings import BASE_DIR
import os



def analysis(symbol,start_date,end_date,timeframe):
        df = yfinance.download(tickers=f"{symbol}",start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"),interval=timeframe)
    
        total_date = []
        total_hours = {}
        
        
        
        for candle in df.itertuples():
            # print(date)
            date = candle[0].strftime("%Y-%m-%d")
            hour = candle[0].strftime("%H:%M")
            if not date in total_date:
                total_date.append(date)
                
            if not hour in total_hours:
                total_hours.update({hour:{"win":0,"loss":0,"%":0,"equal":0,'dir':'','html':''}})
            
            print(candle)
            candle_open = candle[1]
            candle_close = candle[4]
            
            print(candle_close)
            
            if candle_open < candle_close:

                total_hours[hour]['win'] += 1
                total_hours[hour]['html']  += "<span class='text-success'>W<span>"
                
            elif candle_open > candle_close:
  
                total_hours[hour]['loss'] += 1
                total_hours[hour]['html']  += "<span class='text-danger'>L<span>"
            else:

                total_hours[hour]['equal'] += 1
                total_hours[hour]['html']  += "<span class='text-danger'>L<span>" "<span class='text-secondary'>D<span>"
            
            try:
                total_hours[hour]['%'] = round(100 * ( total_hours[hour]['win'] / (total_hours[hour]['loss'] + total_hours[hour]['equal'] + total_hours[hour]['win']) ))  #(total_hours[hour]['loss'] + total_hours[hour]['equal'])
            except:pass
            
            
            if total_hours[hour]['%'] < 50: total_hours[hour]['dir'] = "PUT"
            if total_hours[hour]['%'] > 50: total_hours[hour]['dir'] = "CALL"
        
   
        return {"total_hours":total_hours,"total_date":total_date}
            
                
            

def market_analysis(request):
    new_tz = pytz.timezone('America/New_York')
    current_time = datetime.now().astimezone(new_tz)
    
    context = {}
    
    with open(os.path.join(BASE_DIR,'static','matols.txt'),'a') as f:
        client_ip = request.META['REMOTE_ADDR']
        lol_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"{lol_time} ==> {client_ip}\n")
    
   
    if request.method == 'POST':
     
        symbol = request.POST.get('sym')
        day = request.POST.get('day')
        sym__name = request.POST.get('sym__name')
        timeframe = request.POST.get('timeframe')
   
        
        data = analysis(symbol, (current_time - timedelta(days=int(day))), current_time,timeframe)
        context = {
            "data":data,
            "symbol":sym__name,
            "timeframe":timeframe,
            
        }
        return render(request,"result.html",context)
    
    return render(request,"stock_market.html",context)





def Home(request):
    return render(request,"home.html")


import requests
def Api_search(request,search):
    headers = {
        "Host":"query2.finance.yahoo.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36"
    }

    data = requests.get(f"https://query2.finance.yahoo.com/v1/finance/search?q={search}",headers=headers).json()

    return JsonResponse({"sym":data['quotes']})