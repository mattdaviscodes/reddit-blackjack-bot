INSERT INTO command_types
        (command_type_id, name)
VALUES  (1, 'deal'),
        (2, 'hit'),
        (3, 'stay'),
        (4, 'double_down'),
        (5, 'split'),
        (6, 'help'),
        (7, 'high_scores'),
        (8, 'stats'),
        (9, 'recharge_credits');    -- Show deep-dive of player's stats

INSERT INTO action_types
        (action_type_id, name)
VALUES  (-1, 'invalid_command'),
        (1, 'begin_game'),
        (2, 'player_hit'),
        (3, 'player_stay'),
        (4, 'player_double_down'),
        (5, 'player_split'),
        (6, 'dealer_hit'),
        (7, 'dealer_stay'),
        (8, 'player_win'),
        (9, 'dealer_win'),
        (10, 'player_blackjack'),
        (11, 'dealer_blackjack'),
        (12, 'push'),
        (13, 'end_game'),
        (14, 'recharge_credits'),
        (15, 'help'),
        (16, 'stats'),
        (17, 'high_scores'),
        (18, 'new_player');
