# Feature encoding scheme:
# - Wind: feature[:1]
# - Round Position: feature[1:2]
# - Hand: feature[2:36] (34 types)
# - Self Pongs: feature[36:70] (34 types)
# - Self Kongs: feature[70:104] (34 types)
# - Self Chows: feature[104:125] (21 types)
# - Op Pongs: feature[125:159] (34 types)
# - Op Kongs: feature[159:193] (34 types)
# - Op Chows: feature[193:214] (21 types)
# - Next Pongs: feature[214:248] (34 types)
# - Next Kongs: feature[248:282] (34 types)
# - Next Chows: feature[282:303] (21 types)
# - Prev Pongs: feature[303:337] (34 types)
# - Prev Kongs: feature[337:371] (34 types)
# - Prev Chows: feature[371:392] (21 types)
# - Action tile: feature[392:426] (34 types)
# - Discard Pool: feature[426:460] (34 types)

def encoder(state: dict) -> list:
    features = [0] * 460
    
    # Format checking
    if 'current_wind' not in state:
        raise ValueError("Record malformed: missing 'current_wind'")
    if 'round_position' not in state:
        raise ValueError("Record malformed: missing 'round_position'")
    if 'hand' not in state:
        raise ValueError("Record malformed: missing 'hand'")
    if 'called_tuples' not in state:
        raise ValueError("Record malformed: missing 'called_tuples'")
    if 'action' not in state:
        raise ValueError("Record malformed: missing 'action'")
    if 'action_tile' not in state:
        raise ValueError("Record malformed: missing 'action_tile'")
    if 'discard_pool' not in state:
        raise ValueError("Record malformed: missing 'discard_pool'")
    if 'opposite_player_called_tuples' not in state:
        raise ValueError("Record malformed: missing 'opposite_player_called_tuples''")
    if 'next_player_called_tuples' not in state:
        raise ValueError("Record malformed: missing 'next_player_called_tuples'")
    if 'previous_player_called_tuples' not in state:
        raise ValueError("Record malformed: missing 'previous_player_called_tuples'")

    # Wind encoding
    features[0] = state['current_wind'] / 3  # Normalize to [0,1]
    # Round Position encoding
    features[1] = state['round_position'] / 3  # Normalize to [0,1]
    # Hand encoding
    for tile in state['hand']:
        # Hand encoding
        tile_id = tile - 1
        # Apply normalization
        features[2 + tile_id] += 1 / 4
    
    chow_id_mapping = {
        # 'm' chows
        1: 0,
        2: 1,
        3: 2,
        4: 3,
        5: 4,
        6: 5,
        7: 6,
        # 'p' chows
        10: 7,
        11: 8,
        12: 9,
        13: 10,
        14: 11,
        15: 12,
        16: 13,
        # 's' chows
        19: 14,
        20: 15,
        21: 16,
        22: 17,
        23: 18,
        24: 19,
        25: 20,
    }

    # Self call tuple encoding (assume all tuples are valid)
    for t in state['called_tuples']:
        # Check tuple type
        if len(t) == 4:
            idx = t[0] - 1
            features[70 + idx] += 1
        if len(t) == 3:
            # Pong case
            if t[0] == t[1] == t[2]:
                idx = t[0] - 1
                features[36 + idx] += 1
            else:
                # Chow case
                t.sort()
                idx = chow_id_mapping.get(t[0], None)
                if idx is not None:
                    # Applly normalization
                    features[104 + idx] += 1 / 4

    # Opposite side player call tuple encoding (assume all tuples are valid)
    for t in state['opposite_player_called_tuples']:
        # Check tuple type
        if len(t) == 4:
            idx = t[0] - 1
            features[159 + idx] += 1
        if len(t) == 3:
            # Pong case
            if t[0] == t[1] == t[2]:
                idx = t[0] - 1
                features[125 + idx] += 1
            else:
                # Chow case
                t.sort()
                idx = t[0] - 1
                # Apply normalization
                features[193 + idx] += 1 / 4

    # Next player call tuple encoding (assume all tuples are valid)
    for t in state['next_player_called_tuples']:
        # Check tuple type
        if len(t) == 4:
            idx = t[0] - 1
            features[248 + idx] += 1
        if len(t) == 3:
            # Pong case
            if t[0] == t[1] == t[2]:
                idx = t[0] - 1
                features[214 + idx] += 1
            else:
                # Chow case
                t.sort()
                idx = chow_id_mapping.get(t[0], None)
                if idx is not None:
                    # Apply normalization
                    features[282 + idx] += 1 / 4

    # Previous side player call tuple encoding (assume all tuples are valid)
    for t in state['previous_player_called_tuples']:
        # Check tuple type
        if len(t) == 4:
            idx = t[0] - 1
            features[337 + idx] += 1
        if len(t) == 3:
            # Pong case
            if t[0] == t[1] == t[2]:
                idx = t[0] - 1
                features[303 + idx] += 1
            else:
                # Chow case
                t.sort()
                idx = chow_id_mapping.get(t[0], None)
                if idx is not None:
                    # Apply normalization
                    features[371 + idx] += 1 / 4

    # Action tile encoding
    if state['action_tile']:
        action_tile_id = state['action_tile'] - 1
        features[392 + action_tile_id] = 1

    # Discard pool encoding
    for tile in state['discard_pool']:
        t_id = tile - 1
        # Apply normalization
        features[426 + t_id] += 1 / 4

    return features