video_file = "C:/Users/Omer/Desktop/Proxy/Videos/videos.txt"


class VideoGetMain:
    lines = []
    size = 0
    times = []

    def read(self):
        file = open(video_file, "r")
        f1 = file.readlines()
        for x in f1:
            splitted = x.split(" ")
            self.lines.append(splitted[0])
            self.times.append(splitted[1])
        self.size = len(self.lines)
        file.close()
        return self.lines, self.times

    def get_video_size(self):
        print(str(self.size)+"lk")
        return self.size

    def get_video_urls(self):
        return self.lines
