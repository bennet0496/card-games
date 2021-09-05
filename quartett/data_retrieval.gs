function test(){
  //console.log(TWITCHID("LinusTech"))
  //console.log(TWITCHFOLLOWER(35987962))
  //console.log(TWITTERFOLLOWER("bennet0496"))
  //console.log(MAPFUNC([["LinusTech", "ludwig"]], TWITCHID))
  console.log(YOUTUBESUBS('UCrPseYLGpNygVi34QpGNqpA'))
}

function TWITCHFOLLOWER(id) {
  var url = "https://api.twitch.tv/helix/users/follows?to_id=" + id + "&first=1";
  var response = UrlFetchApp.fetch(url, {
    'headers' : {
      'Authorization': 'Bearer REDACTED',
      'Client-Id': 'REDACTED'
    }});

  console.log(response)
  var json = response.getContentText();
  console.log(json)
  var data = JSON.parse(json);

  return data.total;
}

function TWITCHID(name) {
  var url = "https://api.twitch.tv/helix/users?login=" + name.toString().toLowerCase();

  var response = UrlFetchApp.fetch(url, {
    'headers' : {
      'Authorization': 'Bearer REDACTED',
      'Client-Id': 'REDACTED'
    }});

  console.log(response)
  var json = response.getContentText();
  console.log(json)
  var data = JSON.parse(json);

  return data.data[0].id;
}

function TWITTERFOLLOWER(name) {
  var url = "https://api.twitter.com/2/users/by/username/" + name.toString().toLowerCase() + "?user.fields=public_metrics";

  var response = UrlFetchApp.fetch(url, {
    'headers' : {
      'Authorization': 'Bearer REDACTED'
    }});

  console.log(response)
  var json = response.getContentText();
  console.log(json)
  var data = JSON.parse(json);

  return data.data.public_metrics.followers_count;
}

/**
 * @OnlyCurrentDoc
 */
function YOUTUBESUBS(name) {
  response = YouTube.Channels.list('statistics', {
    id: name,
    key: 'REDACTED'
  })

  console.log(response)
  //var json = response.getContentText();
  //console.log(json)
  //var data = JSON.parse(json);

  return Number(response.items[0].statistics.subscriberCount);
}


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