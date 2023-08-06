from WPTextSpinner.Utils import Logger
from WPTextSpinner.Utils.Database import Database
from WPTextSpinner.Utils import Utils


class PostService:
    def __init__(self):
        self.config = self.load_config()
        pass

    def load_config(self):
        data = Utils.get_config_data()

        self.post_type = data['posts']['post_type']

    def get_posts(self, post_type="post"):
        posts = []
        db = Database()
        for result in db.do_query("select id, post_title from " + db.table_prefix + "posts where post_type = %s",(post_type,)):
            id, title = result
            post = {
                'id': id,
                'title': title
            }
            posts.append(post)

        return posts

    def update_post(self, db, post_id, new_content):
        Logger.log("updating post: #"+str(post_id))
        db.do_query("update " + db.table_prefix + "posts set post_content = %s where id = %s",
                    (new_content.encode("utf-8"), post_id))