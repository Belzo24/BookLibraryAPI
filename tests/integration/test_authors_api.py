from faker import Faker

fake = Faker()

def test_add_author(client):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request is sent to /authors
    THEN check that the response is valid and the author is in the database
    """
    author_name = fake.name()
    if not author_name[0].isupper():
        author_name = author_name.capitalize()
        
    data = {
        'author_name': author_name,
        'birth': fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%d/%m/%Y'),
        'author_id': str(fake.uuid4())
    }
    response = client.post('/authors', json=data)
    assert response.status_code == 201
    assert response.json['author_name'] == data['author_name']

def test_add_author_invalid_payload(client):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request with invalid data is sent to /authors
    THEN check for a 422 Unprocessable Entity response
    """
    data = {
        'author_name': 'lowercase name', # Invalid name
        'birth': '1990-01-01', # Invalid date format
        'author_id': str(fake.uuid4())
    }
    response = client.post('/authors', json=data)
    assert response.status_code == 422 