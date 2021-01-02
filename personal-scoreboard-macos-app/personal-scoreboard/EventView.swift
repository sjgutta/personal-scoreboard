//
//  SwiftUIView.swift
//  personal-scoreboard
//
//  Created by Sajan  Gutta on 12/31/20.
//

import SwiftUI

struct EventView: View {
    var body: some View {
        VStack {
            HStack {
                Text("4th Quarter").padding(.leading)
                Spacer()
                Text("4TH and 10 at DET 45").padding(.trailing)
            }.padding(.top, 10)
            HStack {
                Text("Detroit Lions").padding(.leading)
                Spacer()
                Text("5").bold().padding(.trailing)
            }.padding(.top, 15)
            HStack {
                Text("LA Rams").padding(.leading)
                Spacer()
                Text("10").bold().padding(.trailing)
            }.padding(.top, 5).padding(.bottom, 10)
        }.frame(width: 275).overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(Color.blue, lineWidth: 1)
        )
    }
}

struct EventView_Previews: PreviewProvider {
    static var previews: some View {
        EventView()
    }
}
