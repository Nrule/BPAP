from chicken_dinner.pubgapi import PUBG

def Apikey():
    api_key = "api-key"
    return(api_key)

def Player_Stats_Solo(playername):
    # API-KEY
    api_key = Apikey()
    # (server) beschreibt, von wo die Daten bezogen werden sollen
    pubg = PUBG(api_key, "pc-eu")
    shroud = pubg.players_from_names(playername)[0]
    shroud_season = shroud.get_current_season()
    solo_tpp_stats = shroud_season.game_mode_stats("solo")
    solo_fpp_stats = shroud_season.game_mode_stats("solo", "fpp")

    solo_tpp_stats_dict = {}
    solo_tpp_stats_dict['wins'] = solo_tpp_stats['solo']['wins']
    solo_tpp_stats_dict['kills'] = solo_tpp_stats['solo']['kills']
    solo_tpp_stats_dict['assists'] = solo_tpp_stats['solo']['assists']
    solo_tpp_stats_dict['best_rank_point'] = solo_tpp_stats['solo']['best_rank_point']
    solo_tpp_stats_dict['boosts'] = solo_tpp_stats['solo']['boosts']
    solo_tpp_stats_dict['dbnos'] = solo_tpp_stats['solo']['dbnos']
    solo_tpp_stats_dict['daily_kills'] = solo_tpp_stats['solo']['daily_kills']
    solo_tpp_stats_dict['daily_wins'] = solo_tpp_stats['solo']['daily_wins']
    solo_tpp_stats_dict['damage_dealt'] = solo_tpp_stats['solo']['damage_dealt']
    solo_tpp_stats_dict['days'] = solo_tpp_stats['solo']['days']
    solo_tpp_stats_dict['headshot_kills'] = solo_tpp_stats['solo']['headshot_kills']
    solo_tpp_stats_dict['kill_points'] = solo_tpp_stats['solo']['kill_points']
    solo_tpp_stats_dict['longest_kill'] = solo_tpp_stats['solo']['longest_kill']
    solo_tpp_stats_dict['longest_time_survived'] = solo_tpp_stats['solo']['longest_time_survived']
    solo_tpp_stats_dict['losses'] = solo_tpp_stats['solo']['losses']
    solo_tpp_stats_dict['max_kill_streaks'] = solo_tpp_stats['solo']['max_kill_streaks']
    solo_tpp_stats_dict['most_survival_time'] = solo_tpp_stats['solo']['most_survival_time']
    solo_tpp_stats_dict['rank_points'] = solo_tpp_stats['solo']['rank_points']
    solo_tpp_stats_dict['revives'] = solo_tpp_stats['solo']['revives']
    solo_tpp_stats_dict['ride_distance'] = solo_tpp_stats['solo']['ride_distance']
    solo_tpp_stats_dict['road_kills'] = solo_tpp_stats['solo']['road_kills']
    solo_tpp_stats_dict['round_most_kills'] = solo_tpp_stats['solo']['round_most_kills']
    solo_tpp_stats_dict['rounds_played'] = solo_tpp_stats['solo']['rounds_played']
    solo_tpp_stats_dict['suicides'] = solo_tpp_stats['solo']['suicides']
    solo_tpp_stats_dict['swim_distance'] = solo_tpp_stats['solo']['swim_distance']
    solo_tpp_stats_dict['team_kills'] = solo_tpp_stats['solo']['team_kills']
    solo_tpp_stats_dict['time_survived'] = solo_tpp_stats['solo']['time_survived']
    solo_tpp_stats_dict['top_10s'] = solo_tpp_stats['solo']['top_10s']
    solo_tpp_stats_dict['vehicle_destroys'] = solo_tpp_stats['solo']['vehicle_destroys']
    solo_tpp_stats_dict['walk_distance'] = solo_tpp_stats['solo']['walk_distance']
    solo_tpp_stats_dict['weapons_acquired'] = solo_tpp_stats['solo']['weapons_acquired']
    solo_tpp_stats_dict['weekly_kills'] = solo_tpp_stats['solo']['weekly_kills']
    solo_tpp_stats_dict['weekly_wins'] = solo_tpp_stats['solo']['weekly_wins']
    solo_tpp_stats_dict['win_points'] = solo_tpp_stats['solo']['win_points']


    solo_fpp_stats_dict = {}
    solo_fpp_stats_dict['wins'] = solo_fpp_stats['wins']
    solo_fpp_stats_dict['kills'] = solo_fpp_stats['kills']
    solo_fpp_stats_dict['assists'] = solo_fpp_stats['assists']
    solo_fpp_stats_dict['best_rank_point'] = solo_fpp_stats['best_rank_point']
    solo_fpp_stats_dict['boosts'] = solo_fpp_stats['boosts']
    solo_fpp_stats_dict['dbnos'] = solo_fpp_stats['dbnos']
    solo_fpp_stats_dict['daily_kills'] = solo_fpp_stats['daily_kills']
    solo_fpp_stats_dict['daily_wins'] = solo_fpp_stats['daily_wins']
    solo_fpp_stats_dict['damage_dealt'] = solo_fpp_stats['damage_dealt']
    solo_fpp_stats_dict['days'] = solo_fpp_stats['days']
    solo_fpp_stats_dict['headshot_kills'] = solo_fpp_stats['headshot_kills']
    solo_fpp_stats_dict['kill_points'] = solo_fpp_stats['kill_points']
    solo_fpp_stats_dict['longest_kill'] = solo_fpp_stats['longest_kill']
    solo_fpp_stats_dict['longest_time_survived'] = solo_fpp_stats['longest_time_survived']
    solo_fpp_stats_dict['losses'] = solo_fpp_stats['losses']
    solo_fpp_stats_dict['max_kill_streaks'] = solo_fpp_stats['max_kill_streaks']
    solo_fpp_stats_dict['most_survival_time'] = solo_fpp_stats['most_survival_time']
    solo_fpp_stats_dict['rank_points'] = solo_fpp_stats['rank_points']
    solo_fpp_stats_dict['revives'] = solo_fpp_stats['revives']
    solo_fpp_stats_dict['ride_distance'] = solo_fpp_stats['ride_distance']
    solo_fpp_stats_dict['road_kills'] = solo_fpp_stats['road_kills']
    solo_fpp_stats_dict['round_most_kills'] = solo_fpp_stats['round_most_kills']
    solo_fpp_stats_dict['rounds_played'] = solo_fpp_stats['rounds_played']
    solo_fpp_stats_dict['suicides'] = solo_fpp_stats['suicides']
    solo_fpp_stats_dict['swim_distance'] = solo_fpp_stats['swim_distance']
    solo_fpp_stats_dict['team_kills'] = solo_fpp_stats['team_kills']
    solo_fpp_stats_dict['time_survived'] = solo_fpp_stats['time_survived']
    solo_fpp_stats_dict['top_10s'] = solo_fpp_stats['top_10s']
    solo_fpp_stats_dict['vehicle_destroys'] = solo_fpp_stats['vehicle_destroys']
    solo_fpp_stats_dict['walk_distance'] = solo_fpp_stats['walk_distance']
    solo_fpp_stats_dict['weapons_acquired'] = solo_fpp_stats['weapons_acquired']
    solo_fpp_stats_dict['weekly_kills'] = solo_fpp_stats['weekly_kills']
    solo_fpp_stats_dict['weekly_wins'] = solo_fpp_stats['weekly_wins']
    solo_fpp_stats_dict['win_points'] = solo_fpp_stats['win_points']
    return solo_tpp_stats_dict, solo_fpp_stats_dict
