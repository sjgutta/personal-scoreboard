//
//  Team.swift
//  personal-scoreboard
//
//  Created by Sajan  Gutta on 1/1/21.
//

import Foundation
import SwiftUI

class Team {
    var full_name: String
    var logo_url: String
    
    var logo_image: Image {
        return Image(full_name).resizable()
    }
    
    init(full_name: String, logo_url: String) {
        self.full_name = full_name
        self.logo_url = logo_url
    }
}
