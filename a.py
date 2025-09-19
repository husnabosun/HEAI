from django.http import JsonResponse
import pymupdf
import pandas as pd

df_list = []
column_names = None


def get_df(doc):
    page = doc[0]
    tables = (page.find_tables()).tables

    if tables:
        table = tables[0]
        raw_data = table.extract()
        # df = table.to_pandas()

        column_names = raw_data[0]
        data = raw_data[1:]


        df = pd.DataFrame(data, columns=column_names)

        df_list.append(df)
    
    full_df = pd.concat(df_list, ignore_index=True)
    without_date_filtered_df = full_df.drop(columns='Tarih').iloc[:20]
    
    test_results = []
    for i in range(20):
        name = without_date_filtered_df.loc[i]['Tahlil']
        if ',' in without_date_filtered_df.loc[i]['Sonuç']:
            result = float(without_date_filtered_df.loc[i]['Sonuç'].replace(",", "."))
        else:
            result = without_date_filtered_df.loc[i]['Sonuç']
        health_range = without_date_filtered_df.loc[i]['Referans\nDeğeri']
        
        a = {'Tahlil' : name, 'Sonuç' : result, 'Referans Değeri': health_range}
        test_results.append(a)

    return JsonResponse(test_results, safe=False)

doc = pymupdf.open("b.pdf")
def analyze_results(test_results):
    for i in test_results:
        range_raw = i['Referans Değeri']
        parts = range_raw.split("-")

        ceil = float(parts[0].replace(",", "."))
        floor = float(parts[1].replace(",", "."))
        
        name = i['Tahlil']
        result = i['Sonuç']
        
        if type(result) != float:
            continue
        else:
            if result >= ceil and result <=floor:
                print(f"{name} Değeriniz Sağlıklı Aralıktadır.\nSonuç:{result} İdeal Aralık:{ceil}-{floor}")
            else:
                print(f"{name} Değeriniz Sağlıklı Aralıkta Değildir.\nSonuç:{result} İdeal Aralık:{ceil}-{floor}")
                
test_results = get_df(doc)
print(test_results)
#analyze_results(test_results)