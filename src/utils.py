
from src.models.stock_info import StockInfo
from fastapi import APIRouter, Request
import yfinance as yf
from bs4 import BeautifulSoup
import re
import requests
from src.prompt.stock_prompt_template import prompt


backend_router = APIRouter()

def get_llm_client(request: Request):
    return {"llm": request.app.state.llm, "client": request.app.state.client}

def get_company_info(query: str , llm_dependency: dict) -> StockInfo:
    client = llm_dependency["client"]
    
    resp = client.chat.completions.create(
        model="llama3.1",
        messages=[
            {
                "role": "user",
                "content": f"Return the company name and the ticker symbol of the {query}."
            }
        ],
        response_model=StockInfo,
        max_retries=10
    )
    return resp


def get_stock_price(ticker,history=5):
    # time.sleep(4) #To avoid rate limit error
    if "." in ticker:
        ticker=ticker.split(".")[0]
    ticker=ticker+".NS"
    stock = yf.Ticker(ticker)
    df = stock.history(period="1y")
    df=df[["Close","Volume"]]
    df.index=[str(x).split()[0] for x in list(df.index)]
    df.index.rename("Date",inplace=True)
    df=df[-history:]
    # print(df.columns)
    
    return df.to_string()

# Script to scrap top5 googgle news for given company name

def google_query(search_term):
    if "news" not in search_term:
        search_term=search_term+" stock news"
    url=f"https://www.google.com/search?q={search_term}&cr=countryIN"
    url=re.sub(r"\s","+",url)
    return url

def get_recent_stock_news(company_name):
    # time.sleep(4) #To avoid rate limit error
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

    g_query=google_query(company_name)
    res=requests.get(g_query,headers=headers).text
    soup=BeautifulSoup(res,"html.parser")
    news=[]
    for n in soup.find_all("div","n0jPhd ynAwRc tNxQIb nDgy9d"):
        news.append(n.text)
    for n in soup.find_all("div","IJl0Z"):
        news.append(n.text)


    if len(news)>6:
        news=news[:4]
    else:
        news=news
    news_string=""
    for i,n in enumerate(news):
        news_string+=f"{i}. {n}\n"
    top5_news="Recent News:\n\n"+news_string
    
    return top5_news




def get_financial_statements(ticker):
    if "." in ticker:
        ticker=ticker.split(".")[0]
    else:
        ticker=ticker
    ticker=ticker+".NS"    
    company = yf.Ticker(ticker)
    balance_sheet = company.balance_sheet
    if balance_sheet.shape[1]>=3:
        balance_sheet=balance_sheet.iloc[:,:3]    # Remove 4th years data
    balance_sheet=balance_sheet.dropna(how="any")
    balance_sheet = balance_sheet.to_string()
    
    # cash_flow = company.cash_flow.to_string()
    # print(balance_sheet)
    # print(cash_flow)
    return balance_sheet

def Anazlyze_stock(query,llm_dependency: dict ):
    #agent.run(query) Outputs Company name, Ticker
    resp=get_company_info(query,llm_dependency)
    print({"Query":query,"Company_name":resp.company,"Ticker":resp.ticker})
    stock_data=get_stock_price(resp.ticker,history=10)
    stock_financials=get_financial_statements(resp.ticker)
    stock_news=get_recent_stock_news(resp.company)

    available_information=f"Stock Price: {stock_data}\n\nStock Financials: {stock_financials}\n\nStock News: {stock_news}"
    # available_information=f"Stock Financials: {stock_financials}\n\nStock News: {stock_news}"

    print("\n\nAnalyzing.....\n")
    analysis=llm_dependency['llm'](prompt.format(query=query,company=resp.company,available_information=available_information))       
    print(analysis)

    return analysis