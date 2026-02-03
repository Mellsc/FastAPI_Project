from jwt import decode

from fast_zero.security import create_access_token, SECRET_KEY, ALGORITHM

def test_jwt():
    data = {'sub': 'test@email.com'} 
    token = create_access_token(data)

    result = decode(token, SECRET_KEY, algorithms = [ALGORITHM])

    assert result['sub'] == data['sub']
    assert result['exp']
