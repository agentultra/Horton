ENEMY_STATES = ['aggressive', 'passive']

def new_enemy(x, y):
    return {'position': (x, y),
            'state': 'passive'}
