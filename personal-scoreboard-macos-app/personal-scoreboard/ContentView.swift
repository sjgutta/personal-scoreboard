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
    
    var body: some View {
        Text("Personal Scoreboard")
            .font(.title)
            .multilineTextAlignment(.center)
            .padding(.top)
        
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
        
        let current_event_ids = getCurrentEventList()
        
        Text(current_event_ids.joined(separator: ", ")).onAppear(perform: updateEventIds)
        
        let lions = Team(full_name: "Detroit Lions", logo_url: "https://a.espncdn.com/i/teamlogos/nfl/500/det.png")
        let rams = Team(full_name: "Los Angeles Rams", logo_url: "https://a.espncdn.com/i/teamlogos/nfl/500/lar.png")
        let clippers = Team(full_name: "LA Clippers", logo_url: "https://a.espncdn.com/i/teamlogos/nba/500/lac.png")
        let lakers = Team(full_name: "Los Angeles Lakers", logo_url: "https://a.espncdn.com/i/teamlogos/nba/500/lal.png")
        
        let nfl_event = Event(away_team: lions, home_team: rams, sport_type: SportType.nfl, away_score: "7", home_score: "10", status: "IN PROGRESS", status_string: "Q4 | 10:45", yardage_string: "4th and 5 at DET 35", possession: "AWAY")
        
        let nba_event = Event(away_team: clippers, home_team: lakers, sport_type: SportType.nba, away_score: "94", home_score: "100", status: "FINAL", status_string: "Q4 | 24.5", yardage_string: "Not relevant", possession: "NONE")
        
        if self.sport_type == SportType.nfl {
            Text("Hello, NFL!")
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            HStack{
                EventView(event: nfl_event).padding(.leading)
                Spacer()
                EventView(event: nfl_event).padding(.trailing)
            }.padding(.bottom)
        } else {
            Text("Hello, Not NFL!")
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            HStack{
                EventView(event: nba_event).padding(.leading)
                Spacer()
                EventView(event: nba_event).padding(.trailing)
            }.padding(.bottom)
        }
    }
    
    func getCurrentEventList() -> [String] {
        if self.sport_type == SportType.nfl {
            return self.nfl_events
        } else if self.sport_type == SportType.nba {
            return self.nba_events
        } else if self.sport_type == SportType.nhl {
            return self.nhl_events
        } else if self.sport_type == SportType.mlb {
            return self.mlb_events
        } else {
            return []
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
        }
    }
}


struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
