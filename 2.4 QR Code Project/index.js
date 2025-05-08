import inquirer from 'inquirer';
import fs from 'fs'
import qr from 'qr-image'


inquirer
  .prompt([
    {
        type: 'input',
        name: 'url',
        message: "Digite uma URL",
      }
  ]).then((answers) => {
    const qrCode = qr.image(answers.url, {type: 'png'})
    qrCode.pipe(fs.createWriteStream('qrCode.png'))
  })
  