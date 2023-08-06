#-*- coding: UTF-8 -*-
from threading import Thread

from WPTextSpinner.Engine.PostService import PostService
from WPTextSpinner.Utils.Database import Database
from WPTextSpinner.Engine.TextSpinner import TextSpinner
from WPTextSpinner.Utils import Utils


class WPTextSpinner:
    def __init__(self):
        self.db = Database()
        self.config = Utils.get_config_data()
        self.post_service = PostService()
        self.num_threads = self.config['threads']
        self.variables = self.config['variables']

    def spin_posts(self, posts, text, dry=False):
        post_batches = list(Utils.split_list(posts, self.num_threads))

        threads = []

        for post_batch in post_batches:
            thread = Thread(target=self.spin_batch, args=(text, post_batch, dry))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

    def spin_batch(self, text, posts, dry=False):
        db = Database()
        post_count = len(posts)
        for i in range(0, post_count):
            post = posts[i]
            print("Spinning post with id #" + str(post['id']) + " (" + str(i + 1) + "/" + str(
                post_count) + ")")
            content = self.spin_post(post, text)
            if not dry:
                self.post_service.update_post(db, post['id'], content)
        db.close()

    def spin_post(self, post, text):
        text_spinner = TextSpinner(self.variables, post['title'])
        return text_spinner.spin_text_title(text)
