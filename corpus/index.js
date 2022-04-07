const getSubtitles = require("youtube-captions-scraper").getSubtitles;
const getChannelVideos = require("usetube").getChannelVideos;
const fs = require("fs");

chanelsKarla = ["UCshVTOdmZLdLj8LTV1j_0uw", "UCJQQVLyM6wtPleV4wFBK06g", 
                "UC_Zc2fmbDpu_arkwvCDcX5g", "UCyQqzYXQBUWgBTn4pw_fFSQ"]

chanelsDavid = [ "UCX6b17PVsYBQ0ip5gyeme", "UC3uPK6zOTe0HOfcIkuzII0Q", 
                 "UCBSs9x2KzSLhyyA9IKyt4YA","UCrVhY_d0L0qayRhMsRlPBOA"]

/**
 * Escribe en un archivo la información de los videos de un canal de youtube 
 * @param {string} chanel id del canal
 * @param {json} json id, título, subtítulos de cada video del canal 
 */
function write(chanel, json){
  try {
    //pasamos el json a string pero en conservando la identación
    fs.writeFileSync(chanel,JSON.stringify(json, null,2))
  } catch (error) {
    console.log("Algo salió mal "+ error);
  }
}

/**
 * Dado id de cada video en el canal obtiene los subtítulos en español, 
 * en caso de no poder obtener los subtítulos del vídeo este se elimina 
 * del json dado
 * @param {json} videos id, título de cada video del canal 
 * @returns regresa el json con los subtítulos de los videos
 */
async function getAllSubtitles(videos){
  fails = []
  for (video of videos) {
    try {  
      video["subtitles"] = await getSubtitles({
        videoID: video.id, // youtube video id
        lang: "es", // default: `en`
      });
    } catch (error) {
      //En caso de no obtener los subtítulos
      fails.push(video.id)
    }
  }
  //Quitamos los vídeos sin subtítulos
  return videos.filter((x) => !fails.includes(x.id))
}

/**
 * Obtiene el id y nombre de los vídeos de un canal de youtube y
 * posteriormente los subtítulos de cada uno, guarda esta información
 * en un archivo .json
 * @param {string} chanel id del canal
 */
async function scraper(chanel) {
  videos = await getChannelVideos(chanel);
  //Quitamos datos innecesarios
  videos = videos.map((x) => {
    delete x.duration
    delete x.artist
    delete x.title
    delete x.publishedAt
    return x
  });
  //obtenemos los subtítulos
  videos = await getAllSubtitles(videos)
  //guardamos
  write("data/"+chanel+".json", videos)
}

//obtenemos los subtítulos de los videos de varios canales
for (const id of chanelsKarla) {
  scraper(id)
}