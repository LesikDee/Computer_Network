import src.experiment as expr

lose_probability_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
tries = 5
gbn_time = []
for prob in lose_probability_list:
    average_time = 0
    for try_expr in range(tries):
        # exp = expr.Experiment('gbn', 4, prob)
        # expr_time = exp.calc_time('pack_lose')
        # average_time += expr_time
        pass

    average_time /= tries
    gbn_time.append(average_time)

