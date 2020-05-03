import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import pandas_datareader as web
import streamlit as st

yf.pdr_override()

ibovespa_list = pd.read_csv("lista_ibovespa.csv", sep = ";", 
                            encoding = 'utf-8').drop(columns=["Qtde. Teórica"])

ibovespa_list = ibovespa_list.rename(columns = {"Código\xa0":"Symbol", 
                                                "Ação": "Company", 
                                                "Tipo":"Type", 
                                                "Part. (%)": "Share (%)"})
company_code = ibovespa_list["Symbol"]

#O atributo é composto pela sigla do papel mais um sufixo .SA, por ex.: ABEV3.SA
def symbol(imputer):
    imputer = str(imputer) + ".SA"
    return imputer

def company_series(imputer):
    series = web.get_data_yahoo(symbol(imputer))
    series = series["Close"]
    if periods == "2015":
        series = series[(series.index.year >= 2015)]
    if periods == "2016":
        series = series[(series.index.year >= 2016)]
    if periods == "2017":
        series = series[(series.index.year >= 2017)]
    if periods == "2018":
        series = series[(series.index.year >= 2018)]
    if periods == "2019":
        series = series[(series.index.year >= 2019)]
    if periods == "2020": 
        series = series[(series.index.year >= 2020)]
    return series

def company_name(imputer):
    name = ibovespa_list.set_index("Symbol")
    name = name.loc[imputer][0]
    return name

def share(imputer): 
    share = ibovespa_list.set_index("Symbol")
    share = share.loc[imputer][2]
    return share[:-1]
    
    
def graph(moving_average):
    plt.style.use('seaborn')
    plt.figure(figsize=(12,8))
    company_series(imputer).plot(label = company_name(imputer), linewidth = 2.0)
    if "Média Móvel de 9" in moving_average:
        company_series(imputer).rolling(9).mean().plot(label = "MM 09", linewidth=1.0) 
    if "Média Móvel de 21" in moving_average:
        company_series(imputer).rolling(21).mean().plot(label = "MM 21", linewidth=1.0)
    if "Média Móvel de 200" in moving_average:
        company_series(imputer).rolling(200).mean().plot(label = "MM 200", linewidth=1.0, marker = "*")   
    plt.title("Gráfico da " + imputer, fontsize = 25, pad = 20)
    plt.ylabel("Preço do lote", labelpad = 10)
    plt.xlabel("Período", labelpad = 10)
    plt.legend()
    return st.pyplot()

def main():
     st.title("Análise da ação ")    
     st.header(company_name(imputer))
     st.text("Responsável por " + share(imputer) +"% do índice IBOVESPA.")
     moving_average = st.sidebar.multiselect("Deseja adicionar quais médias móveis? ", 
                                     ("Média Móvel de 9", 
                                      "Média Móvel de 21",
                                      "Média Móvel de 200"))
     graph(moving_average)
     plt.title("Distribuição do preço", fontsize = 25, pad = 20)
     company_series(imputer).hist(bins = 40, ec = "k", alpha = .6)
     st.pyplot()
     mean = company_series(imputer).mean()
     st.info(f"A média do preço da ação no período é de: R${mean: .2f}")

if st.sidebar.checkbox("O que é Índice Ibovespa?"):
    st.sidebar.text("   O Ibovespa é o principal indicador de \ndesempenho das ações negociadas na B3 e\nreúne as empresas mais importantes do\nmercado de capitais brasileiro.")

st.sidebar.title("Empresas que compõe o índice IBOVESPA: ")
imputer = st.sidebar.selectbox("Escolha uma das empresas: ", options = (company_code))
periods = st.sidebar.selectbox("Análise gráfica a partir de que ano? ", options = ("2015", "2016", 
                                                                                   "2017", "2018", 
                                                                                   "2019", "2020"))
     
if __name__ == "__main__":
    main()
 


