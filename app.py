from flask import Flask, render_template, request, redirect

from arena import Arena
from equipment import Equipment
from classes import unit_classes
from unit import PlayerUnit, EnemyUnit

app = Flask(__name__)

heroes = {}

arena = Arena()
equipment = Equipment()


@app.route("/")
def menu_page():
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    arena.start_game(**heroes)
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    if arena.is_active:
        result = arena.player_hit()
        return render_template('fight.html', heroes=heroes, result=result)
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/use-skill")
def use_skill():
    if arena.is_active:
        result = arena.player_use_skill()
        return render_template('fight.html', heroes=heroes, result=result)
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.is_active:
        result = arena.next_turn()
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    return render_template("index.html", heroes=heroes)


@app.get("/choose-hero/")
def choose_hero():
    result = {
        "header": 'Choose hero',
        "classes": unit_classes,
        "weapons": equipment.get_weapons_names(),
        "armors": equipment.get_armors_names()
    }
    return render_template('hero_choosing.html', result=result)


@app.post("/choose-hero/")
def choose_hero_post():
    player = PlayerUnit(
        name=request.form['name'],
        unit_class=unit_classes.get(request.form['unit_class'])
    )
    player.equip_weapon(equipment.get_weapon(request.form['weapon']))
    player.equip_armor(equipment.get_armor(request.form['armor']))

    heroes['player'] = player
    return redirect('/choose-enemy/')


@app.get("/choose-enemy/")
def choose_enemy():
    result = {
        "header": 'Choose enemy',
        "classes": unit_classes,
        "weapons": equipment.get_weapons_names(),
        "armors": equipment.get_armors_names()
    }
    return render_template('hero_choosing.html', result=result)


@app.post("/choose-enemy/")
def choose_enemy_post():
    enemy = EnemyUnit(
        name=request.form['name'],
        unit_class=unit_classes.get(request.form['unit_class'])
    )
    enemy.equip_weapon(equipment.get_weapon(request.form['weapon']))
    enemy.equip_armor(equipment.get_armor(request.form['armor']))

    heroes['enemy'] = enemy
    return redirect('/fight/')


if __name__ == "__main__":
    app.run()
