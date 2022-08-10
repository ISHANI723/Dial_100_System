//JSON data to array
const fs = require('fs');

const file='kolkata_fire_station.json'

fs.readFile(file, (err, data) => {
  if (err) throw err;
  let newData=[]
  data = JSON.parse(data);
  data.forEach((v, i) =>{
    newData.push([v.name, {lat:v.lat,lng:v.lng}])
  })
  console.log(newData)
});


