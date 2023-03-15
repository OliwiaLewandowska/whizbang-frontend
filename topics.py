topics_dict = {
    "gameplay": ["gameplay", "mechanic", "mechanics", "objective", "objectives", "challenge", "strategy", "tactic", "tactics", "exploration", "sandbox", "freedom", "level design", "combat system"],
    "graphics": ["graphics", "art", "art & graphics", "resolution", "framerate", "cinematic", "cinematics", "world design"],
    "story": ["story", "plot", "narrative", "dialogue", "character", "characters", "world-building", "lore", "twist", "twists", "climax", "climaxes", "story pacing", "writing quality"],
    "sound": ["sound", "music", "sound effect", "sound effects", "voice acting", "ambient noise", "soundtrack", "sound design", "dialogue quality"],
    "controls": ["control", "controls", "input", "responsiveness", "accuracy", "customizability", "comfort", "user interface"],
    "multiplayer": ["multiplayer", "cooperative", "competitive", "matchmaking", "teamwork", "communication", "leaderboards", "game mode", "game modes"],
    "crossplay" : ["cross-play", "crossplay", "cross play", "across platforms", "different platforms", "cross-platform", "cross platform"],
    "ai": ["AI", "ai", "artificial intelligence", "pathfinding", "difficulty scaling", "companion AI", "boss AI", "enemy AI"],
    "performance": ["performance", "loading time", "loading times", "optimization", "hardware requirement", "hardware requirements", "stability", "system requirement", "system requirements"],
    "price": ["$","price", "cost", "value", "microtransaction", "microtransactions", "DLC", "expansion", "expansions", "sale", "sales", "free-to-play", "monetization practices"],
    "length": ["length", "playtime", "campaign length", "side content", "pace", "repetitiveness", "level variety"],
    "difficulty": ["difficulty", "challenge level", "difficulty setting", "difficulty settings", "difficulty curve", "skill ceiling", "fairness"],
    "replayability": ["replayability", "new game plus", "randomization", "procedural generation", "alternate path", "alternate paths", "achievement", "achievements", "endgame content"],
    "fun": ["fun", "enjoyment", "entertainment", "excitement", "satisfaction", "reward", "rewards"],
    "immersion": ["immersion", "atmosphere", "character customization", "setting"],
    "art": ["art", "visual style", "concept art", "character design", "level design", "environmental design", "animation", "animations"],
    "pacing": ["pacing", "rhythm", "flow", "tempo", "balance", "player freedom", "mission structure"],
    "variety": ["variety", "content diversity", "enemy variety", "weapon variety", "environmental diversity", "playstyle variety", "character build", "character builds"],
    "balance": ["balance", "gameplay balance", "difficulty balance", "balanced game"],
    "bugs": ["weird bug", "bug", "bugs", "glitch", "glitches", "crash", "crashes", "lag", "lags", "freeze", "freezes", "issue", "issues", "performance problem", "performance problems"]
}


name_id_mapping = {"Condemned: Criminal Origins": 4720, "Silent Hill Homecoming": 19000, "Red Faction": 20530, "Zeno Clash": 22200, "Risen 2: Dark Waters": 40390, "Tropico 4": 57690, "Hard West": 307670, "eden*": 315810, "Down To One": 334040, "Tyranny": 362960, "Hot Lava": 382560, "12 is Better Than 6": 410110, "EARTH DEFENSE FORCE 4.1 The Shadow of New Despair": 410320, "Liftoff: FPV Drone Racing": 410340, "Skyforge": 414530, "Starpoint Gemini Warlords": 419480, "The Deed": 420740, "Armored Warfare": 443110, "Transport Fever": 446800, "There's Poop In My Soup": 449540, "Genital Jousting": 469820, "Dungeon Fighter Online": 495910, "Stories Untold": 558420, "Rakuen": 559210, "Them's Fightin' Herds": 574980, "Sunless Skies: Sovereign Edition": 596970, "Cattails | Become a Cat!": 634160, "DOOM VFR": 650000, "Neverwinter Nights: Enhanced Edition": 704450, "UNDER NIGHT IN-BIRTH Exe:Late[cl-r]": 801630, "MU Legend": 874240, "Fate Seeker": 882790, "Cat Quest II": 914710, "Yakuza Kiwami 2": 927380, "The Dungeon Of Naheulbeuk: The Amulet Of Chaos": 970830, "Cricket 19": 1028630, "Wolfenstein: Youngblood": 1056960, "Evil West": 1065310, "Drift86": 1070580, "Dungeon Defenders: Awakened": 1101190, "Florence": 1102130, "Monster Prom 2: Monster Camp": 1140270, "Mortal Online 2": 1170950, "Blackthorn Arena": 1194930, "The Jackbox Party Pack 7": 1211630, "DNF Duel": 1216060, "Alba: A Wildlife Adventure": 1337010, "Sign of Silence": 1346070, "Fate Seeker II": 1559390, "Shotgun King: The Final Checkmate": 1972440}
