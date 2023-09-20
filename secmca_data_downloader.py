from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
import pandas as pd

def secmca_download_csv(serie, start_year, end_year, country_list):
    path = secmca_data_path(serie, start_year, end_year, country_list)

    if path:
        df = secmca_json_to_csv(serie, path, start_year)
        return df
    else:
        return

def secmca_data_path(serie, start_year, end_year, country_list):

    country_num_dic = {"Costa Rica":3, "El Salvador":13,"Guatemala":50,"Honduras":17,"Nicaragua":4,"República Dominicana":52,"Panamá":161}

    parent = "https://www.secmca.org/"
    type_request = "jsonpage/"
    json_view = "jsonview=true&"
    url_country_num = "-".join(map(str, [country_num_dic[c] for c in country_list])) + "/"
    date_range = '-'.join(f'{year}{month}' for year in range(start_year, end_year + 1) for month in range(1, 13))

    if serie == "IPC":
        serie_parent = "?parent=Precios&scid=0&cid=0&scsid=0&"
        serie_son = "son=%C3%8Dndice%20de%20precios%20al%20consumidor&"
        url_start = "url=1/14/"
        url_end = "-&all_vars=1|IPC%20general"
        country_suff = "39/265/19-258/78/"

    elif serie == "TCN":
        serie_parent = "?parent=Tipos%20de%20cambio&scid=0&cid=3&scsid=undefined&"
        serie_son = "son=Tipo%20de%20cambio%20de%20mercado&"
        url_start = "url=29/238/"
        url_end = "-&all_vars=1|Tipo%20de%20cambio%20de%20compra%20promedio%20del%20mes"
        country_suff = "39/269-270/263-264/232/"

    else:
        print(f" ERROR: Valor de SERIE {serie} no includo, debe eser TCN o IPC")
        return None

    path = parent + type_request + serie_parent + serie_son + json_view + url_start + url_country_num + country_suff + date_range + url_end

    return path

def secmca_json_to_csv(serie_code, path, start_year):

    start_date = datetime(start_year, 1, 1)
    end_date = datetime.now()

    month_translation = {'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo','April': 'Abril', 'May': 'Mayo', 'June': 'Junio', 'July': 'Julio','August': 'Agosto', 'September': 'Setiembre', 'October': 'Octubre','November': 'Noviembre', 'December': 'Diciembre'}
    month_year_list = [f"{date.strftime('%Y')}-{month_translation[date.strftime('%B')]}" for date in [start_date + relativedelta(months=i) for i in range(0, (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month + 1))]]

    try:
        response = requests.get(path)
        content = response.json()

        result = []
        for idx, dic in pd.DataFrame.from_dict(content).iterrows():
            df = pd.DataFrame(columns = dic.index, index = month_year_list)
            for key, inner_dict in dic.items():
                serie = pd.DataFrame.from_dict(inner_dict, orient="index")
                if 'valorCalculado' in serie:
                    df[key] = serie['valorCalculado']
            result.append(df)

        for idx, df in enumerate(result):
            display(df)
            file_name = f"{serie_code}_{idx + 1}.csv"
            df.to_csv(file_name, index=False)

        return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
