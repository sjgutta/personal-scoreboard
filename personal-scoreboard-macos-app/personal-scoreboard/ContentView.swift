//
//  ContentView.swift
//  personal-scoreboard
//
//  Created by Sajan  Gutta on 12/20/20.
//

import SwiftUI

struct ContentView: View {
    @State var sport_type: SportType = SportType.nfl
    
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
        
        let lions = Team(full_name: "Detroit Lions")
        let rams = Team(full_name: "LA Rams")
        let clippers = Team(full_name: "LA Clippers")
        let lakers = Team(full_name: "LA Lakers")
        
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
}


struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
