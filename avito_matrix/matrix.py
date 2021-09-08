from typing import List
import aiohttp
import logging
from .errors import MatrixNetworkError

log = logging.getLogger('matrix')


def _traverse(matrix: List[List[int]]) -> List[int]:
    """
    unwind the matrix into 1D array by traversing it in counter-clockwise direction
    starting from the top left corner
    :param matrix: 2D array of integers
    :return: 1D array of integers
    """
    n = len(matrix)
    m = len(matrix[0]) if n > 0 else 0
    vector = [0] * n * m
    left, right, down, up = 0, m - 1, n - 1, 0
    i = 0
    while i < n * m:
        # from up to down
        for row in range(up, down+1):
            vector[i] = matrix[row][left]
            i += 1
        # from left to right
        for col in range(left + 1, right+1):
            vector[i] = matrix[down][col]
            i += 1
        if left < right:
            # from down to up
            for row in range(down - 1, up-1, -1):
                vector[i] = matrix[row][right]
                i += 1
        if up < down:
            # from right to left
            for col in range(right - 1, left, -1):
                vector[i] = matrix[up][col]
                i += 1
        up += 1
        down -= 1
        left += 1
        right -= 1
    return vector


def _parse_text_table(content: str) -> List[List[int]]:
    """
    parse ascii-formatted table into 2D array
    :param content:
    :return:
    """
    matrix = []
    rows = content.split('\n')
    for row in rows:
        if row.startswith('|'):
            cells = row.split('|')
            vector = [int(cell.strip()) for cell in cells if cell]
            matrix.append(vector)
    return matrix


async def get_matrix(url: str) -> List[int]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                content = await resp.content.read()
        except IOError as ex:
            msg = str(ex)
            log.warning(f'unable to retrieve {url}: {msg}')
            raise MatrixNetworkError(msg) from None
    if resp.status != 200:
        log.warning(f'unable to retrieve {url}: response code {resp.status}')
        raise MatrixNetworkError('resource not found')
    matrix = _parse_text_table(content.decode())
    result = _traverse(matrix)
    return result
