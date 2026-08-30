def test_user_response_does_not_expose_password(
    customer,
):
    from apps.users.serializers import UserSerializer

    data = UserSerializer(customer).data

    assert "password" not in data


def test_user_response_does_not_expose_tokens(
    customer,
):
    from apps.users.serializers import UserSerializer

    data = str(UserSerializer(customer).data)

    assert "access" not in data
    assert "refresh" not in data
