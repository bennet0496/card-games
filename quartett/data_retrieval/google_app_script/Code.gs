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

function TWITTERFOLLOWER_MAP(values) {
  if(values === "#VALUE!"){
    return;
  }
  console.log(values)
  return MAPFUNC(values, TWITTERFOLLOWER)
}

function YOUTUBESUB_MAP(values) {
  if(values === "#VALUE!"){
    return;
  }
  console.log(values)
  return MAPFUNC(values, YOUTUBESUBS)
}

function MAPFUNC(values, func) {
  if(typeof(values) !== typeof([])) {
    return [func(values)]
  }
  var val = values.flat()
  console.log(values)
  console.log(val)
  console.log(typeof(values))
  console.log(func)
  console.log(typeof(func))
  return val.map(x=>func(x))
}