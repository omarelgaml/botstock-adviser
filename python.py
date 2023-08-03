import requests
import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import sys
import yfinance as yf
#########################################
def getcompaniesData(ticker_list):
    output_data = []
    # ticker_list = ['AAPL', 'META', 'MMM']#, 'GOOGL','META','GOOG','TSLA'] 
    for ticker in ticker_list:
        json_object = create_json_object(ticker)
        
        if json_object:
            output_data.append(json_object)
    return output_data


#########################################
def getRevenueData(ticker):
    url = f'https://financialmodelingprep.com/api/v3/income-statement/{ticker}?'
    parameters = {
        'limit': 100,
        'apikey':'a4ff4fe833047d87c2056c6fca36aa63'
    }
    response = requests.get(url, params=parameters)
    if response.status_code == 200:
        filtered_list = [filter_json(json_obj) for json_obj in response.json()]
        return filtered_list
    else:
        return None

#########################################

def getHeadlines(company):
    url = 'https://newsapi.org/v2/everything?'
    parameters = {
        'q': company, 
        'pageSize': 100,  
        'from':'2023-07-31',
        'to':'2023-07-31',
        'language':'en',
        'apiKey': '04cf3f29274c44519846bc7a3ecb6654' 
    }
    response = requests.get(url, params=parameters)
    

    response_json = response.json()
    if response.status_code == 200:
        return extract_fields(response_json['articles'], 'title')
    else:
        return None
#########################################
def extract_fields(dict_list, key):
    return [item.get(key) for item in dict_list]
#########################################

def getCompanyName(ticker):
    company = yf.Ticker(ticker)

    company_name = company.info['shortName']
    return company_name.split(' ')[0]
#########################################

def create_json_object(ticker):
    revenue = getRevenueData(ticker)
    companyName = getCompanyName(ticker)
    headlines = getHeadlines(companyName)

    
    return {
        'ticker': ticker,
        'revenue': revenue,
        'headlines': headlines[:50]
    }


#########################################

def filter_json(json_obj):
    return {
        "symbol": json_obj["symbol"],
        "reportedCurrency": json_obj["reportedCurrency"],
        "calendarYear": json_obj["calendarYear"],
        "period": json_obj["period"],
        "revenue": json_obj["revenue"],
        "costOfRevenue": json_obj["costOfRevenue"],
        "grossProfit": json_obj["grossProfit"],
        "grossProfitRatio": json_obj["grossProfitRatio"],
        "interestIncome": json_obj["interestIncome"],
        "interestExpense": json_obj["interestExpense"],
        "depreciationAndAmortization": json_obj["depreciationAndAmortization"],
        "operatingIncome": json_obj["operatingIncome"],
        "operatingIncomeRatio": json_obj["operatingIncomeRatio"],
        "totalOtherIncomeExpensesNet": json_obj["totalOtherIncomeExpensesNet"],
        "netIncome": json_obj["netIncome"],
        "netIncomeRatio": json_obj["netIncomeRatio"],
    }
#########################################

def main(user_input):
    return('done')

if __name__ == "__main__":
    tickers= sys.argv[1]
    jsons = getcompaniesData(tickers.split(','))
    chat = ChatOpenAI(temperature = 0,openai_api_key="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")
    answer = chat([HumanMessage(content=f'''Act as a financial analyst. You will be provided with an array of JSONs for companies, each containing the annual revenue for 5 years and news headlines. Your task is to give long-term and short-term recommendations for these companies\' stocks, using the provided data. Utilize the strategies of "Stock Selection," "Pair Trading," and "Market Timing" to formulate your recommendations. Combine the results and provide a very brief long-term recommendation and short-term recommendations, indicating whether to sell or buy. Please include a concise explanation for your recommendations.
    {jsons}''')])
    print(answer.content)



