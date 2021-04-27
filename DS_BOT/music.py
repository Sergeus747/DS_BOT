import os


class TrackQueue():                                     # Класс очереди треков
    queue = []
    curent_track = None

    def not_empty(self):
        if self.queue:
            return True
        else:
            return False


    def add(self, track):
        self.queue.append(track)
        return "Трек добавлен в очередь"


    def take(self):
        track = self.queue[0]
        self.queue.remove(self.queue[0])
        return track


    def clean(self):
        while len(self.queue):
            track_name = self.queue[0]["File_name"]
            os.system(f"rm {track_name}")
            self.queue.remove(self.queue[0])


    def __del__(self):                                  # деструктор класса
        try:
            track_name = self.curent_track["File_name"]
            os.system(f"rm {track_name}")
        
            while len(self.queue):
                track_name = self.queue[0]["File_name"]
                os.system(f"rm {track_name}")
                self.queue.remove(self.queue[0])
        except TypeError:
            return "TypeError: 'NoneType' object is not subscriptable"