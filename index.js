var getSubtitles = require("youtube-captions-scraper").getSubtitles;

//.then(function (captions) {
//   console.log(captions);
// });

var getChannelVideos = require("./getChannelVideos").default;

(async () => {
  videoIDs = await getChannelVideos("UCZcvCpFcLxOKGbMocVgLjEA", 2);
  console.log(videoIDs);
  videoIDs = videoIDs.map((x) => x.id);
  subtitles = {};
  for (id of videoIDs) {
    subtitles[id] = await getSubtitles({
      videoID: id, // youtube video id
      lang: "es", // default: `en`
    });
  }
  console.log(subtitles);
  //scrapper
})();
