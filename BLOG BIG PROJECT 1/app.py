print('hello world!')

# Connection TEST  ZONE
from puppycompanyblog.blog_posts import blog_posts_test
from puppycompanyblog.core.views import npf
print(blog_posts_test)
print(npf)

from puppycompanyblog import app

if __name__ == '__main__':
    app.run(debug=True)


