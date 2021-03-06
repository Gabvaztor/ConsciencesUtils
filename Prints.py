
def show_percent_by_total(total, count_number):
    same_line = False if total == count_number else True
    pt("Total Size", total, same_line=same_line)
    pt("Count number", count_number, same_line=same_line)
    progress = float(((count_number * 100) / total))
    progress = "{0:.3f}".format(progress)
    pt("Progress percent", progress + "%", same_line=same_line)


def pt(title=None, text=None, same_line=False):
    """
        Use the print function to print a title and an object converted to string
        :param title:
        :param text:
    """
    if text is None:
        text = title
        title = '-------------------------------------'
    else:
        title += ': '
    if same_line:
        print(str(title) + str(text), end="\r")
    else:
        print(str(title) + " \n " + str(text))