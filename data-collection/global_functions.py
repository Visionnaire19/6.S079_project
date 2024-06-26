def normalize_team_name(name):
        name_equivalence = {"Nott'ham Forest":"Nottm Forest",
                        "Nottingham Forest":"Nottm Forest",
                        "Sunderland":"Sunderland AFC", 
                        "Portsmouth":"Portsmouth FC", 
                        "Manchester Utd":"Man Utd",
                        "Manchester United":"Man Utd",
                        "Liverpool":"Liverpool FC", 
                        "Brentford":"Brentford FC", 
                        "Manchester City":"Man City",
                        "Wimbledon":"Wimbledon FC", 
                        "Sheffield Weds":"Sheff Weds",
                        "Sheffield Wednesday":"Sheff Weds",
                        "Sheffield United":"Sheff Utd",
                        "Sheffield Utd":"Sheff Utd",
                        "Tottenham":"Spurs", 
                        "Tottenham Hotspur":"Spurs",
                        "Reading":"Reading FC", 
                        "Barnsley":"Barnsley FC",
                        "Chelsea":"Chelsea FC", 
                        "Blackpool":"Blackpool FC", 
                        "Fulham":"Fulham FC", 
                        "Bournemouth":"AFC Bournemouth", 
                        "Middlesbrough":"Middlesbrough FC", 
                        "Arsenal":"Arsenal FC", 
                        "Burnley":"Burnley FC",
                        "Wolverhampton Wanderers":"Wolves",
                        "Watford":"Watford FC",
                        "West Ham":"West Ham United",
                        "Newcastle":"Newcastle United",
                        "Newcastle Utd":"Newcastle United",
                        "Blackburn":"Blackburn Rovers",
                        "Brighton & Hove Albion":"Brighton",
                        "Queens Park Rangers":"QPR",
                        "Leeds":"Leeds United",
                        "West Bromwich Albion":"West Brom",
                        "Norwich":"Norwich City",
                        "Huddersfield Town":"Huddersfield",
                        "Leicester":"Leicester City",
                        "Cardiff":"Cardiff City",
                        "Swansea":"Swansea City",
                        "Bolton Wanderers":"Bolton",
                        "Charlton Athletic":"Charlton",
                        "Charlton Ath":"Charlton",
                        "Derby":"Derby County",
                        "Ipswich":"Ipswich Town",
                        "Everton": "Everton FC", 
                        "Southampton" : "Southampton FC", 
                        "Wimbledon FC (- 2004)" : "Wimbledon FC"}
        return name_equivalence.get(name, name)