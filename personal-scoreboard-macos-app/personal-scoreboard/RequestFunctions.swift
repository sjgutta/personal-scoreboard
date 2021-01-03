//
//  RequestFunctions.swift
//  personal-scoreboard
//
//  Created by Sajan  Gutta on 1/2/21.
//

import Foundation
import Alamofire
import SwiftyJSON



func getUserEvents(url: String, completionHandler : @escaping (Dictionary<String, [String]>) -> Void) {
    doGetRequest(url: url) { output in
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
            let this_event_id: String = subJson["id"].stringValue
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
