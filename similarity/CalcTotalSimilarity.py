"""各パラメータの類似度から総合スコアを算出"""
def calc_total_similarity(similarities, feature_weight):
    if abs(sum(feature_weight.values()) - 1.0) > 1e-9:
        raise ValueError("FEATURE_WEIGHTの合計は1.0にしてください")

    total_scores = {}

    for mail_id, label_scores in similarities.items():

        total_scores[mail_id] = {}

        for label_name, parameter_scores in label_scores.items():

            total_score = sum(
                score * feature_weight[parameter]
                for parameter, score in parameter_scores.items()
            )

            total_scores[mail_id][label_name] = total_score

    return total_scores