import pandas as pd
import numpy as np
from numpy.linalg import norm
from matplotlib import pyplot as plt

"""
    Load data & Preprocessing
"""
def load_data(filename, idx="date"):
    stock_data = pd.read_csv(filename, encoding="UTF-8", index_col=idx)
    stock_data = stock_data.astype(float)
    date_list = stock_data.index.tolist()

    return stock_data, date_list


def normalization(stock_data, new_max=1, new_min=0):
    norm_data = (stock_data - stock_data.min()) * (new_max - new_min) / (stock_data.max() - stock_data.min()) + new_min

    return norm_data


def get_code_data(norm_stock_data, days=90):  # Input & Get_code_data
    while True:
        try:
            analysis_code = input("Input analaysis code: ")
            analysis_data = norm_stock_data[analysis_code]
            analysis_data = analysis_data[-days:]
            break
        except KeyError:
            print("This code does not exist.")

    return analysis_data, analysis_code


def euclidean_dis(analysis_data, compare_data):
    analysis = analysis_data.to_numpy()
    compare = compare_data.to_numpy()
    distance = np.sqrt(np.sum((analysis - compare) ** 2))

    return 1 / (1 + distance)


def cos_sim(analysis_data, compare_data):
    analysis = analysis_data.to_numpy()
    compare = compare_data.to_numpy()
    similarity = np.dot(analysis, compare) / (norm(analysis) * norm(compare))

    return similarity


def manhattan_dis(analysis_data, compare_data):
    analysis = analysis_data.to_numpy()
    compare = compare_data.to_numpy()
    distance = np.abs(analysis - compare).sum()

    return 1 / (1 + distance)


def mean_squared_difference_sim(analysis_data, compare_data):
    analysis = analysis_data.to_numpy()
    compare = compare_data.to_numpy()
    msd = np.sum((analysis - compare) ** 2)

    return 1 / (1 + (msd / len(analysis)))


def supremum_dis(analysis_data, compare_data):
    analysis = analysis_data.to_numpy()
    compare = compare_data.to_numpy()
    distance = np.abs(analysis - compare).max()

    return 1 / (1 + distance)


def pearson_cor(analysis_data, compare_data):
    analysis = analysis_data.to_numpy()
    compare = compare_data.to_numpy()
    analysis = analysis - np.sum(analysis) / len(analysis)
    compare = compare - np.sum(compare) / len(compare)
    corr = np.dot(analysis, compare) / (norm(analysis) * norm(compare))

    return corr


def dynamic_time_warping(analysis_data, compare_data):
    """
    참고 사이트
    https://hamait.tistory.com/862 (코드)
    https://m.blog.naver.com/PostView.nhn?blogId=happyrachy&logNo=221694956664&proxyReferer=https:%2F%2Fwww.google.com%2F
    """
    analysis = analysis_data.to_numpy()
    compare = compare_data.to_numpy()

    dtw_matrix = np.zeros((len(analysis), len(compare)))

    fun = lambda x, y: abs(x - y)

    dtw_matrix[0, 0] = fun(analysis[0], compare[0])

    for row in range(1, len(analysis)):
        dtw_matrix[row, 0] = dtw_matrix[row - 1, 0] + fun(analysis[row], compare[0])

    for col in range(1, len(compare)):
        dtw_matrix[0, col] = dtw_matrix[0, col - 1] + fun(analysis[0], compare[col])

    for row in range(1, len(analysis)):
        for col in range(1, len(compare)):
            candidates = dtw_matrix[row - 1][col], dtw_matrix[row][col - 1], dtw_matrix[row - 1][col - 1]
            dtw_matrix[row, col] = min(candidates) + fun(analysis[row], compare[col])

    return 1 / (1 + dtw_matrix[-1][-1])


def calculate_similarity(norm_stock_data, analysis_data, measure, days=90):
    dict_func = {
        'euc': euclidean_dis,
        'cos': cos_sim,
        'man': manhattan_dis,
        'msd': mean_squared_difference_sim,
        'sup': supremum_dis,
        'prs': pearson_cor,
        'dtw': dynamic_time_warping
    }

    similarity_list = []
    analysis_code = analysis_data.name
    for compare_code in norm_stock_data:
        if compare_code != analysis_code:
            try:
                for idx in range(len(norm_stock_data) - days + 1):
                    compare_data = norm_stock_data[compare_code][idx:idx + days]
                    similarity = dict_func[measure](analysis_data, compare_data)
                    similarity_list.append(
                        {
                            'code': compare_code,
                            'fromdate': idx,
                            'todate': idx + days - 1,
                            'similarity': similarity
                        }
                    )

            except KeyError:
                print("The method to measure similarity does not exist.")
                break

    return similarity_list


def check_overlap(first_data, second_data):
    if (first_data['fromdate'] <= second_data['fromdate'] <= first_data['todate']) or (
            first_data['fromdate'] <= second_data['todate'] <= first_data['todate']):
        return True

    return False


def find_top_n(sort_sim_list, top_n=10):
    top_n_list = []

    for stock_info in sort_sim_list:
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


def print_result(top_n, date_list):
    print("순위, \t종목코드, \t시작일, \t종료일, \t유사도")

    for idx, data in enumerate(top_n):
        code = data['code']
        fromdate = date_list[data['fromdate']]
        todate = date_list[data['todate']]
        similarity = data['similarity']

        print("{0} \t{1} \t{2} \t{3} \t{4:.2f}".format(idx + 1, code, fromdate, todate, similarity))


def print_plot(stock_data, analysis_code, top_n):
    analysis = stock_data[analysis_code][-90:].to_numpy()
    analysis = normalization(analysis, 100, 1)
    analysis = analysis - analysis[-1] + 100
    plt.plot(analysis, label=analysis_code, linewidth=4)
    plt.title(analysis_code)

    for data in top_n:
        code = data['code']
        stocks = stock_data[code][data['fromdate']:data['todate'] + 1].to_numpy()
        stocks = normalization(stocks, 100, 1)
        stocks = stocks - stocks[-1] + 100
        plt.plot(stocks, label=code)

    plt.xlim([0, len(analysis)])
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.show()


if __name__ == "__main__":
    stock_data, date_list = load_data(filename="sample_stock_prices.csv")
    norm_stock_data = normalization(stock_data)
    analysis_data, analysis_code = get_code_data(norm_stock_data)
    similarity_list = calculate_similarity(norm_stock_data, analysis_data, measure="euc")
    sort_sim_list = sorted(similarity_list, key=(lambda x: -x['similarity']))
    top_n = find_top_n(sort_sim_list)

    print_result(top_n, date_list)
    print_plot(stock_data, analysis_code, top_n)