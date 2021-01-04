//
//  Event.swift
//  personal-scoreboard
//
//  Created by Sajan  Gutta on 1/1/21.
//

import Foundation

class Event {
    var id: String
    var away_team: Team
    var home_team: Team
    var sport_type: SportType
    var away_score: String
    var home_score: String
    var status: String
    var status_string: String
    var yardage_string: String
    var possession: String
    
    var home_possession: Bool {
        return sport_type == SportType.nfl && possession == "HOME"
    }
    
    var away_possession: Bool {
        return sport_type == SportType.nfl && possession == "AWAY"
    }
    
    var event_info: String {
        return "\(home_team.full_name) vs \(away_team.full_name)"
    }
    
    var espn_url: String {
        let BASE = "https://www.espn.com"
        if sport_type == SportType.nfl {
            return BASE + "/nfl/game/_/gameId/\(id)"
        } else if sport_type == SportType.nba {
            return BASE + "/nba/game?gameId=\(id)"
        } else if sport_type == SportType.nhl {
            return BASE + "/nhl/boxscore/_/gameId/\(id)"
        } else if sport_type == SportType.mlb {
            return BASE + "/mlb/game?gameId=\(id)"
        } else {
            return BASE
        }
    }
    
    init(id: String, away_team: Team, home_team: Team, sport_type: SportType, away_score: String, home_score: String, status: String, status_string: String, yardage_string: String, possession: String){
        self.id = id
        self.away_team = away_team
        self.home_team = home_team
        self.away_score = away_score
        self.home_score = home_score
        self.sport_type = sport_type
        self.status = status
        self.status_string = status_string
        if sport_type == SportType.nfl {
            self.yardage_string = yardage_string
        } else {
            self.yardage_string = ""
        }
        self.possession = possession
    }
}
