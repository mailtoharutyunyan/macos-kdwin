// Turns the KDWin input sources on or off, or reports their status.
// Usage: swift tools/keyboards.swift enable|disable|status
import Carbon
import Foundation

let ids = ["org.unknown.keylayout.ArmenianKDWin", "org.unknown.keylayout.RussianKDWin"]

func sid(_ s: TISInputSource) -> String {
    Unmanaged<CFString>.fromOpaque(TISGetInputSourceProperty(s, kTISPropertyInputSourceID)).takeUnretainedValue() as String
}

func sources(includeAll: Bool) -> [TISInputSource] {
    TISCreateInputSourceList(nil, includeAll)?.takeRetainedValue() as? [TISInputSource] ?? []
}

func enabledIDs() -> Set<String> {
    Set(sources(includeAll: false).map(sid))
}

let installed = Dictionary(sources(includeAll: true).map { (sid($0), $0) }, uniquingKeysWith: { a, _ in a })
let command = CommandLine.arguments.dropFirst().first ?? "status"

switch command {
case "enable", "disable":
    var missing = false
    for id in ids {
        guard let source = installed[id] else { print("not loaded yet: \(id)"); missing = true; continue }
        // Enabling right after another change is sometimes dropped, so retry and verify.
        for _ in 0..<5 where enabledIDs().contains(id) != (command == "enable") {
            _ = command == "enable" ? TISEnableInputSource(source) : TISDisableInputSource(source)
            RunLoop.current.run(until: Date().addingTimeInterval(0.5))
        }
        print("\(enabledIDs().contains(id) ? "on " : "off"): \(id)")
    }
    exit(missing && command == "enable" ? 2 : 0)
default:
    let on = enabledIDs()
    for id in ids { print(installed[id] == nil ? "not loaded: \(id)" : "\(on.contains(id) ? "on " : "off"): \(id)") }
}
