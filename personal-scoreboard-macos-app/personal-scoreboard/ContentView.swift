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
    @State var events_in_progress: [BareEvent] = []
    @State var last_event_update: Date = Date()
    @State var timer: Timer?
    
    //auth related state info
    @State var logged_in: Bool = false
    @State var username: String = ""
    @State private var password: String = ""
    @State var auth_error: String = ""
    
    let BASE_URL: String = "http://127.0.0.1:5000"
    
    var body: some View {
        VStack {
            if self.logged_in {
                VStack {
                    HStack {
                        Button(action: {
                            logout()
                        }) {
                            Text("Log Out")
                        }.padding(.leading, 20).padding(.top, 10)
                        Spacer()
                        Text("Personal Scoreboard")
                            .font(.title)
                            .multilineTextAlignment(.center)
                            .padding(.top).onAppear(perform: updateEventIds)
                        Spacer()
                        Button(action: {
                            exit(-1)
                        }) {
                            Text("Quit App")
                        }.padding(.trailing, 20).padding(.top, 10)
                    }
                    
                    HStack {
                        Button(action: {
                            updateEventIds()
                        }) {
                            Text("Refresh Events")
                        }.padding(.leading, 20).padding(.top, 10)
                        Spacer()
                        Text("Last Updated Events: \(getFormattedUpdateTime())").padding(.trailing, 20).padding(.top, 10)
                    }
                    
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
                }.onReceive(NotificationCenter.default.publisher(for: NSPopover.willCloseNotification)) { _ in
                    self.timer?.invalidate()
                    self.timer = nil
                }.onReceive(NotificationCenter.default.publisher(for: NSPopover.willShowNotification)) { _ in
                    let current_date = Date()
                    let diffComponents = Calendar.current.dateComponents([.hour], from: self.last_event_update, to: current_date)
                    if diffComponents.hour ?? 0 >= 12 {
                        updateEventIds()
                    }
                    if !(self.timer != nil) && !self.loading_event_info {
                        updateEvents()
                        self.timer = Timer.scheduledTimer(withTimeInterval: 10, repeats: true) {_ in
                            updateEvents()
                        }
                    }
                }
            } else {
                Text("Personal Scoreboard")
                    .font(.largeTitle)
                    .multilineTextAlignment(.center)
                    .padding(.top, 50).padding(.bottom, 50)
                VStack {
                    VStack {
                        Text("Login")
                            .font(.title)
                        HStack {
                            Text("Username")
                            Spacer()
                        }.padding(.top, 25)
                        TextField("Enter Username...", text: $username)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                        HStack {
                            Text("Password")
                            Spacer()
                        }.padding(.top, 15)
                        SecureField("Enter Password...", text: $password)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                        VStack {
                            Button(action: {
                                authenticate()
                            }) {
                                HStack {
                                    Text("Login")
                                }.padding(.top, 10).padding(.bottom, 10).padding(.trailing, 20).padding(.leading, 20).foregroundColor(.blue)
                                .overlay(
                                    RoundedRectangle(cornerRadius: 10.0)
                                        .stroke(Color.blue, lineWidth: 2.0)
                                )
                            }.buttonStyle(PlainButtonStyle())
                        }.padding(.top)
                        Text(self.auth_error).padding(.top).padding(.bottom).foregroundColor(.red)
                    }
                    .padding()
                    .overlay(
                            RoundedRectangle(cornerRadius: 16)
                                .stroke(Color.black, lineWidth: 1)
                        )
                }.padding(.leading, 75).padding(.trailing, 75)
                VStack {
                    Button(action: {
                        exit(-1)
                    }) {
                        Text("Quit App")
                    }
                }.padding(.top, 50)
                Text("")
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            }
        }
    }
    
    func authenticate() {
        // in future, real authentication will take place here using backend endpoint
        if self.username == "test" && self.password == "test" {
            self.auth_error = ""
            self.logged_in = true
        } else if self.username == "" {
            self.auth_error = "Must enter a username."
        } else if self.password == "" {
            self.auth_error = "Must enter a password"
        } else {
            self.auth_error = "The credentials you entered were invalid."
        }
    }
    
    func logout() {
        self.logged_in = false
        self.password = ""
        self.username = ""
        
        //must stop timer as well
        if self.timer != nil {
            self.timer?.invalidate()
            self.timer = nil
        }
    }
    
    func getFormattedUpdateTime() -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "HH:mm E, d MMM y"
        let last_update_string = formatter.string(from: self.last_event_update)
        return last_update_string
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
    
    func resetObjLists() {
        self.nfl_event_objs = Dictionary<String, Event>()
        self.nba_event_objs = Dictionary<String, Event>()
        self.nhl_event_objs = Dictionary<String, Event>()
        self.mlb_event_objs = Dictionary<String, Event>()
        self.events_in_progress = []
    }
    
    func updateEventIds() {
        print("updating event ids")
        self.loading_event_info = true
        resetObjLists()
        let url = self.BASE_URL + "/api/users/events"
        getUserEvents(url: url, username: self.username, password: self.password) { result in
            self.nfl_events = result["NFL"] ?? []
            self.nba_events = result["NBA"] ?? []
            self.nhl_events = result["NHL"] ?? []
            self.mlb_events = result["MLB"] ?? []
            let BASE_EVENT_URL = self.BASE_URL + "/api/events"
            for event_id in self.nfl_events {
                let url = BASE_EVENT_URL + "/NFL/" + event_id
                getEventInfo(url: url) { output in
                    let retrieved_id = output.id
                    if output.status == "IN PROGRESS" || output.status == "HALFTIME" {
                        let bare_event = BareEvent(id: retrieved_id, sport_type: SportType.nfl)
                        self.events_in_progress.append(bare_event)
                    }
                    self.nfl_event_objs[retrieved_id] = output
                }
            }
            for event_id in self.nba_events {
                let url = BASE_EVENT_URL + "/NBA/" + event_id
                getEventInfo(url: url) { output in
                    let retrieved_id = output.id
                    if output.status == "IN PROGRESS" || output.status == "HALFTIME" {
                        let bare_event = BareEvent(id: retrieved_id, sport_type: SportType.nba)
                        self.events_in_progress.append(bare_event)
                    }
                    self.nba_event_objs[retrieved_id] = output
                }
            }
            for event_id in self.nhl_events {
                let url = BASE_EVENT_URL + "/NHL/" + event_id
                getEventInfo(url: url) { output in
                    let retrieved_id = output.id
                    if output.status == "IN PROGRESS" || output.status == "HALFTIME" {
                        let bare_event = BareEvent(id: retrieved_id, sport_type: SportType.nhl)
                        self.events_in_progress.append(bare_event)
                    }
                    self.nhl_event_objs[retrieved_id] = output
                }
            }
            for event_id in self.mlb_events {
                let url = BASE_EVENT_URL + "/MLB/" + event_id
                getEventInfo(url: url) { output in
                    let retrieved_id = output.id
                    if output.status == "IN PROGRESS" || output.status == "HALFTIME" {
                        let bare_event = BareEvent(id: retrieved_id, sport_type: SportType.mlb)
                        self.events_in_progress.append(bare_event)
                    }
                    self.mlb_event_objs[retrieved_id] = output
                }
            }
            self.loading_event_info = false
            self.last_event_update = Date()
            if !(self.timer != nil) {
                self.timer = Timer.scheduledTimer(withTimeInterval: 10, repeats: true) {_ in
                    updateEvents()
                }
            }
        }
    }
    
    func updateEvents() {
        print("updating events")
        let BASE_EVENT_URL = self.BASE_URL + "/api/events"
        for event in self.events_in_progress {
            let url = BASE_EVENT_URL + "/\(event.sport_type.rawValue)/" + event.id
            getEventInfo(url: url) { output in
                let retrieved_id = output.id
                if event.sport_type == SportType.nfl {
                    self.nfl_event_objs[retrieved_id] = output
                } else if event.sport_type == SportType.nba {
                    self.nba_event_objs[retrieved_id] = output
                } else if event.sport_type == SportType.nhl {
                    self.nhl_event_objs[retrieved_id] = output
                } else if event.sport_type == SportType.mlb {
                    self.mlb_event_objs[retrieved_id] = output
                }
            }
        }
    }
}


struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
