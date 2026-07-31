def decide_label(score):

    if score >= 80:
        return "DX_HIGH_PRIORITY"

    elif score >=50:
        return "DX_REPLY_REQUIRED"

    elif score >=20:
        return "DX_CHECK"

    else:
        return "DX_LOW"