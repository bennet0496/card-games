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
 * Get the number of Twitter Followers by username
 *
 * @param {String} name
 * @return {Number}
 */
function TWITTERFOLLOWER(name) {
  var up = PropertiesService.getUserProperties();
  var t = up.getProperty("TWITTER_BEARER");
  if(t == null) {
    return "API NOT CONFIGURED"
  }
  var url = "https://api.twitter.com/2/users/by/username/" + name.toString().toLowerCase() + "?user.fields=public_metrics";

  var response = UrlFetchApp.fetch(url, {
    'headers' : {
      'Authorization': 'Bearer ' + t
    }});

  console.log(response)
  var json = response.getContentText();
  console.log(json)
  var data = JSON.parse(json);

  return data.data.public_metrics.followers_count;
}