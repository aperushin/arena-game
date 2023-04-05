from unit import PlayerUnit, EnemyUnit

SP_REGEN = 2


class SingletonClass(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonClass, cls).__new__(cls, *args, **kwargs)
        return cls.instance


class Arena(SingletonClass):
    def __init__(self):
        self.player: PlayerUnit | None = None
        self.enemy: EnemyUnit | None = None
        self.sp_regen: int = SP_REGEN
        self.is_active = False

    def start_game(self, player: PlayerUnit, enemy: EnemyUnit):
        self.player = player
        self.enemy = enemy
        self.is_active = True

    def next_turn(self) -> str:
        if self.are_players_alive():
            self.regen_stamina()
            return self.enemy.hit(self.player)

        # If one of the players is dead, game ends
        winner = self.player if self.player.hp > 0 else self.enemy
        return f'{winner.name} won!'

    def are_players_alive(self) -> bool:
        are_alive = bool(self.player.hp and self.enemy.hp)
        if not are_alive:
            self.end_game()
        return are_alive

    def regen_stamina(self):
        self.player.regen_stamina(self.sp_regen)
        self.enemy.regen_stamina(self.sp_regen)

    def end_game(self):
        self.is_active = False

    def player_hit(self) -> str:
        player_log = self.player.hit(self.enemy)
        enemy_log = self.next_turn()
        return '\n'.join([player_log, enemy_log])

    def player_use_skill(self) -> str:
        player_log = self.player.use_skill(self.enemy)
        enemy_log = self.next_turn()
        return '\n'.join([player_log, enemy_log])
