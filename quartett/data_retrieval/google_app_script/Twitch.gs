/*    Retrieve follower counts on social media platforms
 *    Copyright (C) 2021  Bennet Becker<bennet@becker-dd.de>
 *
 *    This program is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    This program is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU General Public License for more details.
 *
 *    You should have received a copy of the GNU General Public License
 *    along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

/**
 * The the exact number of twitch followers by Account ID
 *
 * @param {String|Number} id
 * @return {Number}
 */
function TWITCHFOLLOWER(id) {
  var up = PropertiesService.getUserProperties();
  var tc = up.getProperty("TWITCH_CID");
  var ta = up.getProperty("TWITCH_KEY");
  if(tc == null || ta == null) {
    return "API NOT CONFIGURED"
  }

  var url = "https://api.twitch.tv/helix/users/follows?to_id=" + id + "&first=1";
  var response = UrlFetchApp.fetch(url, {
    'headers' : {
      'Authorization': 'Bearer ' + ta,
      'Client-Id': tc
    }});

  console.log(response)
  var json = response.getContentText();
  console.log(json)
  var data = JSON.parse(json);

  return data.total;
}

/**
 * The the twitch account ID by username
 *
 * @param {String} name
 * @return {Number}
 */
function TWITCHID(name) {
  var up = PropertiesService.getUserProperties();
  var tc = up.getProperty("TWITCH_CID");
  var ta = up.getProperty("TWITCH_KEY");
  if(tc == null || ta == null) {
    return "API NOT CONFIGURED"
  }

  var url = "https://api.twitch.tv/helix/users?login=" + name.toString().toLowerCase();

  var response = UrlFetchApp.fetch(url, {
    'headers' : {
      'Authorization': 'Bearer ' + ta,
      'Client-Id': tc
    }});

  console.log(response)
  var json = response.getContentText();
  console.log(json)
  var data = JSON.parse(json);

  return data.data[0].id;
}