import pandas as pd
import numpy as np
from numpy.linalg import norm
from datetime import datetime
from matplotlib import pyplot as plt


def load_data(filename, idx="date"):  # Load data & preprocessing
    stock_data = pd.read_csv(filename, encoding= "UTF-8", index_col=idx)
    stock_data = (stock_data - stock_data.min()) / (stock_data.max() - stock_data.min())
#     stock_data = (stock_data - stock_data.mean()) / stock_data.std()
    stock_data = stock_data.astype(float)
    dates = stock_data.index.tolist()
    return stock_data, dates


def get_code_data(stock_data, days=90):  # get_input_code_data
    while True:
        try:
            analysis_code = input("Input analaysis code: ")
            analysis_data = stock_data[analysis_code]
            analysis_data = analysis_data[-days:]
            break
        except KeyError:
            print("This code does not exist.")

    return analysis_data, analysis_code


def euclidean_dis(analysis_data, compare_data):
    #     distance = sqrt(sum(pow(a_data - c_data, 2) for a_data, c_data in zip(analysis_data, compare_data)))
    analysis_data = analysis_data.to_numpy()
    compare_data = compare_data.to_numpy()
    distance = np.sqrt(np.sum((analysis_data - compare_data) ** 2))

    return 1 / (1 + distance)


def cos_sim(analysis_data, compare_data):
    analysis_data = analysis_data.to_numpy()
    compare_data = compare_data.to_numpy()
    similarity = np.dot(analysis_data, compare_data) / (norm(analysis_data) * norm(compare_data))

    return similarity


def manhattan_dis(anlaysis_data, compare_data):
    #     distance = sum(abs(a_data - c_data) for a_data, c_data in zip(analysis_data, compare_data))
    analysis_data = anlaysis_data.to_numpy()
    compare_data = compare_data.to_numpy()
    distance = np.abs(anlaysis_data - compare_data).sum()

    return 1 / (1 + distance)


def mean_squared_difference_sim(analysis_data, compare_data):
    #     msd = sum(pow(a_data - c_data, 2) for a_data, c_data in zip(analysis_data, compare_data))
    analysis_data = analysis_data.to_numpy()
    compare_data = compare_data.to_numpy()
    msd = np.sum((analysis_data - compare_data) ** 2)

    return 1 / (1 + (msd / len(analysis_data)))


def calculate_similarity(stock_data, analysis_data, dates, measure, days=90):  # calculate similarity
    dict_func = {
        'euc': euclidean_dis,
        'cos': cos_sim,
        'man': manhattan_dis,
        'msd': mean_squared_difference_sim
    }

    similarity_list = []
    analysis_code = analysis_data.name
    for compare_code in stock_data:
        if compare_code != analysis_code:
            try:
                for idx in range(len(stock_data) - days + 1):
                    compare_data = stock_data[compare_code][idx:idx + days]
                    similarity = dict_func[measure](analysis_data, compare_data)
                    similarity_list.append(
                        {
                            'code': compare_code,
                            'fromdate': dates[idx],
                            'todate': dates[idx + days - 1],
                            'similarity': similarity
                        }
                    )

            except KeyError:
                print("The method to measure similarity does not exist.")
                break

    return similarity_list


def check_overlap(first_data, second_data):
    first_fromdate = datetime.strptime(first_data['fromdate'], '%Y-%m-%d')
    first_todate = datetime.strptime(first_data['todate'], '%Y-%m-%d')

    second_fromdate = datetime.strptime(second_data['fromdate'], '%Y-%m-%d')
    second_todate = datetime.strptime(second_data['todate'], '%Y-%m-%d')

    if (first_fromdate <= second_fromdate <= first_todate) or (first_fromdate <= second_todate <= first_todate):
        return True

    return False


def find_top_n(similarity_list_sort, top_n=10):
    top_n_list = []

    for stock_info in similarity_list_sort:
        if not top_n_list:
            top_n_list.append(stock_info)

        elif len(top_n_list) == top_n:
            break

        else:
            overlap_flag = False
            for top_n_data in top_n_list:
                if top_n_data['code'] == stock_info['code']:
                    overlap_flag = check_overlap(top_n_data, stock_info)
                    if overlap_flag:
                        break

            if not overlap_flag:
                top_n_list.append(stock_info)

    return top_n_list


def print_result(top_n):
    print("순위, \t종목코드, \t시작일, \t종료일, \t유사도")

    for idx, data in enumerate(top_n):
        code = data['code']
        fromdate = data['fromdate']
        todate = data['todate']
        similarity = data['similarity']

        print("{0} \t{1} \t{2} \t{3} \t{4:.2f}".format(idx + 1, code, fromdate, todate, similarity))


def print_plot(analysis_data, analysis_code, top_n):
    analysis_data = analysis_data - analysis_data[-1] + 1
    plt.plot(np.array(analysis_data), label=analysis_code, linewidth=3)
    plt.title(analysis_code)

    for data in top_n:
        code = data['code']
        stocks = np.array(stock_data[code][data['fromdate']:data['todate']])
        stocks = stocks - stocks[-1] + 1
        plt.plot(stocks, label=code)

        plt.xlim([0, len(stocks) + 1])
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.show()


if __name__ == "__main__":
    stock_data, dates = load_data(filename="sample_stock_prices.csv")
    analysis_data, analysis_code = get_code_data(stock_data)
    similarity_list = calculate_similarity(stock_data, analysis_data, dates, measure="euc")
    similarity_list_sort = sorted(similarity_list, key=(lambda x: -x['similarity']))
    top_n = find_top_n(similarity_list_sort)

    print_result(top_n)
    print_plot(analysis_data, analysis_code, top_n)
