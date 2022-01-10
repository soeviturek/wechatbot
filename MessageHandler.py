from wxpy import *

import BooruTask


class MessageHandler():
    def __init__(self,bot):
        print()

    def process_message(self):
        if 'image':
            return BooruTask.get_image()