from python_training import kashit


def test_access_to_result_list(mocker):
    mocked_heavy_function = mocker.patch.object(kashit, 'heavy_func', autospec=True)
    decorated_mock = kashit.save_results(mocked_heavy_function)
    decorated_mock(1, 2, 3, bla=4, bla2=5)
    decorated_mock(1, 2, 3, bla=4, bla2=5)
    mocked_heavy_function.assert_called_once()
