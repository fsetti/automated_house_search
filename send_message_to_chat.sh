#!/bin/sh
recipient="iMessage;+;chat693490188607394227"
message="$1"
echo "$recipient"
cat<<EOF | osascript - "${recipient}" "${message}"
on run {targetChatID, targetMessage}
   tell application "Messages"
    set targetChat to a reference to text chat id targetChatID
    send targetMessage to targetChat
   end tell
end run
EOF
