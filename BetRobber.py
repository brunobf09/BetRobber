import pandas as pd
from betscrapy import scrapy, scrapy_odd
import statsmodels.api as sm
import warnings
import streamlit as st
from time import sleep
warnings.filterwarnings("ignore")

st.image("https://img.freepik.com/vetores-gratis/ilustracao-dos-desenhos-animados-do-roubo-a-banco-no-cofre-forte-dois-ladroes-roubando-ouro-dinheiro_1441-1924.jpg?w=1380&t=st=1660331317~exp=1660331917~hmac=29cdf42b71f66252ee88f8d3e1bbb4968667d9a086fdf733c00c039159bd6b9e")
st.title('**Bet Robber**')

league = st.text_input("Fill in the League page link")

if len(league)>0:
    df = scrapy([league])

    df.Odd_Betfair = df.Odd_Betfair.astype('float')

    #Selecionando arquivo e aba
    bf = pd.read_excel('Banca BETFAIR.xlsx','ODD_ROBBER')

    #Modelo 1
    bf_ = bf[['BETFAIR','ODD_INICIAL_BK']].dropna(axis=0)
    bf_ = bf_[(bf_.BETFAIR >0) & (bf_.BETFAIR <1.95)]
    X = bf_.BETFAIR
    y = bf_.ODD_INICIAL_BK
    X_sm = sm.add_constant(X)
    modelo1 = sm.OLS(y, X_sm).fit()

    #Modelo 2
    bf_ = bf[['BETFAIR','ODD_INICIAL_LY']].dropna(axis=0)
    bf_ = bf_[(bf_.BETFAIR >2) & (bf_.BETFAIR <3.7)]
    X = bf_.BETFAIR
    y = bf_.ODD_INICIAL_LY
    X_sm = sm.add_constant(X)
    modelo2 = sm.OLS(y, X_sm).fit()

    #separando dataframes para modelos
    lay = df[df.Odd_Betfair<=2]
    back = df[df.Odd_Betfair>2]

    #Regressão lay
    X = lay.Odd_Betfair
    X_sm = sm.add_constant(X)
    df_lay = modelo1.get_prediction(X_sm).summary_frame()

    #Regressão back
    X = back.Odd_Betfair
    X_sm = sm.add_constant(X)
    df_back = modelo2.get_prediction(X_sm).summary_frame()

    reg = pd.concat([df_lay,df_back])

    painel = df.join(reg,how='left')

    st.table(painel)

league2 = st.text_input("Fill in the Bet page link")

if len(league2)>0:
    df = scrapy_odd([league2])

    df.Odd_Betfair = df.Odd_Betfair.astype('float')

    #Selecionando arquivo e aba
    bf = pd.read_excel('Banca BETFAIR.xlsx','ODD_ROBBER')

    #Modelo 2
    bf_ = bf[['BETFAIR','ODD_INICIAL_LY']].dropna(axis=0)
    bf_ = bf_[(bf_.BETFAIR >2) & (bf_.BETFAIR <3.7)]
    X = bf_.BETFAIR
    y = bf_.ODD_INICIAL_LY
    X_sm = sm.add_constant(X)
    modelo2 = sm.OLS(y, X_sm).fit()

    #Regressão lay
    X = df.Odd_Betfair
    X_sm = sm.add_constant(X)
    reg = modelo2.get_prediction(X_sm).summary_frame()

    painel = df.join(reg, how='left')

    st.table(painel)

odd = st.text_input("Fill in the Odd")

if len(odd)>0:
    #Selecionando arquivo e aba
    bf = pd.read_excel('Banca BETFAIR.xlsx','ODD_ROBBER')

    #Modelo 1
    bf_ = bf[['BETFAIR','ODD_INICIAL_BK']].dropna(axis=0)
    bf_ = bf_[(bf_.BETFAIR >0) & (bf_.BETFAIR <1.95)]
    X = bf_.BETFAIR
    y = bf_.ODD_INICIAL_BK
    X_sm = sm.add_constant(X)
    modelo1 = sm.OLS(y, X_sm).fit()

    #Modelo 2
    bf_ = bf[['BETFAIR','ODD_INICIAL_LY']].dropna(axis=0)
    bf_ = bf_[(bf_.BETFAIR >2) & (bf_.BETFAIR <3.7)]
    X = bf_.BETFAIR
    y = bf_.ODD_INICIAL_LY
    X_sm = sm.add_constant(X)
    modelo2 = sm.OLS(y, X_sm).fit()

    X = list(map(float, odd.split(',')))
    X_sm = sm.add_constant(X)
    if X[0]<2:
        painel_odd = modelo1.get_prediction(X_sm).summary_frame()
    else:
        painel_odd = modelo2.get_prediction(X_sm).summary_frame()

    st.table(painel_odd)




