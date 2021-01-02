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
        
        if self.sport_type == SportType.nfl {
            Text("Hello, NFL!")
                .frame(maxWidth: .infinity, maxHeight: .infinity)
        } else {
            Text("Hello, Not NFL!")
                .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
        
        HStack{
            EventView().padding(.leading)
            Spacer()
            EventView().padding(.trailing)
        }.padding(.bottom)
    }
}


struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
