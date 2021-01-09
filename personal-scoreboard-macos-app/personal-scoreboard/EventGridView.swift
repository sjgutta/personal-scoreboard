//
//  EventGridView.swift
//  personal-scoreboard
//
//  Created by Sajan  Gutta on 1/9/21.
//

import SwiftUI

struct EventGridView: View {
    var event_list: Dictionary<String, Event>
    
    var body: some View {
        let rows = self.getRows()
        VStack (alignment: .leading) {
            ForEach(rows, id: \.self) { event_ids in
                let left_id = event_ids[0]
                HStack () {
                    if event_ids.count == 2 {
                        let right_id = event_ids [1]
                        EventView(event: event_list[left_id]!)
                        EventView(event: event_list[right_id]!)
                    } else if event_ids.count == 1 {
                        EventView(event: event_list[left_id]!)
                        Spacer()
                    }
                }
            }
        }
    }
    
    func getRows() -> [[String]] {
        var result: [[String]] = [[String]]()
        if event_list.count == 0 {
            return result
        }
        for index in 0...event_list.count - 1 {
            if index % 2 == 0 {
                let this_key = Array(event_list.keys)[index]
                if index == event_list.count - 1{
                    result.append([this_key])
                } else {
                    let next_key = Array(event_list.keys)[index + 1]
                    result.append([this_key, next_key])
                }
            }
        }
        return result
    }
}

struct EventGridView_Previews: PreviewProvider {
    static var previews: some View {
        let lions = Team(full_name: "Detroit Lions", logo_url: "https://a.espncdn.com/i/teamlogos/nfl/500/det.png")
        let rams = Team(full_name: "Los Angeles Rams", logo_url: "https://a.espncdn.com/i/teamlogos/nfl/500/lar.png")
        
        let nfl_event = Event(id: "1", away_team: lions, home_team: rams, sport_type: SportType.nfl, away_score: "7", home_score: "10", status: "IN PROGRESS", status_string: "Q4 | 10:45", yardage_string: "4th and 5 at DET 35", possession: "AWAY")
        
        let events = ["1": nfl_event, "2": nfl_event, "3": nfl_event]
        EventGridView(event_list: events)
    }
}
