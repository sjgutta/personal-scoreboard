//
//  RequestFunctions.swift
//  personal-scoreboard
//
//  Created by Sajan  Gutta on 1/2/21.
//

import Foundation
import Alamofire
import SwiftyJSON

func loginUser(url: String, username: String, password: String, completionHandler : @escaping (JSON) -> Void) {
    let auth_parameters = ["username": username, "password": password]
    doPostRequest(url: url, parameters: auth_parameters) { output in
        completionHandler(output)
    }
}

func getEventInfo(url: String, request_key: String, completionHandler : @escaping (Event) -> Void) {
    let request_parameters = ["secret_key": request_key]
    doPostRequest(url: url, parameters: request_parameters) { output in
        //parsing id
        let event_id = output["id"].stringValue
        
        // parsing teams
        let away_team_name = output["away_team"]["name"].stringValue
        let away_team_logo = output["away_team"]["logo_url"].stringValue
        let away_team = Team(full_name: away_team_name, logo_url: away_team_logo)
        
        let home_team_name = output["home_team"]["name"].stringValue
        let home_team_logo = output["home_team"]["logo_url"].stringValue
        let home_team = Team(full_name: home_team_name, logo_url: home_team_logo)
        
        // parsing sport type
        let sport_string = output["sport"].stringValue
        var sport_type = SportType.nfl
        if sport_string == "NBA" {
            sport_type = SportType.nba
        } else if sport_string == "NHL" {
            sport_type = SportType.nhl
        } else if sport_string == "MLB" {
            sport_type = SportType.mlb
        } else if sport_string == "NCAAM" {
            sport_type = SportType.ncaam
        } else if sport_string == "SOCCER" {
            sport_type = SportType.soccer
        }
        
        //parsing scores
        let away_score = output["away_score"].stringValue
        let home_score = output["home_score"].stringValue
        
        //parsing status info
        let status = output["status"].stringValue
        let status_string = output["status_string"].stringValue
        
        //parsing yardage string and possession
        var yardage_string = ""
        if output["yardage_string"].exists() {
            yardage_string = output["yardage_string"].stringValue
        }
        
        var possession = ""
        if output["possession"].exists() {
            possession = output["possession"].stringValue
        }
        
        let result = Event(id: event_id, away_team: away_team, home_team: home_team, sport_type: sport_type, away_score: away_score, home_score: home_score, status: status, status_string: status_string, yardage_string: yardage_string, possession: possession)
        
        completionHandler(result)
    }
}

func getUserEvents(url: String, username: String, password: String, request_key: String, completionHandler : @escaping (Dictionary<String, [String]>) -> Void) {
    let auth_parameters = ["username": username, "password": password, "secret_key": request_key]
    doPostRequest(url: url, parameters: auth_parameters) { output in
        var result = Dictionary<String, [String]>()
        for sport in SportType.allCases {
            result[sport.rawValue] = [String]()
        }
        if output["error"].exists() {
            completionHandler(result)
        }
        
        let id_list:JSON = output["events"]
        for (_, subJson):(String, JSON) in id_list {
            let this_event_sport: String = subJson["sport"].stringValue
            var this_event_id: String = subJson["id"].stringValue
            if this_event_sport == "SOCCER" && subJson["league"].exists() {
                this_event_id = subJson["league"].stringValue + "/" + this_event_id
            }
            result[this_event_sport]?.append(this_event_id)
        }
        
        completionHandler(result)
    }
}

func doGetRequest(url: String, completionHandler : @escaping (JSON) -> Void){
    AF.request(url, method: .get).validate().responseJSON { response in
        switch response.result {
        case .success(let value):
            let json = JSON(value)
            completionHandler(json)
        case .failure(let error):
            print(error)
        }
    }
}

func doPostRequest(url: String, parameters: Dictionary<String, String>, completionHandler : @escaping (JSON) -> Void){
    AF.request(url, method: .post, parameters: parameters, encoding: JSONEncoding.default).validate().responseJSON { response in
        switch response.result {
        case .success(let value):
            let json = JSON(value)
            completionHandler(json)
        case .failure(let error):
            completionHandler(["error": error])
            print(error)
        }
    }
}
