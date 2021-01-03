//
//  ContentView.swift
//  personal-scoreboard
//
//  Created by Sajan  Gutta on 12/20/20.
//

import SwiftUI

struct ContentView: View {
    @State var sport_type: SportType = SportType.nfl
    @State var loading_event_info: Bool = true
    @State var nfl_events: [String] = []
    @State var nba_events: [String] = []
    @State var nhl_events: [String] = []
    @State var mlb_events: [String] = []
    @State var nfl_event_objs: Dictionary<String, Event> = Dictionary<String, Event>()
    @State var nba_event_objs: Dictionary<String, Event> = Dictionary<String, Event>()
    @State var nhl_event_objs: Dictionary<String, Event> = Dictionary<String, Event>()
    @State var mlb_event_objs: Dictionary<String, Event> = Dictionary<String, Event>()
    
    var body: some View {
        Text("Personal Scoreboard")
            .font(.title)
            .multilineTextAlignment(.center)
            .padding(.top).onAppear(perform: updateEventIds)
        
        Picker("Sport Type", selection: $sport_type) {
            ForEach(SportType.allCases, id: \.self) { this_type in
                Text(this_type.rawValue).tag(this_type)
            }
        }
        .pickerStyle(SegmentedPickerStyle())
        .labelsHidden()
        .padding(.leading).padding(.trailing)
        
        if loading_event_info {
            Text("Loading").foregroundColor(.red)
        }
        
        let gridItems = [GridItem(.fixed(275), spacing: 10, alignment: .center),
                                 GridItem(.fixed(275), spacing: 0, alignment: .center)]
        
        let current_event_objs = getCurrentEventObjsList(sport_type: self.sport_type)
        
        ScrollView(.vertical) {
            LazyVGrid(columns: gridItems, spacing: 10) {
                ForEach(Array(current_event_objs.keys), id: \.self) { event_id in
                    let this_event = current_event_objs[event_id]
                    EventView(event: this_event!)
                }
            }.padding(5)
        }
    }
    
    func getCurrentEventObjsList(sport_type: SportType) -> Dictionary<String, Event> {
        if sport_type == SportType.nfl {
            return self.nfl_event_objs
        } else if sport_type == SportType.nba {
            return self.nba_event_objs
        } else if sport_type == SportType.nhl {
            return self.nhl_event_objs
        } else if sport_type == SportType.mlb {
            return self.mlb_event_objs
        } else {
            return Dictionary<String, Event>()
        }
    }
    
    func updateEventIds() {
        let url = "PLACEHOLDER URL"
        getUserEvents(url: url) { result in
            self.nfl_events = result["NFL"] ?? []
            self.nba_events = result["NBA"] ?? []
            self.nhl_events = result["NHL"] ?? []
            self.mlb_events = result["MLB"] ?? []
            self.loading_event_info = false
            renderEvents()
        }
    }
    
    func renderEvents() {
        let BASE_URL = "http://127.0.0.1:5000/api/events"
        for event_id in self.nfl_events {
            let url = BASE_URL + "/NFL/" + event_id
            getEventInfo(url: url) { output in
                let retrieved_id = output.id
                self.nfl_event_objs[retrieved_id] = output
            }
        }
        for event_id in self.nba_events {
            let url = BASE_URL + "/NBA/" + event_id
            getEventInfo(url: url) { output in
                let retrieved_id = output.id
                self.nba_event_objs[retrieved_id] = output
            }
        }
        for event_id in self.nhl_events {
            let url = BASE_URL + "/NHL/" + event_id
            getEventInfo(url: url) { output in
                let retrieved_id = output.id
                self.nhl_event_objs[retrieved_id] = output
            }
        }
        for event_id in self.mlb_events {
            let url = BASE_URL + "/MLB/" + event_id
            getEventInfo(url: url) { output in
                let retrieved_id = output.id
                self.mlb_event_objs[retrieved_id] = output
            }
        }

    }
}


struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
