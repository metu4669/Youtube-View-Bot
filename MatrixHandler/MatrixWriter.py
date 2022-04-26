def matrix_2_txt(path, matrix, row, col):
    string_to_txt = ""
    for i in range(row):
        if i != 0:
            string_to_txt = string_to_txt+"\n"
        for j in range(col):
            if j is not col-1:
                bt = " "
            else:
                bt = ""
            string_to_txt = string_to_txt+str(matrix[i][j])+bt

    with open(path, "w") as the_file:
        the_file.write(string_to_txt)


def videos_duration_write(path, videos, duration):
    string_to_txt = ""
    for i in range(len(videos)):
        if i != 0 and i != (len(videos)):
            string_to_txt = string_to_txt + "\n"
        string_to_txt = string_to_txt+videos[i]+" "+duration[i]

    with open(path, "w") as the_file:
        the_file.write(string_to_txt)


def proxy_write(path, proxy):
    string_to_txt = ""
    for i in range(len(proxy)):
        if i != 0 and i != (len(proxy)):
            string_to_txt = string_to_txt + "\n"
        string_to_txt = string_to_txt+proxy[i]

    with open(path, "w") as the_file:
        the_file.write(string_to_txt)
