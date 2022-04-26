import MatrixHandler.MatrixWriter
import MatrixHandler.MatrixReader


class MainHandlerClass:
    matrix_file = ""
    video_file = ""
    proxy_file = ""
    matrix = []
    matrix_available_1d = []
    num_proxy = 0
    num_url = 0

    def empty_matrix_creator(self):
        for i in range(self.num_proxy):
            temp_ = []
            for j in range(self.num_url):
                temp_.append(0)
            self.matrix.append(temp_)
        self.write_matrix(self.matrix)

    def __init__(self, matrix_path, videos_path, proxy_path, num_proxy_, num_url_):
        self.matrix_file = matrix_path
        self.video_file = videos_path
        self.proxy_file = proxy_path
        self.num_proxy = num_proxy_
        self.num_url = num_url_

    def write_matrix(self, proxy_url_matrix):
        MatrixHandler.MatrixWriter.matrix_2_txt(self.matrix_file, proxy_url_matrix, len(proxy_url_matrix), len(proxy_url_matrix[0]))

    def write_videos_matrix(self, videos, durations):
        MatrixHandler.MatrixWriter.videos_duration_write(self.video_file, videos, durations)

    def write_proxy_matrix(self, proxies_):
        MatrixHandler.MatrixWriter.proxy_write(self.proxy_file, proxies_)

    def read_matrix(self):
        return MatrixHandler.MatrixReader.txt_2_matrix(self.matrix_file)

    def get_matrix(self):
        return self.read_matrix()
