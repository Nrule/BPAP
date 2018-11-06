from chicken_dinner.pubgapi import PUBG

api_key = "api-key"
pubg = PUBG(api_key, "pc-na")
shroud = pubg.players_from_names("shroud")[0]
recent_match_id = shroud.match_ids[0]
recent_match = pubg.match(recent_match_id)
recent_match_telemetry = recent_match.get_telemetry()
recent_match_telemetry.playback_animation("recent_match.html")


telemetry.playback_animation(
    "match.html",
    zoom=True,
    labels=True,
    label_players=[],
    highlight_winner=True,
    label_highlights=True,
    size=6,
    end_frames=60,
    use_hi_res=False,
    color_teams=True,  # use True for teams, False for solos
    interpolate=True,
    damage=True,
    interval=2,
    fps=30,
)