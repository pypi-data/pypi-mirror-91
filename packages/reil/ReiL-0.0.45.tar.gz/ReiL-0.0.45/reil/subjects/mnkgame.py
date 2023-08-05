# -*- coding: utf-8 -*-
'''
MNKGame class
==============

This class emulates mnk game.
'''


from typing import Any, Optional, Tuple, Union, cast
from reil.utils.mnkboard import MNKBoard
from reil.subjects.subject import Subject
from reil.datatypes import ReilData
import random


class MNKGame(MNKBoard, Subject):
    '''
    Build an m-by-n board (using `MNKBoard` class) in which p players can play.
    Winner is the player who can put `k` pieces in on row, column, or diagonal.
    '''
    # _board is a row vector. (row, column) and index start from 0
    # _board_status: None: no winner yet,
    #                1..players: winner,
    #                0: stall,
    #               -1: illegal board

    def __init__(self, m: int, n: int, k: int, players: int, **kwargs: Any):
        '''
        Arguments
        ---------
        m:
            The number of rows.

        n:
            The number of columns.

        k:
            The winning criterion, i.e. the number of cells in one row,
            column, or diagonal that a player needs to capture to win the game.

        players:
            The number of players.
        '''
        self._board_status = None
        self.set_params(**kwargs)
        MNKBoard.__init__(self, m=m, n=n, k=k, players=players,
                          can_recapture=False, **kwargs)
        Subject.__init__(self, **kwargs)

    def is_terminated(self, _id: Optional[int] = None) -> bool:
        return self._board_status is not None

    def possible_actions(self, _id: int = None) -> Tuple[ReilData, ...]:
        upper = len(self._board)-1

        return tuple(ReilData.single_numerical(
            name='square', value=v, lower=0, upper=upper)
            for v in self.get_action_set())

    def take_effect(self, action: ReilData, _id: int) -> None:
        '''
        Set a piece for the given player on the board.

        Arguments
        ---------
        action:
            The location in which the piece is placed.

        _id:
            ID of the player who sets the piece.
        '''
        Subject.take_effect(self, action, _id)
        self.set_piece(_id, index=cast(int, action.value['square']))

    def default_reward(self, _id: Optional[int] = None) -> ReilData:
        if self._board_status is None:
            r = 0
        elif self._board_status == _id:
            r = 1
        elif self._board_status > 0:
            r = -1
        else:
            r = 0

        return ReilData.single_base(name='reward', value=r)

    def reset(self):
        '''Clear the board and update board_status.'''
        Subject.reset(self)
        MNKBoard.reset(self)
        self._board_status = None

    def set_piece(self, player: int, index: Optional[int] = None,
                  row: Optional[int] = None, column: Optional[int] = None
                  ) -> None:
        '''
        Set a piece for a player.

        Arguments
        ---------
        player:
            ID of the player whose piece will be set on the board.

        row:
            The row on which the piece should be placed.

        column:
            The column on which the piece should be placed.

        index:
            Where to put the piece. Index starts from 0 and assumes the board
            to be a list.

        Raises
        ------
        ValueError:
            Wrong player ID.

        ValueError:
            index is out of range.

        Notes
        -----
        Either `index` or `row` and `column` should be used. If both are used,
        `row` and `column` is used.
        '''
        super().set_piece(
            player=player, index=index, row=row, column=column)  # type: ignore
        if self._board_status is None:
            self._board_status = self._update_board_status(
                player=player, index=index, row=row, column=column)
        elif self._board_status > 0:
            self._board_status = -1

    def _update_board_status(self, player: int,  # noqa: C901
                             index: Optional[int] = None,
                             row: Optional[int] = None,
                             column: Optional[int] = None
                             ) -> Union[int, None]:
        # player wins: player | doesn't win: None | draw: 0
        '''
        Get a player and the location of the latest change and try to find
        a sequence of length k of the specified player.

        Arguments
        ---------
        player:
            ID of the player whose piece will be set on the board.

        row:
            The row on which the piece should be placed.

        column:
            The column on which the piece should be placed.

        index:
            Where to put the piece. Index starts from 0 and assumes the board
            to be a list.

        Return
        ------
        :
            0: sequence not found and the board is full (stall)
            player: sequence found (win)
            None: sequence not found and the board is not full (ongoing)

        Notes
        -----
        Either `index` or `row` and `column` should be used. If both are used,
        `row` and `column` is used.
        '''
        if index is None:
            if row is None or column is None:
                raise TypeError('No (row, column) or index found')
            else:
                r = row
                c = column
        else:
            r = index // self._n
            c = index % self._n

        ul_r = max(r - self._k + 1, 0)
        ul_c = max(c - self._k + 1, 0)
        lr_r = min(r + self._k, self._m - 1)
        lr_c = min(c + self._k, self._n - 1)
        m = self.list_to_matrix(self._board, self._m, self._n)

        # Vertical sequence
        pointer = ul_r
        counter: int = 0
        while pointer <= lr_r:
            counter = (counter + 1) * (m[pointer][c] == player)
            if counter == self._k:
                return player
            pointer += 1

        # Horizontal sequence
        pointer = ul_c
        counter = 0
        while pointer <= lr_c:
            counter = (counter + 1) * (m[r][pointer] == player)
            if counter == self._k:
                return player
            pointer += 1

        # Diagonal \
        min_d = min(r - ul_r, c - ul_c)
        pointer_r = r - min_d
        pointer_c = c - min_d
        counter = 0
        while pointer_r <= lr_r and pointer_c <= lr_c:
            counter = (counter + 1) * (m[pointer_r][pointer_c] == player)
            if counter == self._k:
                return player
            pointer_r += 1
            pointer_c += 1

        # Diagonal /
        min_d = min(r - ul_r, lr_c - c)
        pointer_r = r - min_d
        pointer_c = c + min_d
        counter = 0
        while pointer_r <= lr_r and pointer_c >= ul_c:
            counter = (counter + 1) * (m[pointer_r][pointer_c] == player)
            if counter == self._k:
                return player
            pointer_r += 1
            pointer_c -= 1

        if min(self._board) > 0:
            return 0

        return None

    def __repr__(self):
        return self.__class__.__qualname__


if __name__ == '__main__':
    board = MNKGame(m=3, n=3, k=3, players=2)
    player = {}
    p = 0
    player['P1'] = board.register('P1')
    player['P2'] = board.register('P2')
    while not board.is_terminated():
        current_player = ['P1', 'P2'][p]
        print(p, current_player)
        actions = board.possible_actions(player[current_player])
        board.take_effect(random.choice(actions), player[current_player])
        print(f'{board}\n',
              board.reward('default', player['P1'])[0].value,
              board.reward('default', player['P2'])[0].value)
        p = (p + 1) % 2
