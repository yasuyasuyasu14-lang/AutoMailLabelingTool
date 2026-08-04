def decide_label(score):

    if score >= 40:
        return "DX_HIGH_PRIORITY"

    elif score >=30:
        return "DX_REPLY_REQUIRED"

    elif score >=20:
        return "DX_CHECK"

    else:
        return "DX_LOW"