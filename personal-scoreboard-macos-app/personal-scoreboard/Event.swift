//
//  Event.swift
//  personal-scoreboard
//
//  Created by Sajan  Gutta on 1/1/21.
//

import Foundation

class Event {
    var away_team: Team
    var home_team: Team
    var sport_type: SportType
    var away_score: String
    var home_score: String
    var status_string: String
    var yardage_string: String
    
    init(away_team: Team, home_team: Team, sport_type: SportType, away_score: String, home_score: String, status_string: String, yardage_string: String){
        self.away_team = away_team
        self.home_team = home_team
        self.away_score = away_score
        self.home_score = home_score
        self.sport_type = sport_type
        self.status_string = status_string
        self.yardage_string = yardage_string
    }
}
