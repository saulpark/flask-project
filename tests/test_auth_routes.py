class TestLoginRoute:
    """Tests for login route and open redirect protection."""

    def test_login_page_renders(self, client):
        resp = client.get('/auth/login')
        assert resp.status_code == 200

    def test_login_success_redirects_home(self, client, user):
        resp = client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password123',
        }, follow_redirects=False)
        assert resp.status_code == 302
        assert '/' in resp.headers['Location']

    def test_login_invalid_credentials(self, client, user):
        resp = client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword',
        }, follow_redirects=True)
        assert b'Invalid email or password' in resp.data

    def test_login_rejects_external_next_url(self, client, user):
        resp = client.post('/auth/login?next=https://evil.com', data={
            'email': 'test@example.com',
            'password': 'password123',
        }, follow_redirects=False)
        assert resp.status_code == 302
        assert 'evil.com' not in resp.headers['Location']

    def test_login_allows_relative_next_url(self, client, user):
        resp = client.post('/auth/login?next=/notes/', data={
            'email': 'test@example.com',
            'password': 'password123',
        }, follow_redirects=False)
        assert resp.status_code == 302
        assert '/notes/' in resp.headers['Location']

    def test_login_rejects_protocol_relative_url(self, client, user):
        resp = client.post('/auth/login?next=//evil.com/path', data={
            'email': 'test@example.com',
            'password': 'password123',
        }, follow_redirects=False)
        assert resp.status_code == 302
        assert 'evil.com' not in resp.headers['Location']

    def test_authenticated_user_redirected_from_login(self, auth_client):
        resp = auth_client.get('/auth/login', follow_redirects=False)
        assert resp.status_code == 302


class TestRegisterRoute:
    """Tests for register route."""

    def test_register_page_renders(self, client):
        resp = client.get('/auth/register')
        assert resp.status_code == 200

    def test_register_success(self, client, app):
        resp = client.post('/auth/register', data={
            'email': 'new@example.com',
            'password': 'newpass123',
            'confirm': 'newpass123',
        }, follow_redirects=True)
        assert resp.status_code == 200

    def test_authenticated_user_redirected_from_register(self, auth_client):
        resp = auth_client.get('/auth/register', follow_redirects=False)
        assert resp.status_code == 302


class TestLogoutRoute:
    """Tests for logout route."""

    def test_logout_requires_post(self, auth_client):
        resp = auth_client.get('/auth/logout')
        assert resp.status_code == 405

    def test_logout_redirects_to_login(self, auth_client):
        resp = auth_client.post('/auth/logout', follow_redirects=False)
        assert resp.status_code == 302
        assert '/auth/login' in resp.headers['Location']


class TestLoginRequired:
    """Tests that protected routes redirect unauthenticated users."""

    def test_notes_list_requires_login(self, client):
        resp = client.get('/notes/')
        assert resp.status_code == 302
        assert '/auth/login' in resp.headers['Location']

    def test_notes_new_requires_login(self, client):
        resp = client.get('/notes/new')
        assert resp.status_code == 302

    def test_notes_view_requires_login(self, client):
        resp = client.get('/notes/1')
        assert resp.status_code == 302

    def test_users_view_requires_login(self, client):
        resp = client.get('/users/1')
        assert resp.status_code == 302
