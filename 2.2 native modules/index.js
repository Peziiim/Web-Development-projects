const fs = require("fs");

fs.writeFile("message.text", "Hello From node.js", (err) => {
    if (err) throw err;
    console.log("The file has been saved")
})