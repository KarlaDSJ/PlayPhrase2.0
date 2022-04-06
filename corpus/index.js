const getSubtitles = require("youtube-captions-scraper").getSubtitles;
const getChannelVideos = require("usetube").getChannelVideos;
const fs = require("fs");

chanelsKarla = ["UCshVTOdmZLdLj8LTV1j_0uw", "UCJQQVLyM6wtPleV4wFBK06g", 
                "UC_Zc2fmbDpu_arkwvCDcX5g", "UCyQqzYXQBUWgBTn4pw_fFSQ"]

chanelsDavid = [ "UCX6b17PVsYBQ0ip5gyeme", "UC3uPK6zOTe0HOfcIkuzII0Q", 
                 "UCBSs9x2KzSLhyyA9IKyt4YA","UCrVhY_d0L0qayRhMsRlPBOA"]

/**
 * Escribe en un archivo la información de los videos de un canal de youtube 
 * @param {string} chanel 
 * @param {json} json 
 */
function write(chanel, json){
  try {
    fs.writeFileSync(chanel,JSON.stringify(json, null,2))
  } catch (error) {
    console.log("Algo salió mal "+ error);
  }
}

async function getAllSubtitles(videos){
  fails = []
  for (video of videos) {
    try {  
      video["subtitles"] = await getSubtitles({
        videoID: video.id, // youtube video id
        lang: "es", // default: `en`
      });
    } catch (error) {
      fails.push(video.id)
    }
  }
  return videos.filter((x) => !fails.includes(x.id))
}

async function scraper(chanel) {
  videos = await getChannelVideos(chanel);
  videos = videos.map((x) => {
    delete x.duration
    delete x.artist
    delete x.title
    delete x.publishedAt
    return x
  });
  videos = await getAllSubtitles(videos)
  write("data/"+chanel+".json", videos)
}

for (const id in object) {
  scraper(id)
}