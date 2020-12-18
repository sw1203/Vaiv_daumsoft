import pandas as pd
import numpy as np
from numpy.linalg import norm
from matplotlib import pyplot as plt


"""
    Load data & Preprocessing
"""


def load_data(filename, idx="date"):
    stock_data = pd.read_csv(filename, index_col=idx)
    stock_data = stock_data.astype(float)
    date_list = stock_data.index.tolist()

    return stock_data, date_list


def normalization(stock_data, max_price, min_price):
    if max_price != min_price:
        norm_data = (stock_data - min_price) / (max_price - min_price)
        return norm_data

    else:
        return None


def normalization2(stock_data):
    norm_data = stock_data / stock_data[-1]
    return norm_data


def get_code_data(stock_data, analysis_code, days=90):  # Input & Get_code_data
    try:
        analysis_data = stock_data[analysis_code][-days:]
        norm_analysis_data = normalization(analysis_data, np.max(analysis_data), np.min(analysis_data))
    #         norm_analysis_data = normalization2(analysis_data)
    except KeyError:
        print("This code does not exist.")

    return norm_analysis_data


def euclidean_dis(analysis, compare):
    if analysis is None or compare is None:
        return None
    else:
        distance = np.sqrt(sum((a - b) ** 2 for a, b in zip(analysis, compare)))
        return 1/(1+distance)


def cos_sim(analysis, compare):
    if analysis is None or compare is None:
        return None
    else:
        similarity = np.dot(analysis, compare) / (norm(analysis)*norm(compare))
        return similarity


def manhattan_dis(analysis,compare):
    if analysis is None or compare is None:
        return None
    else:
        distance = sum(abs(a - b) for a, b in zip(analysis, compare))
        return 1/(1+distance)


def mean_squared_difference_sim(analysis, compare):
    if analysis is None or compare is None:
        return None
    else:
        msd = sum((a - b)** 2 for a, b in zip(analysis, compare))
        return 1/(1+(msd/len(analysis)))


def supremum_dis(analysis, compare):
    if analysis is None or compare is None:
        return None
    else:
        distance = max(abs(a - b) for a, b in zip(analysis, compare))
#         distance = np.abs(analysis-compare).max()
        return 1/(1+distance)


def pearson_cor(analysis, compare):
    if analysis is None or compare is None:
        return None
    else:
        analysis = analysis - np.sum(analysis)/len(analysis)
        compare = compare - np.sum(compare)/len(compare)
        corr = np.dot(analysis, compare) / (norm(analysis)*norm(compare))
        return corr


def dynamic_time_warping(analysis, compare):
    """
    참고 사이트
    https://hamait.tistory.com/862 (코드)
    https://m.blog.naver.com/PostView.nhn?blogId=happyrachy&logNo=221694956664&proxyReferer=https:%2F%2Fwww.google.com%2F
    """

    if analysis is None or compare is None:
        return None
    else:
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


def calculate_similarity(stock_data, analysis_data, measure, days=90):
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
    analysis = analysis_data.to_numpy()
    stocks = stock_data.to_numpy()

    for code_idx, compare_code in enumerate(stock_data):
        if compare_code != analysis_data.name:
            for idx in range(len(stocks) - days + 1):
                compare_data = stocks[:, code_idx][idx:idx + days]
                norm_compare_data = normalization(compare_data, np.max(compare_data), np.min(compare_data))
                #                 norm_compare_data = normalization2(compare_data)
                similarity = dict_func[measure](analysis_data, norm_compare_data)
                if similarity != None:
                    similarity_list.append(
                        {
                            'code': compare_code,
                            'fromdate': idx,
                            'todate': idx + days - 1,
                            'similarity': similarity
                        }
                    )

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

def print_plot(analysis_data, analysis_code, stock_data, top_n):

    analysis = analysis_data.to_numpy()
    analysis = analysis - analysis[-1] + 100
    plt.plot(analysis, label=analysis_code, linewidth=4)
    plt.title(analysis_code)

    for data in top_n:
        code = data['code']
        stocks = stock_data[code][data['fromdate']:data['todate'] + 1].to_numpy()
        stocks = normalization(stocks, np.max(stocks), np.min(stocks))
        #         stocks = normalization2(stocks)
        stocks = stocks - stocks[-1] + 100
        plt.plot(stocks, label=code)

    plt.xlim([0, len(analysis)])
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.show()


if __name__ == "__main__":
    stock_data, date_list = load_data(filename="sample_stock_prices.csv")
    analysis_code = "A001560"
    analysis_data = get_code_data(stock_data, analysis_code)
    similarity_list = calculate_similarity(stock_data, analysis_data, measure="euc")
    sort_sim_list = sorted(similarity_list, key=(lambda x: -x['similarity']))
    top_n = find_top_n(sort_sim_list)

    print_result(top_n, date_list)
    print_plot(analysis_data, analysis_code, stock_data, top_n)