

# --- Criteria functions ---
def is_forest(game, x, y, entity=None):
    return game.map.get_tile(x, y).terrain == "Forest"

def is_land(game, x, y, entity=None):
    return game.map.get_tile(x, y).elevation != 0