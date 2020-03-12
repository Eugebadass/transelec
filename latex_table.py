# Purpose : to automatically do a latex table in a text file of your project directory
# How to use it :
# 1-import this py file into the code with the data
# 2-Call the make_a_latex_table function with these attributes :
#     title = str - title of your table
#     label = str - label of your table to make reference to later
#     large = bool - add restrictive bonderies to the width of the table
#     data = dict{lists} - a dictionary that has the name of the column as the key and the list of data as a value
# 3-Check the latextable.txt file for your table


def make_a_latex_table(title="", label="", data={}, large=False):

    if title == "" or label == "" or data == {}:
        print("Need other attributes")
    file = open("latextable.txt", "w")
    struct_col = "|"
    for i in data:
        if data[i][0] is str:
            struct_col += "l|"
        else :
            struct_col += "c|"
    file.write("\\begin{table}[H]\n" +
               "\\centering\n" +
               "\\caption{" + title + "}\n" +
               "\\label{" + label + "}\n")
    if large:
        file.write("\\resizebox{\\textwidth}{!}{\n")
    file.write("\\begin{tabular}{" + struct_col + "}\n" +
               "\\hline\n")
    cnt = 0
    a = []
    for x in data:
        cnt += 1
        if len(data) != cnt:
            file.write(str(x) + "\t&\t")
        else:
            file.write(str(x) + "\t\\\\ \\hline\n")
            a = data[x]

    for y in range(0, len(a)):
        cnt = 0
        for x in data:
            cnt += 1
            if len(data) != cnt:
                file.write(str(data[x][y]) + "\t&\t")
            else:
                file.write(str(data[x][y]) + "\t\\\\ \\hline\n")
    file.write("\\end{tabular}\n")
    if large:
        file.write("}\n")
    file.write("\\end{table}\n")

    file.close()


if __name__ == "__main__" :
    a = "salut"
    b = "slt"
    c = {"a" : [1, 2, 3], "b" : ["bla", "blabla", "blablabla"], "c" : [223365, 569844, 566522], "d" : [1, 5, 6]}
    make_a_latex_table(a, b, data=c, large=True)