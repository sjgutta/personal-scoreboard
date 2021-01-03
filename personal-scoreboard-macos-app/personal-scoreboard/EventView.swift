//
//  SwiftUIView.swift
//  personal-scoreboard
//
//  Created by Sajan  Gutta on 12/31/20.
//

import SwiftUI

struct EventView: View {
    @State var event: Event
    
    var body: some View {
        VStack {
            HStack {
                Text(self.event.status_string).padding(.leading)
                Spacer()
                Text(self.event.yardage_string).padding(.trailing)
            }.padding(.top, 10)
            HStack {
                self.event.away_team.logo_image.aspectRatio(contentMode: .fit).frame(width: 35).padding(.leading, 5)
                Text(self.event.away_team.full_name).padding(.leading, 5)
                if self.event.away_possession {
                    Text("🏈")
                }
                Spacer()
                Text(self.event.away_score).bold().padding(.trailing)
            }.padding(.top, 5)
            HStack {
                self.event.home_team.logo_image.aspectRatio(contentMode: .fit).frame(width: 35).padding(.leading, 5)
                Text(self.event.home_team.full_name).padding(.leading, 5)
                if self.event.home_possession {
                    Text("🏈")
                }
                Spacer()
                Text(self.event.home_score).bold().padding(.trailing)
            }.padding(.bottom, 10)
        }.frame(width: 275).overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(Color.blue, lineWidth: 1)
        )
    }
}

struct EventView_Previews: PreviewProvider {
    static var previews: some View {
        let lions = Team(full_name: "Detroit Lions", logo_url: "https://a.espncdn.com/i/teamlogos/nfl/500/det.png")
        let rams = Team(full_name: "Los Angeles Rams", logo_url: "https://a.espncdn.com/i/teamlogos/nfl/500/lar.png")
        
        let nfl_event = Event(id: "1", away_team: lions, home_team: rams, sport_type: SportType.nfl, away_score: "7", home_score: "10", status: "IN PROGRESS", status_string: "Q4 | 10:45", yardage_string: "4th and 5 at DET 35", possession: "AWAY")
        
        EventView(event: nfl_event)
    }
}
