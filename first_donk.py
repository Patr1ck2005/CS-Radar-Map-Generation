from demoparser2 import DemoParser
import pandas as pd
from matplotlib import pyplot as plt

parser = DemoParser("demo/faze-vs-spirit-m1-nuke.dem")
# ticks_df = parser.parse_ticks(
#     ['spotted', 'approximate_spotted_by', 'velocity', 'health', 'shots_fired', 'game_time', 'FIRE'],
#     ticks=range(2200, 10000))
# ticks_df[ticks_df['name'].isin(['broky', 'zont1x'])].to_csv('ticks_df.csv')
# print(parser.list_game_events())
# # If you just want the names of all events then you can use this:
# event_names = parser.list_game_events()
#
# # Currently the event "all" gives you all events. Cursed solution for now
# df = parser.parse_events(["player_hurt", 'weapon_fire'], player_extra=['yaw', 'pitch', 'approximate_spotted_by'])
# print(df)
# df[0][1].to_csv(f"{df[0][0]}.csv")
# df[1][1].to_csv(f"{df[1][0]}.csv")

player_hurt_events = parser.parse_event("player_hurt", player_extra=['health'])
player_hurt_events.to_csv(f"debug_player_hurt.csv")
player_death_events = parser.parse_event("player_death")
aim_df = parser.parse_ticks(["pitch", "yaw"])

shoot_process = []
hurt_tick_domains = []
tick = 0
start_tick = None
for (idx, event) in player_hurt_events.iterrows():
    if event['attacker_name'] == 'donk':
        if start_tick is None:
            start_tick = event["tick"]
        else:
            if event['health'] == 0:
                end_tick = event["tick"]
                hurt_tick_domains.append((start_tick, end_tick))
                start_tick = None
            elif event['tick'] - start_tick > 64:
                end_tick = start_tick
                hurt_tick_domains.append((start_tick, end_tick))
                start_tick = None
    if tick == event['tick']:
        pass
    else:
        tick = event['tick']

print(hurt_tick_domains)
for i, (start_tick, end_tick) in enumerate(hurt_tick_domains):
    subdf = aim_df[(aim_df["tick"].between(start_tick, end_tick)) & (aim_df["name"] == str('donk'))]
    plt.plot(subdf["yaw"], subdf["pitch"], '-o', label=f'donk {i}')
    plt.legend()
    plt.show()
    subdf.to_csv(f"donk.csv")
    # attacker can be none when player gets hurt by c4 etc.
    # if attacker != None:
    #     subdf = aim_df[(aim_df["tick"].between(start_tick, end_tick)) & (aim_df["name"] == str(attacker))]
    #     if attacker == "donk":
    #         subdf.to_csv(f"{attacker}.csv")
    #         break
