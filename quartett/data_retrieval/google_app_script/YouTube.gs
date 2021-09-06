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
 * Get the (rounded (by API)) number of Youtube Subs for the YouTube Channel ID
 *
 * @param {String} name
 * @return {Number}
 */
function YOUTUBESUBS(name) {
  var up = PropertiesService.getUserProperties();
  var y = up.getProperty("YTAPI");
  if(y == null) {
    return "API NOT CONFIGURED"
  }

  response = YouTube.Channels.list('statistics', {
    id: name,
    key: y
  })

  console.log(response)
  //var json = response.getContentText();
  //console.log(json)
  //var data = JSON.parse(json);

  return Number(response.items[0].statistics.subscriberCount);
}