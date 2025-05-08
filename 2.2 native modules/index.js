const fs = require("fs");

fs.writeFile("message.txt", "Hello From node.js", (err) => {
    if (err) throw err;
    console.log("The file has been saved")
})

let read = fs.readFile("message.txt", (err) => {
    if (err) throw err;
    
})

console.log(read)