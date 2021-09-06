# Data Retrieval App Script

Create a new Google Sheet or copy [this one](https://docs.google.com/spreadsheets/d/1PNigfMZxkcFCL-bBftrlsnI27p0M-1DBATydvOtGVuk/edit?usp=sharing).
Goto Tools, Script Editor and Paste the .gs Files (if you copied the Sheet they should alread be present). Reload your Sheet and Authorize the Script.

Now you need to Configure the API Keys, with the newly added "API Config" Menu
  - [YouTube](https://console.cloud.google.com/apis/credentials)
  - [Twitter](https://developer.twitter.com/en/portal/dashboard)
  - [Twitch](https://dev.twitch.tv/console/apps)

Now you should be able to retrieve follower counts with the following functions

For Twitch:
```
=TWITCHFOLLOWER(TWITCHID("bennet0496"))
=TWITCHFOLLOWER(TWITCHID(A2))
```
_Twitch Followers need to be retrieved by ID, so you need to get the ID first_

For Twitter:
```
=TWITTERFOLLOWER("bennet0496")
=TWITTERFOLLOWER(A3)
```

For YouTube:
```
=YOUTUBESUBS("UCJzpXG59mOQjh8vukSNq-Hg")
=YOUTUBESUBS(A4)
```
_YouTube also needs the Channel ID, this can be retrieved from the Channel URL e.g. 
`https://www.youtube.com/channel/UCJzpXG59mOQjh8vukSNq-Hg` has the ID `UCJzpXG59mOQjh8vukSNq-Hg`._
_This will not work with custom channel links or names if the URL for a channel is not `/channel/...`,
you can get by clicking on channel from an Community Post or Video of the Channel._

Bulk retrieval to create averages are also possible
```
=AVERAGE(YOUTUBESUB_MAP(SPLIT(G2,",")))
=AVERAGE(TWITTERFOLLOWER_MAP(SPLIT(E2,",")))
```