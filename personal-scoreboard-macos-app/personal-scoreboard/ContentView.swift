//
//  ContentView.swift
//  personal-scoreboard
//
//  Created by Sajan  Gutta on 12/20/20.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        Text("Hello, Scoreboard!")
            .frame(maxWidth: .infinity, maxHeight: .infinity)
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
