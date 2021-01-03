//
//  RequestFunctions.swift
//  personal-scoreboard
//
//  Created by Sajan  Gutta on 1/2/21.
//

import Foundation
import Alamofire
import SwiftyJSON

func getUserEvents(url: String, completionHandler : @escaping ([String]) -> Void) {
    doGetRequest(url: url) { output in
        let id_list:[String] = output["event_ids"].arrayValue.map { $0.stringValue}
        completionHandler(id_list)
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
