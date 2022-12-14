from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///SQL_test_db'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""
        db.drop_all()
        db.create_all()

        user = User(first_name="Mark", last_name="Jones")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

        post = Post(title="Best Post", content="Blablabla", user_id=self.user_id)
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id

    def test_list_users(self):
        """Show all users"""

        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Mark', html)

    def test_show_user_details(self):
        """Show user details based on id"""

        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Mark Jones</h1>', html)
            self.assertIn('Best Post', html)

    def test_add_user_form(self):
        """Show add_user form"""

        with app.test_client() as client:
            resp = client.get("/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Add a new user:</h2>', html)

    def test_add_user_post(self):
        """Adds a new user to DB"""

        with app.test_client() as client:
            d = {"first_name": "Jake", "last_name": "Miller", "image": ""}
            resp = client.post('/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Users</h1>", html)
            self.assertIn('Jake Miller', html)
    
    def test_edit_user_form(self):
        """Show form to updaye user info"""

        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Edit a user:</h2>', html)

    def test_update_user_post(self):
        """Updates user info"""

        with app.test_client() as client:
            d={'first_name':'Markus', 'last_name':'Jones', 'image':''}
            resp = client.post(f"/{self.user_id}/edit", data=d,follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Users</h1>", html)
            self.assertIn('Markus Jones', html)

    def test_delete_user(self):
        """DElete user with that id"""
        
        with app.test_client() as client:
            resp = client.post(f"/{self.user_id}/delete",follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Users</h1>", html)
            self.assertNotIn('Mark Jones', html)

    def test_create_post(self):
        """Test to create a new post"""

        with app.test_client() as client:
            d = {"title": "Hi", "content": "How are you?", "user_id": "9"}
            resp = client.post(f'/{self.user_id}/posts/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Mark Jones</h1>", html)
            self.assertIn('Hi', html)

    def test_edit_post(self):
        """Test post updates"""

        with app.test_client() as client:
            d={'title':'Best Post', 'content':'Updated Content', 'user_id':'1'}
            resp = client.post(f"/posts/{self.post_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Best Post</h1>", html)
            self.assertIn('Updated Content', html)

    def test_delete_post(self):
        """Test to delete post"""

        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/delete",follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Mark Jones</h1>", html)
            self.assertNotIn('Best Post', html)

class TagsViewsTestCase(TestCase):
    """Tests for views for Tags."""

    def setUp(self):
        """Add sample tag."""
        
        db.drop_all()
        db.create_all()

        user = User(first_name="Mark", last_name="Jones")
        db.session.add(user)
        db.session.commit()

        tag = Tag(name="sky")
        post = Post(title='Good Post 1', content='some text', user_id = 1)
        db.session.add(post)
        db.session.add(tag)
        db.session.commit()

        new_connection = PostTag(post_id=1, tag_id=1)
        db.session.add(new_connection)
        db.session.commit()

        
        self.tag_id = tag.id
        self.post_id = post.id    
    
   
    def test_show_tags(self):
        """Show tags"""

        with app.test_client() as client:
            resp = client.get("/tags")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Tags', html)
            self.assertIn('sky', html)
    
    def test_show_tag_details(self):
        """Show tag details"""

        with app.test_client() as client:
            resp = client.get(f'/tags/{self.tag_id}')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>sky</h1>', html)
            self.assertIn('edit', html)
            self.assertIn('Good Post 1', html)

    def test_add_tag(self):
        """Testing add tag function"""

        with app.test_client() as client:
            d = {'name':'springboard'}
            resp = client.post(f'/tags/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Tags</h1>', html)
            self.assertIn('springboard', html)

    def test_edit_tag(self):
        """Testing edit tag function"""

        with app.test_client() as client:
            d = {'name':'Good Post 2'}
            resp = client.post(f'/tags/{self.tag_id}/edit', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Tags</h1>', html)
            self.assertIn('Good Post 2', html)
            self.assertNotIn('Good Post 1', html)

    def test_delete_tag(self):
        """Testing delete tag function"""

        with app.test_client() as client:
            resp = client.post(f'/tags/{self.tag_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Tags</h1>', html)
            self.assertNotIn('Good Post 1', html)      


