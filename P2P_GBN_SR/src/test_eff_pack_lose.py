import src.experiment as expr
import random
random.seed(1)

if __name__ == '__main__':
    lose_probability_list = [0.7]  # [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    window_size = 4
    session_seconds = 10
    tries = 1
    gbn_time = []
    for prob in lose_probability_list:
        for try_expr in range(tries):
            exp = expr.Experiment('gbn', window_size, prob, seconds=session_seconds)
            tr = exp.calc_efficiency()
            print(tr)

    # for i in range(20):
    #     print(random.random())