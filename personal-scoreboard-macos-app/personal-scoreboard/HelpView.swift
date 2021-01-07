//
//  HelpView.swift
//  personal-scoreboard
//
//  Created by Sajan  Gutta on 1/6/21.
//

import SwiftUI

struct HelpQuestion: View {
    var question: String
    var answer: String
    
    var body: some View {
        VStack (alignment: .leading) {
            Text(self.question)
                .font(.headline).bold().multilineTextAlignment(.leading).fixedSize(horizontal: false, vertical: true)
            Text(self.answer).multilineTextAlignment(.leading).fixedSize(horizontal: false, vertical: true)
        }.padding(.bottom, 10)
    }
}

struct HelpView: View {
    var body: some View {
        VStack (alignment: .leading) {
            HelpQuestion(question: "Has a game started but it still says Upcoming?", answer: "Use the refresh events button to solve this problem!")
            HelpQuestion(question: "Have you added a new favorite on the website but the team's game isn't showing up here?", answer: "Use the refresh events button to solve this problem as well!")
            HelpQuestion(question: "Logged into your account but events not loading in?", answer: "Something probably changed on our end. Try logging in and logging out to solve the problem.")
            HelpQuestion(question: "Unable to solve the problem?", answer: "Check our website at www.mypersonalscoreboard.com for updates or to contact us about your issue.")
        }.padding(.leading, 25).padding(.trailing, 25)
    }
}

struct HelpView_Previews: PreviewProvider {
    static var previews: some View {
        HelpView()
    }
}
