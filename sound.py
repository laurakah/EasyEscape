class Sound():

    def __init__(self):
        pass

    @staticmethod
    def play_sound(file_path):
        import subprocess

        subprocess.Popen(['aplay', "-q", file_path])
