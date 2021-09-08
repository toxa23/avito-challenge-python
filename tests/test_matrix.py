import asyncio
from avito_matrix import get_matrix, MatrixNetworkError
from avito_matrix.matrix import _parse_text_table, _traverse
import pytest


CONTENT = """+-----+-----+-----+-----+
|  10 |  20 |  30 |  40 |
+-----+-----+-----+-----+
|  50 |  60 |  70 |  80 |
+-----+-----+-----+-----+
|  90 | 100 | 110 | 120 |
+-----+-----+-----+-----+
| 130 | 140 | 150 | 160 |
+-----+-----+-----+-----+"""
MATRIX = [
    [10, 20, 30, 40],
    [50, 60, 70, 80],
    [90, 100, 110, 120],
    [130, 140, 150, 160]
]
TRAVERSAL = [
    10, 50, 90, 130,
    140, 150, 160, 120,
    80, 40, 30, 20,
    60, 100, 110, 70,
]
SOURCE_URL = 'https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt'


@pytest.mark.parametrize('content, matrix', [
    (CONTENT, MATRIX),
    ('bad text', [])
])
def test_parse_response(content, matrix):
    result = _parse_text_table(CONTENT)
    assert result == MATRIX


@pytest.mark.parametrize('matrix, traversal', [
    (
        [],
        []
    ),
    (
        [[1]],
        [1]
    ),
    (
        [[1, 2], [3, 4]],
        [1, 3, 4, 2]
    ),
    (
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [1, 4, 7, 8, 9, 6, 3, 2, 5]
    ),
    (
        MATRIX,
        TRAVERSAL
    ),
    (
        [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]],
        [1, 6, 11, 16, 21, 22, 23, 24, 25, 20, 15, 10, 5, 4, 3, 2, 7, 12, 17, 18, 19, 14, 9, 8, 13]
    )
])
def test_traverse(matrix, traversal):
    result = _traverse(matrix)
    assert result == traversal


def test_get_matrix_success():
    assert asyncio.run(get_matrix(SOURCE_URL)) == TRAVERSAL


@pytest.mark.parametrize('url', [
    'https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/not-a-matrix.txt',
    'http://bad-host'
])
def test_get_matrix_failure(url):
    with pytest.raises(MatrixNetworkError):
        asyncio.run(get_matrix(url))
