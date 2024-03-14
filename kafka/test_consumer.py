from unittest.mock import MagicMock, patch

from consumer import get_db_connection, upload_to_database, send_valid_assistance, send_valid_emergency, handle_message


@patch("consumer.get_db_connection")
def test_upload_database(mock_connection):
    """Tests the upload database function"""

    mock_connection = MagicMock()
    mock_commit = mock_connection.commit

    location = {"at": "01/12/2024", "site": "2", "val": "4"}

    upload_to_database(mock_connection, location)

    assert mock_commit.call_count == 1


@patch("consumer.get_db_connection")
def test_upload_assistance(mock_connection):
    """Tests the upload assistance function"""

    mock_connection = MagicMock()
    mock_commit = mock_connection.commit

    location = {"at": "01/12/2024", "site": "2", "val": "-1", "type": "0"}

    send_valid_assistance(mock_connection, location)

    assert mock_commit.call_count == 1


@patch("consumer.get_db_connection")
def test_upload_emergency(mock_connection):
    """Tests the upload emergency function"""

    mock_connection = MagicMock()
    mock_commit = mock_connection.commit

    location = {"at": "01/12/2024", "site": "2", "val": "-1", "type": "1"}

    send_valid_emergency(mock_connection, location)

    assert mock_commit.call_count == 1


def test_check_incorrect_site():
    """Test that checks if a message has no 'site' key it returns an error message"""

    message = {"at": "2024-03-12T13:12:18.645631+00:00", 'val': 4}

    result = handle_message(message)

    assert result == "Error: Invalid Missing 'site' Key"


def test_check_incorrect_at():
    """Test that checks if a message has no 'at' key it returns an error message"""

    message = {"site": 3, 'val': 4}

    result = handle_message(message)

    assert result == "Error: Missing 'at' Key"


def test_check_incorrect_at():
    """Test that checks if a message has no 'val' key it returns an error message"""

    message = {"at": "2024-03-12T13:12:18.645631+00:00", "site": "3"}

    result = handle_message(message)

    assert result == "Error: Invalid Missing 'val' Key"
