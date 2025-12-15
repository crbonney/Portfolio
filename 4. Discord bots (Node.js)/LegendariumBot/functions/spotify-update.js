const request = require('request'); // "Request" library
const {readFileSync, writeFileSync} = require('jsonfile'); //read/write memory JSON file

const {spotify_client_id, spotify_token} = require('../config.json');
const {TESTING_MODE} = require('../bot-constants.json');

const spotify_show_ids = {
    "greenTeam": "7y28T1qUAaZAM75F4Yd1iN",
    "mainTeam": "4ClG3neWN8KRvGt3eYBDQ2"
}
const show_url_builder = function(teamName) {
    return show_url = "https://api.spotify.com/v1/shows/"
    + spotify_show_ids[teamName]
    + "?market=ES";
}

const loginOptions = {
    url: 'https://accounts.spotify.com/api/token',
    headers: {
        'Authorization': 'Basic ' + (Buffer.from(spotify_client_id + ':' + spotify_token).toString('base64'))
    },
    form: {
        grant_type: 'client_credentials'
    },
    json: true
};


module.exports = {
    name: "spotify-update",
    description: "gets episode information from spoptify",
    async get_show_data(teamName) {
        console.log(`beginning ${teamName} update.`);
        // get access token for API call
        const access_options = await login(teamName);

        // get episode data from Spotify API using access token
        const episode_data = await get_show_data(access_options,teamName);

        // load information about latest episodes and series from memory.json
        const memory = readFileSync('./memory.json');
        const teamMemory = memory[teamName];

        // check if fake episode to load, then load it
        if (teamMemory.fake) {
            episode_data.title = teamMemory.fake.title;
            episode_data.description = teamMemory.fake.description;
            episode_data.link = teamMemory.fake.link;
            episode_data.id = "fake_spotify_id";

            // get episode number with RegEx, if it couldn't find one, set to -1
            const episode_number_regex = /#(\d+)/;
            episode_data.number = episode_number_regex.exec(episode_data.title);
            episode_data.number = episode_data.number ? episode_data.number[1] : -1;

            console.log("| found fake episode.")

            // fake flag resets to false after post episode
            // has been confirmed denied in next function
        }


        // store data in object
        const resultObject = 
        {
            teamName: teamName,
            episode: episode_data
        };

        // check for potential flags and add them
        if (episode_data.id == teamMemory.latest_episode.id) {
            resultObject.flag = "ID_FLAG";
            console.log("| FLAG: episode IDs match (episode is not new)");
        } 
//	else if (episode_data.number <= teamMemory.latest_episode.number) {
//            resultObject.flag = "NUMBER_FLAG";
//            console.log("| FLAG: episode nubmer is lower/equal to last episode.");
//        }

        // check if episode belongs in series, if match found, add information to resultObject
        for (const series of teamMemory.series) {
          const identifier_regex = new RegExp(series.identifier,'i'); // 'i' adds case insensitive tag
//          console.log(identifier_regex);
          const series_match = episode_data.title.match(identifier_regex);
//          console.log(episode_data.title);
          if (series_match) {
            resultObject.series = series;
            console.log(`| Episode found to be in ${series_match} series.`);
            break;
          }
        }
        console.log("| returning episode data");
        return resultObject;
    }
}


const login = async function(teamName) {
    return new Promise((resolve,reject) => {
        request.post(loginOptions, async function(error, response, body) {
            if (error || response.statusCode !== 200) {
                console.error("Error logging in: " + error);
                reject("Error: " + error)
                return;
            }

            // use the access token to access the Spotify Web API
            var options = {
              url: show_url_builder(teamName),
              headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                'Authorization': `Bearer ${body.access_token}`
                },
                json: true
            };
            resolve(options);
        });
    });
};


// uses access_token to get episode data from podcast
const get_show_data = async function(access_options,teamName) {
    return new Promise((resolve,reject) => {
        request.get(access_options, function(error, response, body) {
            if (error || response.statusCode !== 200) {
                console.error("| Error getting show: " + error);
                reject("Error: "+ error);
                return;
            }
            const episode_data = {};

	    // find the first non 'null' episode returned by the API
	    // because apparentlly Spotify can sometimes return null as the lastest episode
	    let i=0;
	    let episode = null;
	    while (episode == null && i < body.episodes.items.length) {
		//log to check how many attempts are required to find a valid episode
		console.log("checking item " + i + "..."); 
		episode = body.episodes.items[i];
		i++;
	    }

	    //console.log(episode);
            episode_data.title = episode.name;
            episode_data.link = episode.external_urls.spotify;

            // get episode number with RegEx, if it couldn't find one, set to -1
            const episode_number_regex = /#(\d+)/;
            episode_data.number = episode_number_regex.exec(episode_data.title);
            episode_data.number = episode_data.number ? episode_data.number[1] : -1;
            episode_data.id = episode.id;

            // extract first paragraph of episode description, if it couldn't find it, set to empty

            //unescapeHTML converts html codes into characters
            episode_data.description = unescapeHTML(episode.html_description);
            // regex searches for text between first instance of <p> or <p><br/>
            // and <p or <br/ , which should be the first paragraph of the description
            const regEx = /(<p><br\/>|\<p\>)(.*?)\<(br|\/p)/;
            episode_data.description = regEx.exec(episode_data.description);
            episode_data.description = episode_data.description ? episode_data.description[2] : "";


            console.log("| retrieved episode data from spotify");
            resolve(episode_data);

        });
    });

}


// list of special characters for HTML decoder
const htmlEntities = {
    nbsp: ' ',
    cent: '¢',
    pound: '£',
    yen: '¥',
    euro: '€',
    copy: '©',
    reg: '®',
    lt: '<',
    gt: '>',
    quot: '"',
    amp: '&',
    apos: '\''
};

// undoes HTML character encoding (ex: &39; => ')
const unescapeHTML = function(str) {
    return str.replace(/\&([^;]+);/g, function (entity, entityCode) {
        var match;
        if (entityCode in htmlEntities) {
            return htmlEntities[entityCode];
        /*eslint no-cond-assign: 0*/
        } else if (match = entityCode.match(/^#x([\da-fA-F]+)$/)) {
            return String.fromCharCode(parseInt(match[1], 16));
        /*eslint no-cond-assign: 0*/
        } else if (match = entityCode.match(/^#(\d+)$/)) {
            return String.fromCharCode(~~match[1]);
        } else {
            return entity;
        }
    });
};

