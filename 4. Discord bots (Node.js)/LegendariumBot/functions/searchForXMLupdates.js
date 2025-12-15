const https = require('node:https');
const {parseString} = require('xml2js'); //parse XML data string into JSON
const {readFileSync, writeFileSync} = require('jsonfile'); //read/write memory JSON file
const {TESTING_MODE} = require('../bot-constants.json');

// URLs for RSS feeds to get
xml_urls = {
  "greenTeam": "https://anchor.fm/s/19bf48c0/podcast/rss",
  "mainTeam": "https://feed.podbean.com/thelegendarium/feed.xml"
}

module.exports = {

  name: "searchForXMLupdates",
  description: "Gets XML file from RSS feed for [mainTeam/greenTeam], and checks if there is a new episode. Returns object with results",

  async execute(teamName) {
    console.log(`updating XML of ${teamName}`);

    // get XML URL for teamName, if its undefined, teamName is invalid
    const xml_url = xml_urls[teamName];
    if (!xml_url) return Promise.reject("error, invalid teamName");

    // get XML file from URL (function at bottom of file)
    const data = await request_XML(xml_url);

    // parse XML file from string (function at bottom of file)
    let parsedData = await parse_XML(data);

    // mainTeam XML is formatted slightly different and requires extra processing step
    if (teamName == "mainTeam") {
      parsedData = JSON.parse(JSON.stringify(parsedData));
    }



    // load information about latest episodes and series from memory.json
    const memory = readFileSync('./memory.json');
    const teamMemory = memory[teamName];


    // get information about latest episode in XML
    let latest_episode_title = parsedData.rss.channel[0].item[0].title[0];
    let latest_episode_link = parsedData.rss.channel[0].item[0].link[0];
    let latest_episode_description = parsedData.rss.channel[0].item[0].description;

    // searches for content between the first paragraph tag <p>CONTENT</p>
    const paragraph_regEx = /\<p\>(.*?)\<\/p\>/;
    latest_episode_description = paragraph_regEx.exec(latest_episode_description)[1];
    if (!latest_episode_description) {
      // if description wasn't found, substitute link
      console.log("| couldn not find episode description, substituting link");
      latest_episode_description = latest_episode_link;
    }

    // if bot is in Test Mode and there's a fake episode loaded, use that instead
    if (TESTING_MODE && teamMemory.fake) {
      latest_episode_title = teamMemory.fake.title;
      latest_episode_description = "Fake description for a fake episode.";
      latest_episode_link = teamMemory.fake.link;

      // set fake episode flag back to false
      memory[teamName].fake = false;  
      writeFileSync('./memory.json', memory, {spaces:2, EOL: '\r\n'});
      console.log("| found fake episode.")
    }


    // if the latest title matches the stored title, return no new episodes
    if (teamMemory.latest_episode.title == latest_episode_title) {
      console.log(`| no new episodes found for ${teamName}`);
      return {teamName: teamName, episode: false}
    }

    // get episode number with RegEx
    const episode_number_regex = /#(\d+)/;
    let latest_episode_number = episode_number_regex.exec(latest_episode_title);
    latest_episode_number = latest_episode_number ? latest_episode_number[1] : -1;

    // start building object to return with information gathered about latest episode in XML
    const resultObject = {
      teamName: teamName,
      episode: {
        title: latest_episode_title,
        description: latest_episode_description,
        link: latest_episode_link,
        number: latest_episode_number
      }
    }

    console.log(resultObject.episode.title);
    // if episode number is higher than stored episode, assume update is valid
    if (latest_episode_number > teamMemory.latest_episode.number) {
      console.log("| episode found with higher number");
    }
    // if episode number equals or is less than stored episode, flag potential invalid update
    else {
      console.log("| FLAG: episode found with lower or equal episode number");
      resultObject.flag = 'NUMBER_FLAG';
    }

    // check if episode belongs in series, if match found, add information to resultObject
    for (const series of teamMemory.series) {
      const identifier_regex = new RegExp(series.identifier,'i'); // 'i' adds case insensitive tag
      // console.log(identifier_regex);
      const series_match = latest_episode_title.match(identifier_regex);
      // console.log(series_match);
      if (series_match) {
        resultObject.series = series;
        break;
      }
    }

    console.log(`| ${teamName} processing complete, returning resultObject`);
    return resultObject

  },

};

// uses promise to make synchronous request for XML data from URL
const request_XML = async function(xml_url) {
  return new Promise((resolve,reject) => {
    https.get(xml_url, (res) => {
      if (!(res.statusCode >= 200 && res.statusCode < 400)) return console.log("| invalid status code error: " + res.statusCode);
      console.log(`| XML found, collecting data.`);
      let data = '';

      res.on('data', (data_) => {
        data += data_.toString();
      });

      res.on('end', () => {
        console.log(`| XML request complete, parsing data.`);

        resolve(data);
      });
    });
  });
}

// uses promise to synchronously parse XML data string
const parse_XML = async function(xml_data) {
  return new Promise ((resolve,reject) => {
    parseString(xml_data,(err,res)=> {
      if (err) {
        reject(err);
      }
      resolve(res)
    });
  });
}
