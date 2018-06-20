def getHtmlElement(tag='p', msg="undefined", selfclose=False, **kwargs):
    """
    Creating an HTML element
    return <tag args>msg</tag>
    """
    element = "<" + tag
    for key, val in kwargs.items():
        element += " " + key + "=" + val
    element += ">"
    if selfclose:
        return element
    element += "{M}</{T}>".format(M=msg, T=tag)
    return element


def getBlock(text, color, width="40"):
    return "<div style=\"background-color:{C};color:black;display:inline-block;width:{W}px;text-align:center\">{T}</div>".format(
        C=color, T=text, W=width)


def getLeetCodeStatus(questions):
    from . import leetcode as lc
    body = "<div style=\"background-color:cyan;display:block\">"
    for i, q in enumerate(questions):
        q_id = q['id']
        q_status = q['status']
        body += getBlock("[%03d]" % q_id, lc.getColorViaStatus(q_status).split('_')[-1], width="42") + "\n"
        if (i+1) % 25 == 0:
            body += "<br>\n"
    body += "<br>" * 3 + "\n"
    for stat in ["solved", "unsolved", "stuck", "marked"]:
        body += getBlock("[###]", lc.getColorViaStatus(stat).split('_')[-1], width="55")
        body += " " + getHtmlElement(tag='b', msg=stat)
        body += getBlock(" " * 20, "cyan", width="150")
    body += "<br>" * 3 + "\n"
    return body