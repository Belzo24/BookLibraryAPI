import pytest
from pydantic import ValidationError
from validation_logging.errors import AuthorInput
from faker import Faker

fake = Faker()

def test_author_input_valid():
    """
    GIVEN valid author data
    WHEN creating an AuthorInput instance
    THEN no validation error is raised
    """
    valid_name = fake.name()
    # Ensure the first letter is capitalized for the validator
    if not valid_name[0].isupper():
        valid_name = valid_name.capitalize()

    author_data = {
        "author_name": valid_name,
        "birth": fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%d/%m/%Y'),
        "author_id": str(fake.uuid4())
    }
    AuthorInput(**author_data)


def test_author_name_invalid_no_capital():
    """
    GIVEN author data with a non-capitalized name
    WHEN creating an AuthorInput instance
    THEN a ValidationError is raised
    """
    with pytest.raises(ValidationError) as excinfo:
        AuthorInput(
            author_name="john doe",
            birth="01/01/1990",
            author_id="123"
        )
    assert "did not start with capital letter" in str(excinfo.value)


def test_author_name_invalid_is_integer():
    """
    GIVEN author data with an integer as a name
    WHEN creating an AuthorInput instance
    THEN a ValidationError is raised
    """
    with pytest.raises(ValidationError) as excinfo:
        AuthorInput(
            author_name="12345",
            birth="01/01/1990",
            author_id="123"
        )
    assert "input just numbers" in str(excinfo.value)

def test_birth_date_invalid_format():
    """
    GIVEN author data with an invalid birth date format
    WHEN creating an AuthorInput instance
    THEN a ValidationError is raised
    """
    with pytest.raises(ValidationError) as excinfo:
        AuthorInput(
            author_name="Valid Name",
            birth="2000-01-01", # Wrong format
            author_id="123"
        )
    assert "invalid birth input" in str(excinfo.value)

def test_birth_date_various_valid_formats():
    """
    GIVEN author data with various valid birth date formats
    WHEN creating an AuthorInput instance
    THEN no validation error is raised
    """
    formats = ["%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y"]
    for fmt in formats:
        AuthorInput(
            author_name="Valid Name",
            birth=fake.date_of_birth(minimum_age=18, maximum_age=90).strftime(fmt),
            author_id=str(fake.uuid4())
        ) 